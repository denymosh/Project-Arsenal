#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ANALYZER_DIR = Path(__file__).resolve().parent
TRACKER_PATH = PROJECT_ROOT / "memory" / "analyzed_reports_tracker.json"
TMP_DIR = PROJECT_ROOT / "tmp"


def load_tracker() -> dict:
    if not TRACKER_PATH.exists():
        return {}
    try:
        return json.loads(TRACKER_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_tracker(data: dict) -> None:
    TRACKER_PATH.parent.mkdir(parents=True, exist_ok=True)
    TRACKER_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def newest_unprocessed_report(ticker: str, tracker: dict) -> Path:
    base = PROJECT_ROOT / "reports" / ticker / "originals"
    if not base.exists():
        raise SystemExit(f"not found: {base}")

    done = set(tracker.get(ticker, []))
    candidates = sorted(base.glob("*.pdf"), key=lambda p: p.stat().st_mtime, reverse=True)
    for p in candidates:
        rel = str(p.relative_to(PROJECT_ROOT))
        if rel not in done:
            return p
    raise SystemExit(f"no unprocessed pdf for {ticker}")


def extract_pdf_to_md(pdf_path: Path, ticker: str) -> Path:
    try:
        import fitz
    except Exception as exc:
        raise SystemExit("missing pymupdf. Run: pip install -e . in analyzer directory") from exc

    TMP_DIR.mkdir(parents=True, exist_ok=True)
    out = TMP_DIR / f"{ticker}_{pdf_path.stem}.md"

    doc = fitz.open(pdf_path)
    parts = []
    for idx, page in enumerate(doc, start=1):
        text = page.get_text("text")
        parts.append(f"\n\n# Page {idx}\n\n{text.strip()}\n")
    doc.close()

    out.write_text("".join(parts), encoding="utf-8")
    return out


def build_prompt(ticker: str, report_text: str, source_pdf: str) -> str:
    return (
        f"你是研报结构化分析助手。请分析 {ticker} 最新研报，来源文件: {source_pdf}。\n"
        "必须只输出一个 JSON 对象，不要输出任何解释、前后缀或代码块。\n"
        "JSON 必须符合 AnalysisInput schema: {ticker, report{...}}。\n"
        "report 必须包含: date,institution,institution_en,analyst,rating,target_price,sentiment_score,"
        "views,key_metrics,key_assumptions,risk_factors,blind_spots,catalysts,chart_insights,cross_comparison。\n"
        "评级用中文集合: 强买/买入/增持/持有/减持/卖出。\n\n"
        "研报原文如下:\n"
        f"{report_text}\n"
    )


def extract_json_blob(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, flags=re.S)
        if m:
            text = m.group(1)
    if text.startswith("{"):
        return json.loads(text)

    m = re.search(r"(\{(?:.|\n)*\})", text, flags=re.S)
    if not m:
        raise SystemExit("failed to parse JSON output from openclaw agent")
    return json.loads(m.group(1))


def pick_payload_text(outer: object) -> str | None:
    if not isinstance(outer, dict):
        return None

    for key in ("message", "output", "text", "reply"):
        val = outer.get(key)
        if isinstance(val, str) and val.strip():
            return val

    result = outer.get("result")
    if isinstance(result, dict):
        payloads = result.get("payloads")
        if isinstance(payloads, list):
            for item in payloads:
                if isinstance(item, dict):
                    text = item.get("text")
                    if isinstance(text, str) and text.strip():
                        return text

    return None


def _to_float(value: Any, default: float = 0.0) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        m = re.search(r"-?\d+(?:\.\d+)?", value.replace(",", ""))
        if m:
            try:
                return float(m.group(0))
            except Exception:
                return default
    return default


def normalize_for_save_schema(payload: dict, ticker: str) -> dict:
    if not isinstance(payload, dict):
        raise SystemExit("analysis payload is not a JSON object")

    out = dict(payload)
    out.setdefault("ticker", ticker)
    report = out.get("report")
    if not isinstance(report, dict):
        raise SystemExit("analysis payload missing report object")

    report.setdefault("date", "")
    report.setdefault("institution", "")
    report.setdefault("institution_en", "")
    report.setdefault("analyst", "")
    report.setdefault("rating", "持有")
    report["target_price"] = _to_float(report.get("target_price"), 0.0)
    report["sentiment_score"] = max(-1.0, min(1.0, _to_float(report.get("sentiment_score"), 0.0)))

    views = report.get("views", [])
    if isinstance(views, list):
        norm_views = []
        for item in views:
            if isinstance(item, dict) and "summary" in item:
                norm_views.append(item)
            else:
                text = item if isinstance(item, str) else json.dumps(item, ensure_ascii=False)
                norm_views.append({
                    "topic": "核心观点",
                    "stance": "bullish",
                    "confidence": "medium",
                    "summary": text,
                    "data_points": [],
                    "predictions": [],
                })
        report["views"] = norm_views
    else:
        report["views"] = []

    km = report.get("key_metrics")
    if isinstance(km, dict):
        km.setdefault("revenue_estimate", None)
        km.setdefault("eps_estimate", None)
        km.setdefault("growth_rate", None)
        km.setdefault("margin_estimate", None)
        km.setdefault("other", {})
        report["key_metrics"] = km
    elif isinstance(km, list):
        report["key_metrics"] = {
            "revenue_estimate": None,
            "eps_estimate": None,
            "growth_rate": None,
            "margin_estimate": None,
            "other": {f"metric_{i+1}": str(v) for i, v in enumerate(km)},
        }
    else:
        report["key_metrics"] = {
            "revenue_estimate": None,
            "eps_estimate": None,
            "growth_rate": None,
            "margin_estimate": None,
            "other": {},
        }

    for key in ("key_assumptions", "risk_factors", "blind_spots"):
        val = report.get(key)
        if isinstance(val, list):
            report[key] = [str(x) for x in val]
        elif isinstance(val, str) and val.strip():
            report[key] = [val]
        else:
            report[key] = []

    catalysts = report.get("catalysts", [])
    if isinstance(catalysts, list):
        norm_cats = []
        for item in catalysts:
            if isinstance(item, dict) and "event" in item and "expected_date" in item:
                norm_cats.append(item)
            else:
                text = item if isinstance(item, str) else json.dumps(item, ensure_ascii=False)
                norm_cats.append({
                    "event": text,
                    "expected_date": report.get("date") or "TBD",
                    "importance": "medium",
                    "related_views": [],
                })
        report["catalysts"] = norm_cats
    else:
        report["catalysts"] = []

    charts = report.get("chart_insights", [])
    if isinstance(charts, list):
        norm_charts = []
        for i, item in enumerate(charts, start=1):
            if isinstance(item, dict) and "chart_name" in item and "description" in item:
                norm_charts.append(item)
            else:
                text = item if isinstance(item, str) else json.dumps(item, ensure_ascii=False)
                norm_charts.append({
                    "chart_name": f"chart_{i}",
                    "chart_type": "line",
                    "source_file": "",
                    "description": text,
                    "key_observations": [],
                    "data_not_in_text": [],
                    "investment_implication": "",
                })
        report["chart_insights"] = norm_charts
    else:
        report["chart_insights"] = []

    cc = report.get("cross_comparison")
    if isinstance(cc, dict) and "vs_previous_reports" in cc:
        report["cross_comparison"] = cc
    elif isinstance(cc, list):
        report["cross_comparison"] = {
            "vs_previous_reports": [],
            "consensus_position": " | ".join(str(x) for x in cc),
        }
    elif isinstance(cc, str):
        report["cross_comparison"] = {
            "vs_previous_reports": [],
            "consensus_position": cc,
        }
    else:
        report["cross_comparison"] = {
            "vs_previous_reports": [],
            "consensus_position": "",
        }

    out["report"] = report
    return out


def run_openclaw_analysis(ticker: str, report_file: Path, source_pdf: Path) -> Path:
    report_text = report_file.read_text(encoding="utf-8", errors="ignore")
    prompt = build_prompt(ticker, report_text, str(source_pdf.name))

    cmd = [
        "openclaw",
        "agent",
        "--agent",
        "superbrain",
        "--message",
        prompt,
        "--json",
    ]
    last_err = None
    proc = None
    for attempt in (1, 2):
        try:
            proc = subprocess.run(
                cmd,
                cwd=str(PROJECT_ROOT),
                capture_output=True,
                text=True,
                timeout=900,
            )
            if proc.returncode == 0:
                break
            last_err = f"openclaw agent failed (attempt {attempt}): {proc.stderr or proc.stdout}"
        except subprocess.TimeoutExpired:
            last_err = f"openclaw agent timeout after 900s (attempt {attempt})"

        if attempt == 1:
            time.sleep(3)

    if proc is None or proc.returncode != 0:
        raise SystemExit(last_err or "openclaw agent failed")

    raw = proc.stdout.strip()
    payload = None
    try:
        outer = json.loads(raw)
        payload_text = pick_payload_text(outer)
        if payload_text:
            payload = extract_json_blob(payload_text)
        else:
            payload = extract_json_blob(raw)
    except Exception:
        payload = extract_json_blob(raw)

    payload = normalize_for_save_schema(payload, ticker)

    TMP_DIR.mkdir(parents=True, exist_ok=True)
    out = TMP_DIR / f"analysis_{ticker}.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def run_save_analysis(ticker: str, input_json: Path) -> None:
    cmd = [sys.executable, str(ANALYZER_DIR / "save_analysis.py"), ticker, "--input", str(input_json)]
    subprocess.run(cmd, cwd=str(ANALYZER_DIR), check=True)


def run_auto_push(message: str) -> None:
    cmd = [sys.executable, str(ANALYZER_DIR / "auto_push.py"), message]
    subprocess.run(cmd, cwd=str(ANALYZER_DIR), check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Auto analyze newest unprocessed report and push")
    parser.add_argument("ticker", help="Ticker like NVDA")
    parser.add_argument("--report-file", help="Optional explicit report PDF path")
    parser.add_argument("--skip-push", action="store_true", help="Skip git push / vercel sync")
    args = parser.parse_args()

    ticker = args.ticker.upper()
    tracker = load_tracker()

    if args.report_file:
        report_pdf = Path(args.report_file).resolve()
        if not report_pdf.exists():
            raise SystemExit(f"report file not found: {report_pdf}")
    else:
        report_pdf = newest_unprocessed_report(ticker, tracker)

    extracted_md = extract_pdf_to_md(report_pdf, ticker)
    analysis_json = run_openclaw_analysis(ticker, extracted_md, report_pdf)
    run_save_analysis(ticker, analysis_json)
    if not args.skip_push:
        run_auto_push(f"analysis: update {ticker} newest unprocessed report")

    rel = str(report_pdf.relative_to(PROJECT_ROOT)) if report_pdf.is_relative_to(PROJECT_ROOT) else str(report_pdf)
    tracker.setdefault(ticker, [])
    if rel not in tracker[ticker]:
        tracker[ticker].append(rel)
    save_tracker(tracker)

    print(f"done: {ticker} -> {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
