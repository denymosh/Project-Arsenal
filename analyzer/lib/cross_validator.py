"""
研报分析系统 - 交叉验证模块

准备交叉验证数据：多篇研报间的观点对比矩阵。
"""

from .models import TickerData, MajorDivergence
from .data_manager import load_ticker_data, save_ticker_data


def find_divergences(ticker: str) -> list[MajorDivergence]:
    """
    分析标的所有研报，找出重大分歧

    逻辑：
    1. 对每个观点维度，统计看多/看空的机构
    2. 如果同一维度上既有看多也有看空，标记为分歧
    3. 根据分歧的机构数量判断严重程度
    """
    ticker_data = load_ticker_data(ticker)
    reports = ticker_data.reports

    if len(reports) < 2:
        print("  ℹ️ 研报数量不足2篇，无法进行交叉验证")
        return []

    # 收集每个维度下各机构的立场
    topic_stances: dict[str, dict[str, list[str]]] = {}
    # 格式: { "FSD": { "bullish": ["高盛", "花旗"], "bearish": ["摩根"] } }

    for report in reports:
        for view in report.views:
            topic = view.topic
            stance = view.stance

            if topic not in topic_stances:
                topic_stances[topic] = {"bullish": [], "neutral": [], "bearish": []}

            topic_stances[topic][stance].append(report.institution)

    # 识别分歧
    divergences = []
    for topic, stances in topic_stances.items():
        bulls = stances.get("bullish", [])
        bears = stances.get("bearish", [])

        # 存在看多和看空的对立机构
        if bulls and bears:
            # 判断严重程度
            total_opinions = len(bulls) + len(bears) + len(stances.get("neutral", []))
            if len(bulls) >= 2 and len(bears) >= 2:
                severity = "major"
            elif len(bulls) >= 1 and len(bears) >= 1:
                severity = "moderate"
            else:
                severity = "minor"

            divergence = MajorDivergence(
                topic=topic,
                severity=severity,
                description=f"{', '.join(bulls)}看多 vs {', '.join(bears)}看空",
                bulls=bulls,
                bears=bears,
                impact_on_valuation=f"该维度上{len(bulls)+len(bears)}家机构存在分歧"
            )
            divergences.append(divergence)

    # 按严重程度排序
    severity_order = {"major": 0, "moderate": 1, "minor": 2}
    divergences.sort(key=lambda d: severity_order.get(d.severity, 3))

    # 更新到标的数据
    ticker_data.cross_comparison.major_divergences = divergences

    # 找出最高共识和最大异见
    if topic_stances:
        # 最高共识：所有机构立场一致的维度
        consensus_topics = []
        contrarian_topics = []
        for topic, stances in topic_stances.items():
            total = sum(len(v) for v in stances.values())
            if total >= 2:
                dominant = max(stances.items(), key=lambda x: len(x[1]))
                ratio = len(dominant[1]) / total
                if ratio >= 0.8:
                    consensus_topics.append((topic, dominant[0], ratio))
                elif ratio <= 0.5:
                    contrarian_topics.append((topic, ratio))

        if consensus_topics:
            best = max(consensus_topics, key=lambda x: x[2])
            ticker_data.cross_comparison.highest_conviction_view = (
                f"{best[0]}（{int(best[2]*100)}%机构{'看多' if best[1]=='bullish' else '看空' if best[1]=='bearish' else '中性'}）"
            )

        if contrarian_topics:
            worst = min(contrarian_topics, key=lambda x: x[1])
            ticker_data.cross_comparison.most_contrarian_view = (
                f"{worst[0]}（仅{int(worst[1]*100)}%一致，分歧最大）"
            )

    save_ticker_data(ticker_data)

    if divergences:
        print(f"  ⚡ 发现 {len(divergences)} 个分歧点:")
        for d in divergences:
            emoji = "🔴" if d.severity == "major" else "🟡" if d.severity == "moderate" else "🟢"
            print(f"     {emoji} [{d.severity}] {d.topic}: {d.description}")
    else:
        print(f"  ✅ 所有维度观点基本一致，无重大分歧")

    return divergences
