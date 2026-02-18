"""
研报分析系统 - Pydantic 数据模型定义

定义所有结构化数据的类型，确保数据一致性和验证。
Antigravity分析完研报后输出的JSON必须符合这些模型。
"""

from __future__ import annotations
from typing import Optional
from datetime import date
from pydantic import BaseModel, Field


# ============================================================
# 研报中的单个观点预测
# ============================================================
class Prediction(BaseModel):
    """单个可验证的预测"""
    metric: str = Field(..., description="预测指标名称，如'Q1交付量'")
    predicted_value: str = Field(..., description="预测值，如'42万'")
    deadline: str = Field(..., description="验证时间节点，如'2026-Q2'或'2026-04-02'")
    comparison_to_consensus: Optional[str] = Field(
        None, description="与市场共识的偏离方向: above/inline/below"
    )
    # 以下字段由回溯验证时填入
    verified: bool = Field(False, description="是否已验证")
    actual_value: Optional[str] = Field(None, description="实际值")
    accurate: Optional[bool] = Field(None, description="预测是否准确")
    deviation_pct: Optional[float] = Field(None, description="偏差百分比")


# ============================================================
# 研报中的单个观点
# ============================================================
class View(BaseModel):
    """研报中的一个核心观点"""
    topic: str = Field(..., description="观点主题/维度，如'FSD'、'交付量'")
    stance: str = Field(..., description="立场: bullish/neutral/bearish")
    confidence: str = Field("medium", description="置信度: high/medium/low")
    summary: str = Field(..., description="观点摘要")
    data_points: list[str] = Field(default_factory=list, description="支撑数据点")
    predictions: list[Prediction] = Field(default_factory=list, description="可量化的预测")


# ============================================================
# 关键财务指标预测
# ============================================================
class KeyMetrics(BaseModel):
    """研报中的关键财务预测指标"""
    revenue_estimate: Optional[str] = Field(None, description="营收预测")
    eps_estimate: Optional[str] = Field(None, description="EPS预测")
    growth_rate: Optional[str] = Field(None, description="增长率预测")
    margin_estimate: Optional[str] = Field(None, description="利润率预测")
    other: dict[str, str] = Field(default_factory=dict, description="其他指标")


# ============================================================
# 图表视觉洞察（从PDF图片中解读）
# ============================================================
class ChartInsight(BaseModel):
    """从研报图表/图片中提取的视觉洞察，纯文字提取无法获取的补充信息"""
    chart_name: str = Field(..., description="图表名称，如'EVA Margin vs Share Price'")
    chart_type: str = Field("line", description="图表类型: line/bar/scatter/heatmap/table/flow")
    source_file: str = Field("", description="图片文件名（相对于images目录）")
    description: str = Field(..., description="图表内容的详细描述")
    key_observations: list[str] = Field(default_factory=list, description="从图表中观察到的关键视觉信号")
    data_not_in_text: list[str] = Field(
        default_factory=list,
        description="该图表提供的、但文字中未包含的新增数据/趋势"
    )
    investment_implication: str = Field("", description="该图表对投资决策的启示")


# ============================================================
# 催化剂事件
# ============================================================
class Catalyst(BaseModel):
    """一个催化剂事件"""
    event: str = Field(..., description="事件描述")
    expected_date: str = Field(..., description="预期日期 YYYY-MM-DD 或 YYYY-QN")
    importance: str = Field("medium", description="重要程度: high/medium/low")
    related_views: list[str] = Field(default_factory=list, description="相关观点维度")


# ============================================================
# 与历史研报的对比记录
# ============================================================
class ComparisonRecord(BaseModel):
    """与某篇历史研报的对比"""
    compared_with: str = Field(..., description="对比的研报ID")
    topic: str = Field(..., description="对比维度")
    divergence: str = Field(..., description="分歧程度: major/moderate/minor/consensus")
    description: str = Field(..., description="分歧描述")


class CrossComparisonResult(BaseModel):
    """交叉对比结果"""
    vs_previous_reports: list[ComparisonRecord] = Field(default_factory=list)
    consensus_position: str = Field("", description="该研报在共识中的位置描述")


# ============================================================
# 单篇研报的完整分析结果
# ============================================================
class ReportAnalysis(BaseModel):
    """Antigravity分析一篇研报后的完整结构化输出"""
    # 基本信息
    date: str = Field(..., description="研报发布日期 YYYY-MM-DD")
    institution: str = Field(..., description="发布机构中文名")
    institution_en: str = Field("", description="发布机构英文名")
    analyst: str = Field("", description="分析师姓名")
    rating: str = Field(..., description="评级: 强买/买入/增持/持有/减持/卖出")
    previous_rating: Optional[str] = Field(None, description="前次评级")
    target_price: float = Field(..., description="目标价（美元）")
    previous_target_price: Optional[float] = Field(None, description="前次目标价")
    sentiment_score: float = Field(
        ..., ge=-1.0, le=1.0,
        description="整体情感打分，-1(极度看空)到1(极度看多)"
    )

    # 核心分析内容
    views: list[View] = Field(default_factory=list, description="核心观点列表")
    key_metrics: Optional[KeyMetrics] = Field(None, description="关键财务预测")
    key_assumptions: list[str] = Field(default_factory=list, description="关键假设")
    risk_factors: list[str] = Field(default_factory=list, description="提及的风险因素")
    blind_spots: list[str] = Field(default_factory=list, description="研报未提及的盲点")
    catalysts: list[Catalyst] = Field(default_factory=list, description="催化剂事件")

    # 图表视觉洞察
    chart_insights: list[ChartInsight] = Field(
        default_factory=list, description="从图表/图片中提取的视觉洞察"
    )

    # 交叉对比
    cross_comparison: Optional[CrossComparisonResult] = Field(
        None, description="与历史研报的交叉对比结果"
    )


# ============================================================
# 分析输入文件格式（Antigravity → save_analysis.py）
# ============================================================
class AnalysisInput(BaseModel):
    """Antigravity输出的完整分析文件格式"""
    ticker: str = Field(..., description="标的代码，如'TSLA'")
    report: ReportAnalysis = Field(..., description="分析结果")


# ============================================================
# 标的数据文件中的存储格式
# ============================================================
class StoredReport(ReportAnalysis):
    """存储在 data/{TICKER}.json 中的研报记录，在ReportAnalysis基础上增加了ID等字段"""
    id: str = Field(..., description="唯一标识，格式: YYYYMMDD_institution_en_lower")
    analyst_reliability: Optional[float] = Field(None, description="该分析师的靠谱度评分")
    analysis_file: str = Field("", description="分析MD文件相对路径")


class ConsensusMatrix(BaseModel):
    """共识矩阵：每个维度的看多/中性/看空统计"""
    bullish: int = 0
    neutral: int = 0
    bearish: int = 0
    not_mentioned: int = 0


class MajorDivergence(BaseModel):
    """重大分歧记录"""
    topic: str
    severity: str = Field(..., description="major/moderate/minor")
    description: str
    bulls: list[str] = Field(default_factory=list, description="看多的机构")
    bears: list[str] = Field(default_factory=list, description="看空的机构")
    impact_on_valuation: str = Field("", description="对估值的影响")


class CrossComparison(BaseModel):
    """标的级别的交叉对比数据"""
    consensus_matrix: dict[str, ConsensusMatrix] = Field(default_factory=dict)
    major_divergences: list[MajorDivergence] = Field(default_factory=list)
    highest_conviction_view: str = ""
    most_contrarian_view: str = ""


class CurrentConsensus(BaseModel):
    """当前共识数据"""
    rating: Optional[str] = None
    avg_target_price: Optional[float] = None
    min_target_price: Optional[float] = None
    max_target_price: Optional[float] = None
    sentiment_avg: Optional[float] = None
    total_reports: int = 0
    last_updated: Optional[str] = None


class SentimentRecord(BaseModel):
    """情感历史记录"""
    date: str
    institution: str
    score: float


class TickerData(BaseModel):
    """标的数据文件的完整结构 (data/{TICKER}.json)"""
    ticker: str
    name_en: str
    name_cn: str
    current_consensus: CurrentConsensus = Field(default_factory=CurrentConsensus)
    view_dimensions: list[str] = Field(default_factory=list)
    reports: list[StoredReport] = Field(default_factory=list)
    cross_comparison: CrossComparison = Field(default_factory=CrossComparison)
    sentiment_history: list[SentimentRecord] = Field(default_factory=list)


# ============================================================
# 记分板相关模型
# ============================================================
class TickerAccuracy(BaseModel):
    """某机构在某标的上的准确率"""
    total: int = 0
    verified: int = 0
    accurate: int = 0
    rate: Optional[float] = None


class VerifiedPrediction(BaseModel):
    """已验证的预测记录"""
    date: str
    ticker: str
    prediction: str
    actual: str
    accurate: bool
    deviation_pct: Optional[float] = None


class InstitutionScore(BaseModel):
    """机构评分记录"""
    name: str
    name_en: str = ""
    reliability_score: float = 0.0
    reliability_tier: str = "B"
    total_predictions: int = 0
    verified_predictions: int = 0
    accurate_predictions: int = 0
    accuracy_rate: float = 0.0
    by_ticker: dict[str, TickerAccuracy] = Field(default_factory=dict)
    recent_verified: list[VerifiedPrediction] = Field(default_factory=list)
    accuracy_trend: list[dict] = Field(default_factory=list)


class ReliabilityTier(BaseModel):
    """靠谱度分层定义"""
    min_rate: float
    label: str
    color: str
    weight: float


class Scorecard(BaseModel):
    """记分板完整数据"""
    institutions: list[InstitutionScore] = Field(default_factory=list)
    reliability_tiers: dict[str, ReliabilityTier] = Field(default_factory=dict)
    last_updated: Optional[str] = None


# ============================================================
# 催化剂日历模型
# ============================================================
class PredictionToVerify(BaseModel):
    """待验证的预测"""
    report_id: str
    institution: str
    metric: str
    value: str


class CatalystEvent(BaseModel):
    """催化剂日历中的事件"""
    id: str
    date: str
    ticker: str
    event: str
    importance: str = "medium"
    related_reports: list[str] = Field(default_factory=list)
    predictions_to_verify: list[PredictionToVerify] = Field(default_factory=list)
    verified: bool = False
    actual_result: Optional[str] = None


class CatalystCalendar(BaseModel):
    """催化剂日历完整数据"""
    catalysts: list[CatalystEvent] = Field(default_factory=list)
    last_updated: Optional[str] = None
