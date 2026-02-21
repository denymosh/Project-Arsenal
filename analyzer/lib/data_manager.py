"""
研报分析系统 - JSON数据管理器

负责所有JSON文件的读取、写入、更新和合并操作。
"""

import json
import os
from pathlib import Path
from typing import Optional
from datetime import date

from .models import (
    TickerData, StoredReport, Scorecard, InstitutionScore,
    CatalystCalendar, CatalystEvent, AnalysisInput,
    CurrentConsensus, SentimentRecord, PredictionToVerify
)


# 项目根目录（analyzer的上一级）
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
REPORTS_DIR = PROJECT_ROOT / "reports"


def get_data_dir() -> Path:
    """获取data目录路径"""
    return DATA_DIR


def get_reports_dir() -> Path:
    """获取reports目录路径"""
    return REPORTS_DIR


# ============================================================
# 通用JSON读写
# ============================================================
def read_json(filepath: Path) -> dict:
    """读取JSON文件，如果文件不存在返回空字典"""
    if not filepath.exists():
        return {}
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(filepath: Path, data: dict) -> None:
    """写入JSON文件，自动创建父目录"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✅ 已写入: {filepath.relative_to(PROJECT_ROOT)}")


# ============================================================
# 标的数据操作
# ============================================================
def load_ticker_data(ticker: str) -> TickerData:
    """加载标的数据文件"""
    filepath = DATA_DIR / f"{ticker}.json"
    if not filepath.exists():
        raise FileNotFoundError(f"标的数据文件不存在: {filepath}")
    raw = read_json(filepath)
    return TickerData.model_validate(raw)


def ensure_ticker_registered(ticker: str) -> None:
    """确保标的已注册到 tickers.json 且存在 data/{ticker}.json。"""
    ticker = ticker.upper()

    # 1) 注册到 tickers.json
    tickers_path = DATA_DIR / "tickers.json"
    raw = read_json(tickers_path)
    items = raw.get("tickers", [])
    exists = any((x.get("symbol") or "").upper() == ticker for x in items)
    if not exists:
        items.append({
            "symbol": ticker,
            "name_en": ticker,
            "name_cn": ticker,
            "sector": "待补充",
            "default_dimensions": ["核心业务", "增长", "利润率", "现金流", "竞争格局", "估值"],
        })
        raw["tickers"] = sorted(items, key=lambda x: (x.get("symbol") or ""))
        raw["last_updated"] = date.today().isoformat()
        write_json(tickers_path, raw)
        print(f"  🆕 已自动注册新标的: {ticker}")

    # 2) 创建 data/{ticker}.json 空壳
    ticker_path = DATA_DIR / f"{ticker}.json"
    if not ticker_path.exists():
        stub = TickerData(
            ticker=ticker,
            name_en=ticker,
            name_cn=ticker,
        )
        write_json(ticker_path, stub.model_dump())
        print(f"  🆕 已初始化数据文件: data/{ticker}.json")


def save_ticker_data(ticker_data: TickerData) -> None:
    """保存标的数据文件"""
    filepath = DATA_DIR / f"{ticker_data.ticker}.json"
    write_json(filepath, ticker_data.model_dump())


def generate_report_id(report_date: str, institution_en: str) -> str:
    """
    生成研报唯一ID
    格式: YYYYMMDD_institution（小写下划线连接）
    例如: 20260217_goldman_sachs
    """
    date_part = report_date.replace("-", "")
    inst_part = institution_en.lower().replace(" ", "_").replace(".", "")
    return f"{date_part}_{inst_part}"


def add_report_to_ticker(ticker: str, analysis: AnalysisInput) -> StoredReport:
    """
    将一篇新的研报分析结果添加到标的数据中

    参数:
        ticker: 标的代码
        analysis: Antigravity输出的分析结果

    返回:
        StoredReport: 存储后的研报记录
    """
    # 确保新标的可自动注册并初始化
    ensure_ticker_registered(ticker)

    # 加载现有数据
    ticker_data = load_ticker_data(ticker)
    report = analysis.report

    # 生成ID
    report_id = generate_report_id(report.date, report.institution_en or report.institution)

    # 检查是否已存在（防止重复添加）
    existing_ids = [r.id for r in ticker_data.reports]
    if report_id in existing_ids:
        print(f"  ⚠️ 研报 {report_id} 已存在，将覆盖更新")
        ticker_data.reports = [r for r in ticker_data.reports if r.id != report_id]

    # 构建存储记录
    analysis_filename = f"{report.date}_{report.institution}_{report.rating}_分析.md"
    analysis_path = f"reports/{ticker}/analysis/{analysis_filename}"

    stored = StoredReport(
        id=report_id,
        analysis_file=analysis_path,
        **report.model_dump()
    )

    # 追加到报告列表
    ticker_data.reports.append(stored)

    # 添加情感历史记录
    ticker_data.sentiment_history.append(SentimentRecord(
        date=report.date,
        institution=report.institution,
        score=report.sentiment_score
    ))

    # 更新维度列表（合并新观点的维度）
    for view in report.views:
        if view.topic not in ticker_data.view_dimensions:
            ticker_data.view_dimensions.append(view.topic)

    # 保存
    save_ticker_data(ticker_data)

    return stored


# ============================================================
# 记分板操作
# ============================================================
def load_scorecard() -> Scorecard:
    """加载记分板数据"""
    filepath = DATA_DIR / "scorecard.json"
    raw = read_json(filepath)
    return Scorecard.model_validate(raw)


def save_scorecard(scorecard: Scorecard) -> None:
    """保存记分板数据"""
    filepath = DATA_DIR / "scorecard.json"
    write_json(filepath, scorecard.model_dump())


def ensure_institution_in_scorecard(
    institution: str, institution_en: str = ""
) -> None:
    """确保机构在记分板中有记录，如果没有则创建"""
    scorecard = load_scorecard()
    existing_names = [inst.name for inst in scorecard.institutions]
    if institution not in existing_names:
        scorecard.institutions.append(InstitutionScore(
            name=institution,
            name_en=institution_en
        ))
        scorecard.last_updated = date.today().isoformat()
        save_scorecard(scorecard)
        print(f"  📋 已在记分板中添加新机构: {institution}")


# ============================================================
# 催化剂日历操作
# ============================================================
def load_catalysts() -> CatalystCalendar:
    """加载催化剂日历"""
    filepath = DATA_DIR / "catalysts.json"
    raw = read_json(filepath)
    return CatalystCalendar.model_validate(raw)


def save_catalysts(calendar: CatalystCalendar) -> None:
    """保存催化剂日历"""
    filepath = DATA_DIR / "catalysts.json"
    write_json(filepath, calendar.model_dump())


def add_catalysts_from_report(
    ticker: str, report_id: str, institution: str,
    catalysts: list[dict]
) -> None:
    """
    从研报分析结果中提取催化剂事件并添加到日历

    如果相同事件已存在，则合并研报引用；如果是新事件则新增。
    """
    calendar = load_catalysts()

    for cat in catalysts:
        event_name = cat.get("event", "")
        event_date = cat.get("expected_date", "")

        # 生成催化剂ID
        cat_id = f"{ticker.lower()}_{event_name.replace(' ', '_').lower()[:30]}"

        # 查找是否已存在相同事件
        existing = None
        for existing_cat in calendar.catalysts:
            if existing_cat.ticker == ticker and existing_cat.event == event_name:
                existing = existing_cat
                break

        if existing:
            # 已存在：追加研报引用
            if report_id not in existing.related_reports:
                existing.related_reports.append(report_id)
                # 添加该研报的预测到待验证列表
                for view in cat.get("related_views", []):
                    existing.predictions_to_verify.append(PredictionToVerify(
                        report_id=report_id,
                        institution=institution,
                        metric=event_name,
                        value=f"见{institution}研报分析"
                    ))
        else:
            # 新事件：创建催化剂记录
            new_catalyst = CatalystEvent(
                id=cat_id,
                date=event_date,
                ticker=ticker,
                event=event_name,
                importance=cat.get("importance", "medium"),
                related_reports=[report_id],
                predictions_to_verify=[]
            )
            calendar.catalysts.append(new_catalyst)

    # 按日期排序
    calendar.catalysts.sort(key=lambda c: c.date)
    calendar.last_updated = date.today().isoformat()
    save_catalysts(calendar)


# ============================================================
# 标的列表操作
# ============================================================
def get_all_tickers() -> list[str]:
    """获取所有关注标的的代码列表"""
    filepath = DATA_DIR / "tickers.json"
    raw = read_json(filepath)
    return [t["symbol"] for t in raw.get("tickers", [])]


def get_ticker_info(ticker: str) -> Optional[dict]:
    """获取标的的基本信息"""
    filepath = DATA_DIR / "tickers.json"
    raw = read_json(filepath)
    for t in raw.get("tickers", []):
        if t["symbol"] == ticker:
            return t
    return None
