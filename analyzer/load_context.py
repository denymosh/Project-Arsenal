"""
研报分析系统 - 上下文加载脚本

用法: uv run python load_context.py TSLA

功能: 加载标的的历史分析上下文，供Antigravity阅读后进行交叉对比分析。
输出: 该标的已有研报列表、共识数据、机构靠谱度等信息。
"""

import sys
import os
import json

# Windows环境下强制使用UTF-8编码输出
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# 将analyzer目录加入路径
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))

from lib.data_manager import load_ticker_data, load_scorecard, load_catalysts, get_ticker_info
from lib.backtest_engine import get_unverified_predictions


def load_context(ticker: str) -> None:
    """加载并打印标的的完整上下文"""

    print(f"\n{'='*60}")
    print(f"  📖 {ticker} 历史上下文加载")
    print(f"{'='*60}\n")

    # 1. 标的基本信息
    info = get_ticker_info(ticker)
    if info:
        print(f"📌 标的: {info['symbol']} - {info['name_cn']} ({info['name_en']})")
        print(f"   行业: {info['sector']}")
        print(f"   默认分析维度: {', '.join(info['default_dimensions'])}")
    else:
        print(f"⚠️ 标的 {ticker} 不在关注列表中")
        return

    # 2. 加载标的数据
    try:
        ticker_data = load_ticker_data(ticker)
    except FileNotFoundError:
        print(f"⚠️ 标的数据文件不存在: data/{ticker}.json")
        return

    # 3. 当前共识
    c = ticker_data.current_consensus
    print(f"\n📊 当前共识:")
    if c.total_reports > 0:
        print(f"   评级: {c.rating}")
        print(f"   目标价: ${c.min_target_price} - ${c.max_target_price} (均值: ${c.avg_target_price})")
        print(f"   情感均值: {c.sentiment_avg:+.2f}" if c.sentiment_avg else "   情感均值: -")
        print(f"   研报总数: {c.total_reports}")
    else:
        print("   暂无已分析的研报")

    # 4. 已有研报列表
    if ticker_data.reports:
        print(f"\n📄 已分析研报 ({len(ticker_data.reports)}篇):")
        print(f"   {'日期':<12} {'机构':<10} {'评级':<6} {'目标价':<10} {'情感':<8}")
        print(f"   {'-'*46}")
        for r in sorted(ticker_data.reports, key=lambda x: x.date, reverse=True):
            print(f"   {r.date:<12} {r.institution:<10} {r.rating:<6} ${r.target_price:<9.0f} {r.sentiment_score:+.2f}")

        # 5. 各研报核心观点摘要
        print(f"\n🎯 各研报核心观点:")
        for r in sorted(ticker_data.reports, key=lambda x: x.date, reverse=True):
            print(f"\n   [{r.date}] {r.institution} ({r.rating}, ${r.target_price}):")
            for view in r.views:
                stance_map = {"bullish": "🟢", "neutral": "🟡", "bearish": "🔴"}
                emoji = stance_map.get(view.stance, "⚪")
                print(f"     {emoji} {view.topic}: {view.summary}")

    # 6. 交叉对比：分歧分析
    divergences = ticker_data.cross_comparison.major_divergences
    if divergences:
        print(f"\n⚡ 当前分歧点 ({len(divergences)}个):")
        for d in divergences:
            emoji = "🔴" if d.severity == "major" else "🟡" if d.severity == "moderate" else "🟢"
            print(f"   {emoji} [{d.severity}] {d.topic}")
            print(f"      看多: {', '.join(d.bulls)}")
            print(f"      看空: {', '.join(d.bears)}")

    # 7. 共识矩阵
    matrix = ticker_data.cross_comparison.consensus_matrix
    if matrix:
        print(f"\n🔥 共识矩阵:")
        print(f"   {'维度':<12} {'🟢看多':<8} {'🟡中性':<8} {'🔴看空':<8}")
        print(f"   {'-'*36}")
        for topic, cm in matrix.items():
            print(f"   {topic:<12} {cm.bullish:<8} {cm.neutral:<8} {cm.bearish:<8}")

    # 8. 机构靠谱度
    scorecard = load_scorecard()
    if scorecard.institutions:
        # 筛选与该标的相关的机构
        relevant_insts = []
        for inst in scorecard.institutions:
            if ticker in inst.by_ticker or inst.verified_predictions > 0:
                relevant_insts.append(inst)

        if relevant_insts:
            print(f"\n📋 相关机构靠谱度:")
            print(f"   {'机构':<10} {'准确率':<10} {'等级':<6} {'已验证':<8}")
            print(f"   {'-'*34}")
            for inst in relevant_insts:
                print(
                    f"   {inst.name:<10} {inst.accuracy_rate:.0%}{'':>5} "
                    f"{inst.reliability_tier:<6} {inst.verified_predictions}/{inst.total_predictions}"
                )

    # 9. 待验证的预测
    unverified = get_unverified_predictions(ticker)
    if unverified:
        print(f"\n⏳ 待验证的预测 ({len(unverified)}个):")
        for uv in unverified:
            print(f"   [{uv['date']}] {uv['institution']}: {uv['metric']} = {uv['predicted_value']} (截止{uv['deadline']})")

    # 10. 相关催化剂
    calendar = load_catalysts()
    relevant_cats = [c for c in calendar.catalysts if c.ticker == ticker and not c.verified]
    if relevant_cats:
        print(f"\n📅 即将到来的催化剂:")
        for cat in relevant_cats:
            imp_map = {"high": "🔴", "medium": "🟡", "low": "🟢"}
            emoji = imp_map.get(cat.importance, "⚪")
            print(f"   {emoji} {cat.date} - {cat.event}")

    print(f"\n{'='*60}")
    print(f"  ✅ 上下文加载完成")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: uv run python load_context.py <TICKER>")
        print("示例: uv run python load_context.py TSLA")
        sys.exit(1)

    ticker = sys.argv[1].upper()
    load_context(ticker)
