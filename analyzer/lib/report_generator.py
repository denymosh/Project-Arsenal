"""
研报分析系统 - 分析报告MD生成器

根据结构化分析数据生成Markdown格式的分析报告文件。
"""

from pathlib import Path
from datetime import date

from .models import StoredReport, TickerData
from .data_manager import PROJECT_ROOT, REPORTS_DIR, load_ticker_data


def generate_analysis_md(ticker: str, report: StoredReport) -> Path:
    """
    生成单篇研报的分析MD文件

    参数:
        ticker: 标的代码
        report: 存储的研报记录

    返回:
        生成的MD文件路径
    """
    # 构建文件路径
    filename = f"{report.date}_{report.institution}_{report.rating}_分析.md"
    filepath = REPORTS_DIR / ticker / "analysis" / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # 加载标的数据获取交叉对比上下文
    ticker_data = load_ticker_data(ticker)

    # 生成MD内容
    lines = []

    # 标题
    lines.append(f"# {ticker} 研报分析 - {report.institution} {report.date}")
    lines.append("")

    # 基本信息表
    lines.append("## 📋 基本信息")
    lines.append("")
    lines.append("| 项目 | 内容 |")
    lines.append("|------|------|")
    lines.append(f"| 机构 | {report.institution} ({report.institution_en}) |")
    lines.append(f"| 分析师 | {report.analyst or '未标注'} |")
    lines.append(f"| 日期 | {report.date} |")
    lines.append(f"| 评级 | **{report.rating}** |")
    if report.previous_rating:
        lines.append(f"| 前次评级 | {report.previous_rating} |")
    lines.append(f"| 目标价 | **${report.target_price}** |")
    if report.previous_target_price:
        lines.append(f"| 前次目标价 | ${report.previous_target_price} |")
    lines.append(f"| 情感评分 | {report.sentiment_score:+.2f} (-1到+1) |")
    if report.analyst_reliability is not None:
        lines.append(f"| 分析师靠谱度 | {report.analyst_reliability:.0%} |")
    lines.append("")

    # 核心观点
    lines.append("## 🎯 核心观点")
    lines.append("")

    for i, view in enumerate(report.views, 1):
        # 立场标签
        stance_map = {"bullish": "🟢 看多", "neutral": "🟡 中性", "bearish": "🔴 看空"}
        stance_label = stance_map.get(view.stance, view.stance)

        # 检查是否与其他研报有分歧
        divergence_note = ""
        if report.cross_comparison and report.cross_comparison.vs_previous_reports:
            for comp in report.cross_comparison.vs_previous_reports:
                if comp.topic == view.topic and comp.divergence in ("major", "moderate"):
                    divergence_note = f" ⚡ {comp.description}"

        lines.append(f"### {i}. {view.topic} - {stance_label}{divergence_note}")
        lines.append("")
        lines.append(f"**观点**: {view.summary}")
        lines.append("")

        if view.data_points:
            lines.append("**支撑数据**:")
            for dp in view.data_points:
                lines.append(f"- {dp}")
            lines.append("")

        if view.predictions:
            lines.append("**可量化预测**:")
            lines.append("")
            lines.append("| 指标 | 预测值 | 验证时间 | 共识偏离 | 状态 |")
            lines.append("|------|--------|---------|---------|------|")
            for pred in view.predictions:
                consensus_map = {"above": "⬆️ 高于共识", "inline": "➡️ 符合共识", "below": "⬇️ 低于共识"}
                consensus_label = consensus_map.get(pred.comparison_to_consensus or "", "")
                status = "✅" if pred.accurate else "❌" if pred.accurate is False else "⏳ 待验证"
                lines.append(
                    f"| {pred.metric} | {pred.predicted_value} | {pred.deadline} | {consensus_label} | {status} |"
                )
            lines.append("")

    # 关键财务指标
    if report.key_metrics:
        lines.append("## 📊 关键财务预测")
        lines.append("")
        lines.append("| 指标 | 预测 |")
        lines.append("|------|------|")
        if report.key_metrics.revenue_estimate:
            lines.append(f"| 营收 | {report.key_metrics.revenue_estimate} |")
        if report.key_metrics.eps_estimate:
            lines.append(f"| EPS | {report.key_metrics.eps_estimate} |")
        if report.key_metrics.growth_rate:
            lines.append(f"| 增长率 | {report.key_metrics.growth_rate} |")
        if report.key_metrics.margin_estimate:
            lines.append(f"| 利润率 | {report.key_metrics.margin_estimate} |")
        for key, val in report.key_metrics.other.items():
            lines.append(f"| {key} | {val} |")
        lines.append("")

    # 关键假设
    if report.key_assumptions:
        lines.append("## 💡 关键假设")
        lines.append("")
        for assumption in report.key_assumptions:
            lines.append(f"- {assumption}")
        lines.append("")

    # 风险因素
    if report.risk_factors:
        lines.append("## ⚠️ 风险因素")
        lines.append("")
        for risk in report.risk_factors:
            lines.append(f"- {risk}")
        lines.append("")

    # 盲点分析
    if report.blind_spots:
        lines.append("## 🔍 风险盲点（研报未提及）")
        lines.append("")
        for spot in report.blind_spots:
            lines.append(f"- {spot}")
        lines.append("")

    # 催化剂
    if report.catalysts:
        lines.append("## 📅 催化剂时间节点")
        lines.append("")
        lines.append("| 事件 | 预期日期 | 重要性 | 相关维度 |")
        lines.append("|------|---------|--------|---------|")
        for cat in report.catalysts:
            imp_map = {"high": "🔴 高", "medium": "🟡 中", "low": "🟢 低"}
            imp_label = imp_map.get(cat.importance, cat.importance)
            related = ", ".join(cat.related_views) if cat.related_views else "-"
            lines.append(f"| {cat.event} | {cat.expected_date} | {imp_label} | {related} |")
        lines.append("")

    # 图表视觉洞察
    if hasattr(report, 'chart_insights') and report.chart_insights:
        lines.append("## 📈 图表视觉洞察")
        lines.append("")
        lines.append("> 以下洞察来自研报图表的视觉分析，补充纯文字提取无法获取的信息。")
        lines.append("")
        for ci_idx, ci in enumerate(report.chart_insights, 1):
            chart_type_map = {
                "line": "📉 折线图",
                "bar": "📊 柱状图",
                "scatter": "🔵 散点图",
                "heatmap": "🟥 热力图",
                "table": "📋 数据表",
                "flow": "🔄 流程图",
            }
            ct_label = chart_type_map.get(ci.chart_type, ci.chart_type)
            lines.append(f"### {ci_idx}. {ci.chart_name} ({ct_label})")
            lines.append("")
            if ci.source_file:
                lines.append(f"*来源图片: `images/{ci.source_file}`*")
                lines.append("")
            lines.append(f"**描述**: {ci.description}")
            lines.append("")
            if ci.key_observations:
                lines.append("**关键视觉信号**:")
                for obs in ci.key_observations:
                    lines.append(f"- 👁️ {obs}")
                lines.append("")
            if ci.data_not_in_text:
                lines.append("**文字中未包含的新增数据**:")
                for d in ci.data_not_in_text:
                    lines.append(f"- 🆕 {d}")
                lines.append("")
            if ci.investment_implication:
                lines.append(f"**投资启示**: {ci.investment_implication}")
                lines.append("")

    # 交叉对比结果
    if report.cross_comparison and report.cross_comparison.vs_previous_reports:
        lines.append("## 🔄 与其他研报的交叉对比")
        lines.append("")
        for comp in report.cross_comparison.vs_previous_reports:
            div_map = {
                "major": "🔴 重大分歧",
                "moderate": "🟡 中度偏离",
                "minor": "🟢 轻微差异",
                "consensus": "✅ 共识一致"
            }
            div_label = div_map.get(comp.divergence, comp.divergence)
            lines.append(f"- **{comp.topic}** [{div_label}]: {comp.description}")
        lines.append("")
        if report.cross_comparison.consensus_position:
            lines.append(f"**共识定位**: {report.cross_comparison.consensus_position}")
            lines.append("")

    # 生成日期
    lines.append("---")
    lines.append(f"*分析生成时间: {date.today().isoformat()}*")

    # 写入文件
    content = "\n".join(lines)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  📝 分析报告已生成: {filepath.relative_to(PROJECT_ROOT)}")
    return filepath


def generate_summary_md(ticker: str) -> Path:
    """
    生成标的的汇总对比MD文件

    汇总所有研报的评级、目标价、核心分歧等
    """
    ticker_data = load_ticker_data(ticker)
    filepath = REPORTS_DIR / ticker / "_summary.md"
    filepath.parent.mkdir(parents=True, exist_ok=True)

    lines = []
    lines.append(f"# {ticker} ({ticker_data.name_cn}) - 研报汇总")
    lines.append("")
    lines.append(f"*最后更新: {date.today().isoformat()}*")
    lines.append("")

    # 共识概览
    c = ticker_data.current_consensus
    if c.total_reports > 0:
        lines.append("## 📊 共识概览")
        lines.append("")
        lines.append("| 指标 | 值 |")
        lines.append("|------|-----|")
        lines.append(f"| 共识评级 | **{c.rating}** |")
        lines.append(f"| 平均目标价 | ${c.avg_target_price:.0f} |" if c.avg_target_price else "| 平均目标价 | - |")
        lines.append(f"| 目标价区间 | ${c.min_target_price} - ${c.max_target_price} |" if c.min_target_price else "| 目标价区间 | - |")
        lines.append(f"| 情感均值 | {c.sentiment_avg:+.2f} |" if c.sentiment_avg else "| 情感均值 | - |")
        lines.append(f"| 研报总数 | {c.total_reports} |")
        lines.append("")

    # 研报列表
    if ticker_data.reports:
        lines.append("## 📄 研报列表")
        lines.append("")
        lines.append("| 日期 | 机构 | 评级 | 目标价 | 情感 | 分析文件 |")
        lines.append("|------|------|------|--------|------|---------|")
        for r in sorted(ticker_data.reports, key=lambda x: x.date, reverse=True):
            sentiment_bar = "🟢" if r.sentiment_score > 0.3 else "🔴" if r.sentiment_score < -0.3 else "🟡"
            analysis_link = f"[查看](analysis/{r.date}_{r.institution}_{r.rating}_分析.md)"
            lines.append(
                f"| {r.date} | {r.institution} | {r.rating} | ${r.target_price} | "
                f"{sentiment_bar} {r.sentiment_score:+.2f} | {analysis_link} |"
            )
        lines.append("")

    # 分歧分析
    divergences = ticker_data.cross_comparison.major_divergences
    if divergences:
        lines.append("## ⚡ 主要分歧")
        lines.append("")
        for d in divergences:
            emoji = "🔴" if d.severity == "major" else "🟡" if d.severity == "moderate" else "🟢"
            lines.append(f"### {emoji} {d.topic} [{d.severity}]")
            lines.append("")
            lines.append(f"- **看多**: {', '.join(d.bulls)}")
            lines.append(f"- **看空**: {', '.join(d.bears)}")
            lines.append(f"- **影响**: {d.impact_on_valuation}")
            lines.append("")

    # 共识矩阵
    matrix = ticker_data.cross_comparison.consensus_matrix
    if matrix:
        lines.append("## 🔥 共识矩阵")
        lines.append("")
        lines.append("| 维度 | 🟢看多 | 🟡中性 | 🔴看空 | 未提及 |")
        lines.append("|------|--------|--------|--------|--------|")
        for topic, cm in matrix.items():
            lines.append(
                f"| {topic} | {cm.bullish} | {cm.neutral} | {cm.bearish} | {cm.not_mentioned} |"
            )
        lines.append("")

    content = "\n".join(lines)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  📋 汇总文件已更新: {filepath.relative_to(PROJECT_ROOT)}")
    return filepath
