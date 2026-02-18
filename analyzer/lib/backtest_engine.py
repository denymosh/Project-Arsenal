"""
研报分析系统 - 回溯验证引擎

将研报中的预测与实际数据进行对比，更新准确率和记分板。
"""

from datetime import date
from typing import Optional

from .models import TickerData, Scorecard, VerifiedPrediction, TickerAccuracy
from .data_manager import (
    load_ticker_data, save_ticker_data,
    load_scorecard, save_scorecard,
    load_catalysts, save_catalysts
)


def verify_prediction(
    ticker: str,
    metric: str,
    actual_value: str,
    accurate: bool,
    deviation_pct: Optional[float] = None
) -> dict:
    """
    验证一个特定指标的预测

    参数:
        ticker: 标的代码
        metric: 预测指标名（需与研报中的prediction.metric匹配）
        actual_value: 实际值
        accurate: 预测是否准确
        deviation_pct: 偏差百分比（可选）

    返回:
        验证结果摘要
    """
    ticker_data = load_ticker_data(ticker)
    scorecard = load_scorecard()
    results = []

    # 遍历所有研报，找到匹配的预测
    for report in ticker_data.reports:
        for view in report.views:
            for pred in view.predictions:
                if pred.metric == metric and not pred.verified:
                    # 更新预测验证状态
                    pred.verified = True
                    pred.actual_value = actual_value
                    pred.accurate = accurate
                    pred.deviation_pct = deviation_pct

                    result = {
                        "report_id": report.id,
                        "institution": report.institution,
                        "predicted": pred.predicted_value,
                        "actual": actual_value,
                        "accurate": accurate,
                        "deviation_pct": deviation_pct
                    }
                    results.append(result)

                    # 更新记分板
                    _update_institution_score(
                        scorecard, report.institution, report.institution_en,
                        ticker, pred, actual_value, accurate, deviation_pct
                    )

                    status = "✅" if accurate else "❌"
                    print(f"  {status} {report.institution}: 预测{pred.predicted_value} → 实际{actual_value}")

    # 保存更新
    save_ticker_data(ticker_data)

    scorecard.last_updated = date.today().isoformat()
    save_scorecard(scorecard)

    # 更新催化剂日历中对应事件的验证状态
    _update_catalyst_verification(ticker, metric, actual_value)

    return {
        "metric": metric,
        "actual_value": actual_value,
        "verified_count": len(results),
        "details": results
    }


def _update_institution_score(
    scorecard: Scorecard,
    institution: str,
    institution_en: str,
    ticker: str,
    prediction,
    actual_value: str,
    accurate: bool,
    deviation_pct: Optional[float]
) -> None:
    """更新机构的记分板数据"""
    # 查找或创建机构记录
    inst_record = None
    for inst in scorecard.institutions:
        if inst.name == institution:
            inst_record = inst
            break

    if inst_record is None:
        inst_record = __import__("lib.models", fromlist=["InstitutionScore"]).InstitutionScore(
            name=institution,
            name_en=institution_en
        )
        scorecard.institutions.append(inst_record)

    # 更新总预测数
    inst_record.total_predictions += 1
    inst_record.verified_predictions += 1
    if accurate:
        inst_record.accurate_predictions += 1

    # 计算准确率
    if inst_record.verified_predictions > 0:
        inst_record.accuracy_rate = (
            inst_record.accurate_predictions / inst_record.verified_predictions
        )
        inst_record.reliability_score = inst_record.accuracy_rate

    # 更新靠谱度分层
    rate = inst_record.accuracy_rate
    if rate >= 0.9:
        inst_record.reliability_tier = "S"
    elif rate >= 0.8:
        inst_record.reliability_tier = "A"
    elif rate >= 0.65:
        inst_record.reliability_tier = "B"
    elif rate >= 0.5:
        inst_record.reliability_tier = "C"
    else:
        inst_record.reliability_tier = "D"

    # 更新按标的统计
    if ticker not in inst_record.by_ticker:
        inst_record.by_ticker[ticker] = TickerAccuracy()
    ta = inst_record.by_ticker[ticker]
    ta.total += 1
    ta.verified += 1
    if accurate:
        ta.accurate += 1
    ta.rate = ta.accurate / ta.verified if ta.verified > 0 else None

    # 添加到最近验证列表（保留最近20条）
    inst_record.recent_verified.append(VerifiedPrediction(
        date=date.today().isoformat(),
        ticker=ticker,
        prediction=prediction.predicted_value,
        actual=actual_value,
        accurate=accurate,
        deviation_pct=deviation_pct
    ))
    inst_record.recent_verified = inst_record.recent_verified[-20:]


def _update_catalyst_verification(ticker: str, metric: str, actual_value: str) -> None:
    """更新催化剂日历中相关事件的验证状态"""
    calendar = load_catalysts()
    for catalyst in calendar.catalysts:
        if catalyst.ticker == ticker and not catalyst.verified:
            # 检查是否有相关预测被验证
            for ptv in catalyst.predictions_to_verify:
                if ptv.metric == metric or catalyst.event in metric:
                    catalyst.verified = True
                    catalyst.actual_result = actual_value
                    break
    save_catalysts(calendar)


def get_unverified_predictions(ticker: str) -> list[dict]:
    """
    获取标的所有尚未验证的预测

    返回:
        待验证预测的列表
    """
    ticker_data = load_ticker_data(ticker)
    unverified = []

    for report in ticker_data.reports:
        for view in report.views:
            for pred in view.predictions:
                if not pred.verified:
                    unverified.append({
                        "report_id": report.id,
                        "institution": report.institution,
                        "date": report.date,
                        "topic": view.topic,
                        "metric": pred.metric,
                        "predicted_value": pred.predicted_value,
                        "deadline": pred.deadline
                    })

    return unverified
