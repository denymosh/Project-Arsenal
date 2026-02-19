"""
研报分析系统 - 共识计算模块

根据所有已分析的研报，计算当前共识评级、目标价区间、情感均值等。
每次添加新研报后自动调用。
"""

from datetime import date
from .models import TickerData, CurrentConsensus, ConsensusMatrix
from .data_manager import load_ticker_data, save_ticker_data


# 评级权重映射（用于计算加权共识）
RATING_SCORES = {
    "强买": 5,
    "买入": 4,
    "增持": 3,
    "持有": 2,
    "减持": 1,
    "卖出": 0,
}

# 反向映射：分数 → 评级
SCORE_TO_RATING = {
    (4.5, 5.0): "强买",
    (3.5, 4.5): "买入",
    (2.5, 3.5): "增持",
    (1.5, 2.5): "持有",
    (0.5, 1.5): "减持",
    (0.0, 0.5): "卖出",
}


def score_to_rating(score: float) -> str:
    """将数值评分转换为评级文字"""
    for (low, high), rating in SCORE_TO_RATING.items():
        if low <= score <= high:
            return rating
    return "持有"


def update_consensus(ticker: str) -> CurrentConsensus:
    """
    重新计算标的的共识数据

    基于所有已分析研报计算：
    - 平均评级
    - 目标价区间（最低/平均/最高）
    - 平均情感分数
    """
    ticker_data = load_ticker_data(ticker)
    reports = ticker_data.reports

    if not reports:
        ticker_data.current_consensus = CurrentConsensus()
        save_ticker_data(ticker_data)
        return ticker_data.current_consensus

    # 计算评级共识
    rating_scores = []
    for r in reports:
        if r.rating in RATING_SCORES:
            rating_scores.append(RATING_SCORES[r.rating])

    avg_rating_score = sum(rating_scores) / len(rating_scores) if rating_scores else 2.0
    consensus_rating = score_to_rating(avg_rating_score)

    # 计算目标价区间
    target_prices = [r.target_price for r in reports if r.target_price > 0]
    avg_tp = sum(target_prices) / len(target_prices) if target_prices else None
    min_tp = min(target_prices) if target_prices else None
    max_tp = max(target_prices) if target_prices else None

    # 计算情感均值
    sentiments = [r.sentiment_score for r in reports]
    avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else None

    # 更新共识
    consensus = CurrentConsensus(
        rating=consensus_rating,
        avg_target_price=round(avg_tp, 2) if avg_tp else None,
        min_target_price=min_tp,
        max_target_price=max_tp,
        sentiment_avg=round(avg_sentiment, 3) if avg_sentiment else None,
        total_reports=len(reports),
        last_updated=date.today().isoformat()
    )

    ticker_data.current_consensus = consensus
    save_ticker_data(ticker_data)

    tp_range = "N/A"
    if min_tp is not None and max_tp is not None:
        if min_tp == max_tp:
            tp_range = f"${min_tp}"
        else:
            tp_range = f"${min_tp}-${max_tp}"

    tp_avg = f"${avg_tp:.2f}" if avg_tp is not None else "N/A"
    sentiment_text = f"{avg_sentiment:.2f}" if avg_sentiment is not None else "N/A"

    print(f"  📊 共识更新完成:")
    print(f"     评级: {consensus_rating} | 目标价: {tp_range} (均值{tp_avg})")
    print(f"     情感均值: {sentiment_text} | 研报总数: {len(reports)}")

    return consensus


def update_consensus_matrix(ticker: str) -> None:
    """
    更新交叉对比的共识矩阵

    统计每个观点维度上，看多/中性/看空的机构数量
    """
    ticker_data = load_ticker_data(ticker)
    reports = ticker_data.reports
    dimensions = ticker_data.view_dimensions

    # 构建共识矩阵
    matrix = {}
    for dim in dimensions:
        matrix[dim] = ConsensusMatrix()

    for report in reports:
        covered_topics = set()
        for view in report.views:
            topic = view.topic
            if topic not in matrix:
                matrix[topic] = ConsensusMatrix()

            covered_topics.add(topic)
            if view.stance == "bullish":
                matrix[topic].bullish += 1
            elif view.stance == "neutral":
                matrix[topic].neutral += 1
            elif view.stance == "bearish":
                matrix[topic].bearish += 1

        # 未提及的维度计数
        for dim in dimensions:
            if dim not in covered_topics:
                if dim in matrix:
                    matrix[dim].not_mentioned += 1

    ticker_data.cross_comparison.consensus_matrix = {
        k: v for k, v in matrix.items()
    }

    save_ticker_data(ticker_data)
    print(f"  🔥 共识矩阵已更新（{len(matrix)}个维度）")
