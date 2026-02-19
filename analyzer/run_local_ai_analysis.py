#!/usr/bin/env python3
"""Run local AI analysis (OpenAI-compatible API) and persist into project data.

Usage:
  python run_local_ai_analysis.py TSLA \
    --report-file ../reports/TSLA/originals/2026-02-18_xxx.md \
    --model anthropic/claude-opus-4.1 \
    --auto-push
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ANALYZER_DIR = Path(__file__).resolve().parent
TMP_DIR = PROJECT_ROOT / "tmp"


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())


def call_model(prompt: str, model: str) -> str:
    base_url = os.environ.get("LOCAL_AI_BASE_URL", "").rstrip("/")
    api_key = os.environ.get("LOCAL_AI_API_KEY", "")
    if not base_url or not api_key:
        raise RuntimeError("Missing LOCAL_AI_BASE_URL or LOCAL_AI_API_KEY")

    url = f"{base_url}/chat/completions"
    body = {
        "model": model,
        "temperature": 0.2,
        "messages": [
            {
                "role": "system",
                "content": (
                    "你是研报结构化分析助手。仅输出JSON，不要解释。"
                    "输出必须符合 AnalysisInput schema: {ticker, report{...}}。"
                ),
            },
            {"role": "user", "content": prompt},
        ],
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


def extract_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, flags=re.S)
        if m:
            text = m.group(1)
    return json.loads(text)


def run_save_analysis(ticker: str, input_path: Path) -> None:
    cmd = [sys.executable, str(ANALYZER_DIR / "save_analysis.py"), ticker, "--input", str(input_path)]
    subprocess.run(cmd, cwd=str(ANALYZER_DIR), check=True)


def run_auto_push(msg: str) -> None:
    cmd = [sys.executable, str(ANALYZER_DIR / "auto_push.py"), msg]
    subprocess.run(cmd, cwd=str(ANALYZER_DIR), check=True)


def build_prompt(ticker: str, report_text: str) -> str:
    return (
        f"请分析以下{ticker}研报内容，并输出严格JSON。\n"
        "要求覆盖: institution, rating, target_price, sentiment_score, views, key_metrics,"
        "key_assumptions, risk_factors, blind_spots, catalysts, chart_insights, cross_comparison。\n\n"
        "研报原文:\n"
        f"{report_text}\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run local AI analysis and save to project")
    parser.add_argument("ticker", help="Ticker like TSLA")
    parser.add_argument("--report-file", required=True, help="Path to text/markdown report content")
    parser.add_argument("--model", required=True, help="Model id under your configured API")
    parser.add_argument("--auto-push", action="store_true", help="Run auto_push.py after save")
    args = parser.parse_args()

    load_env(PROJECT_ROOT / ".env.local_ai")
    ticker = args.ticker.upper()
    report_path = Path(args.report_file)
    if not report_path.is_absolute():
        report_path = (PROJECT_ROOT / report_path).resolve()
    if not report_path.exists():
        raise SystemExit(f"report file not found: {report_path}")

    report_text = report_path.read_text(encoding="utf-8", errors="ignore")
    prompt = build_prompt(ticker, report_text)

    content = call_model(prompt=prompt, model=args.model)
    payload = extract_json(content)

    TMP_DIR.mkdir(parents=True, exist_ok=True)
    out = TMP_DIR / f"analysis_{ticker}.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"saved model output => {out}")

    run_save_analysis(ticker, out)
    if args.auto_push:
        run_auto_push(f"analysis: update {ticker} by local-ai model {args.model}")

    print("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
