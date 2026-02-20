#!/usr/bin/env python3
"""Update TSLA.json: fill in Report 0 (Argus) and Report 2 (Morningstar) missing fields."""
import json, os

DATA_PATH = os.path.expanduser("~/openclaw-workspace-superbrain/Project/antigravity-research/luminescent-hubble/data/TSLA.json")

with open(DATA_PATH, "r") as f:
    data = json.load(f)

# ============================================================
# REPORT 0: Argus Research
# ============================================================
r0 = data["reports"][0]

# --- chart_insights ---
r0["chart_insights"] = [
    {
        "chart_name": "TSLA Price & EPS/Revenue Overview",
        "chart_type": "line",
        "source_file": "images/Argus_TSLA_4Q25_p1.png",
        "description": "Argus第1页综合概览：包含2024-2027年TSLA股价走势图（含200日均线）、季度EPS柱状图、季度Revenue柱状图，以及Key Statistics面板",
        "key_observations": [
            "👁️ 股价在2025Q4触及52周高点$498.83后回落至$449.06，200日均线从~$200稳步上升至~$400区间",
            "👁️ EPS从2024年$2.29大幅下降至2025年$1.67（-27%），Argus预计2026E恢复至$2.03、2027E $2.95",
            "👁️ Revenue从2024年$97.7B微降至2025年$94.8B（-3%），但预计2026E反弹至$105.3B（+11%）、2027E $122.2B（+16%）",
            "👁️ 季度EPS走势显示2025年四个季度均低于2024年同期（0.27/0.40/0.50/0.50 vs 0.45/0.52/0.72/0.60）"
        ],
        "data_not_in_text": [
            "🆕 200日均线在2025年底约$350-380区间，当前股价$449高于均线约15-20%，技术面偏强",
            "🆕 2027年季度EPS预估呈加速增长：Q1 $0.59→Q4 $0.82，暗示下半年盈利弹性更大",
            "🆕 2027年季度Revenue预估：Q1 $27.5B→Q4 $33.7B，Q4同比增长约26%"
        ],
        "investment_implication": "EPS从2025年$1.67到2027E $2.95意味着77%增长，但当前P/E 205x仍需大幅压缩才能合理化。Revenue增长预期（2027E +16%）与EPS增长（+45%）的差距暗示利润率改善是关键假设"
    },
    {
        "chart_name": "Growth & Valuation Analysis (2021-2025)",
        "chart_type": "table",
        "source_file": "images/Argus_TSLA_4Q25_p2.png",
        "description": "Argus第2页左侧：2021-2025年增长分析表格，包含Revenue、COGS、Gross Profit、Operating Income、Net Income、EPS等完整损益数据，以及增长率和估值区间",
        "key_observations": [
            "👁️ Operating Income从2022年峰值$13.8B连续三年下滑至2025年$4.8B（-65%），降幅远超Revenue（-14%）",
            "👁️ R&D支出从2021年$2.6B激增至2025年$6.4B（+147%），占Revenue比从4.8%升至6.8%，反映AI/自动驾驶投入加速",
            "👁️ 2025年P/E区间461.9-198.4x，即使取低端198x仍远高于2022年低端29.9x，估值泡沫显著",
            "👁️ Sustainable Growth Rate从2022年33.4%暴跌至2025年6.8%，反映盈利能力大幅恶化"
        ],
        "data_not_in_text": [
            "🆕 SG&A从2022年$3.9B增至2025年$5.8B（+48%），增速超过Revenue，管理费用控制不佳",
            "🆕 税率从2021年11%→2025年27%，税负大幅增加是净利润下降的隐藏因素",
            "🆕 Price/Cash Flow从2022年低端23.3x升至2025年低端47.9x，现金流估值也在恶化",
            "🆕 2023年Income Taxes为-$5B（负数），对应Net Income $15B的异常高值，说明2023年盈利含大额税收优惠"
        ],
        "investment_implication": "核心矛盾：Revenue增长停滞（2024-2025近零增长）但R&D和SG&A持续膨胀，Operating Margin从2022年17%压缩至2025年5.1%。除非AI/Robotaxi投入在2027年开始产生规模收入，否则利润率难以恢复"
    },
    {
        "chart_name": "Financial & Risk Analysis (2023-2025)",
        "chart_type": "table",
        "source_file": "images/Argus_TSLA_4Q25_p2.png",
        "description": "Argus第2页右侧：2023-2025年财务实力和风险分析表格，包含现金、流动比率、债务比率、利润率、回报率和风险指标",
        "key_observations": [
            "👁️ ROE从2023年27.9%暴跌至2025年4.9%，ROA从15.9%降至2.9%，资本回报率接近行业平均水平",
            "👁️ Working Capital从2023年$20.9B增至2025年$36.9B（+77%），流动性极为充裕",
            "👁️ Operating Margin从2023年9.2%→2025年5.1%，连续两年下滑，盈利能力持续恶化",
            "👁️ Oper Income/Int Exp从2023年64.9x降至2025年16.6x，利息覆盖率下降但仍安全"
        ],
        "data_not_in_text": [
            "🆕 Cash Cycle从2023年4.8天延长至2025年13.9天，运营效率下降，可能反映库存积压或应收账款增加",
            "🆕 Cash Flow/Cap Ex从2023年1.5x→2025年1.7x，虽然利润下降但现金流对资本支出的覆盖反而改善",
            "🆕 Total Debt/Equity从2023年15.3%升至2025年17.9%，杠杆略有增加但仍处低位"
        ],
        "investment_implication": "财务实力的核心矛盾：$36.9B Working Capital和$16.5B现金提供了充足的安全垫，但ROE从28%跌至5%说明资本效率极低。2026年$20B+资本支出计划将进一步考验现金流"
    },
    {
        "chart_name": "Peer & Industry Comparison Scatterplot",
        "chart_type": "scatter",
        "source_file": "images/Argus_TSLA_4Q25_p3.png",
        "description": "Argus第3页：TSLA vs GM vs Ford的增长-估值散点图（X轴=5yr Growth Rate, Y轴=P/E），以及多维度估值对比条形图（P/E, P/S, P/B, PEG, 5yr Growth, Debt/Capital）",
        "key_observations": [
            "👁️ TSLA在散点图右上角极端位置：5yr Growth 105%, P/E 205x，与GM（7%, 7.2x）和Ford（4%, 13x）形成巨大鸿沟",
            "👁️ TSLA Net Margin仅4.0%，低于Ford的2.5%但高于GM的1.5%——利润率并不支撑其极高估值",
            "👁️ 估值条形图中TSLA在P/E、P/S、P/B、5yr Growth上均为5（最高），仅Debt/Capital为1（最低），PEG为2-3",
            "👁️ GM和Ford均获BUY评级，TSLA获HOLD——Argus认为传统车企估值更具吸引力"
        ],
        "data_not_in_text": [
            "🆕 TSLA市值$1.56T是GM($78B)+Ford($55B)之和的11.7倍，但Revenue仅为两者之和的约60%",
            "🆕 PEG评分TSLA为2-3（vs Market），说明即使考虑105%的5年增长预期，估值仍偏高",
            "🆕 TSLA 1yr EPS Growth 45.3%看似强劲，但这是从极低基数（2025年$1.08 EPS）的反弹"
        ],
        "investment_implication": "TSLA的估值完全建立在105%的5年EPS增长预期上。如果Robotaxi/AI变现延迟，增长率下调至50%，P/E可能从205x压缩至100x以下，对应股价腰斩风险。相比之下GM/Ford提供了更好的风险回报比"
    }
]

# --- key_metrics ---
r0["key_metrics"] = {
    "revenue_estimate": "$105.3B (FY2026E), $122.2B (FY2027E)",
    "eps_estimate": "$2.03 (FY2026E), $2.95 (FY2027E)",
    "growth_rate": "-2.9% Revenue YoY (2025), 21.56% 1yr EPS Growth Forecast, 105% 5yr EPS Growth Forecast",
    "margin_estimate": "20.1% Gross Margin (Q4 2025), 5.1% Operating Margin (FY2025), 4.0% Net Margin",
    "valuation_multiple": "P/E 205.2x (FY2026E), P/S 16.48x, P/B 16.86x, P/CF 91.1x, EV/EBITDA 127.9x",
    "other": "Beta 1.64, Debt/Capital 9.2%, Cash $16.5B, Market Cap $1.56T, Credit Baa3/BBB stable"
}

# --- risk_factors ---
r0["risk_factors"] = [
    "核心EV需求放缓：联邦$7,500税收抵免到期+消费者兴趣减弱，2025年交付量同比下降",
    "竞争加剧：GM、Ford等传统车企及新势力加速EV布局，Tesla美国EV市场份额从~80%降至~50%",
    "定价压力导致毛利率增长不一致，前瞻性盈利预期持续下调（2026E EPS从$2.26下调至$2.03）",
    "2026年资本支出计划超$200亿（2025年仅$90亿），大规模投入AI/Robotaxi/Optimus但近期回报可见性差",
    "估值指标处于历史高位或接近高位（P/E 205x, P/S 14.2x），大部分估值依赖未经验证的长期赌注",
    "宏观风险：全球经济疲软、消费偏好变化、原材料成本上升、关税成本增加",
    "管理层风险：CEO Musk同时管理SpaceX、xAI等多家公司，精力分散"
]

# --- catalysts ---
r0["catalysts"] = [
    {
        "event": "2026年Robotaxi服务扩展至7个新城市",
        "expected_date": "2026-H1",
        "impact": "positive",
        "description": "如果Robotaxi成功扩展并产生可观收入，将验证AI投资逻辑，可能触发估值重估"
    },
    {
        "event": "Optimus机器人量产启动",
        "expected_date": "2026-H2",
        "impact": "positive",
        "description": "管理层计划2026年底开始量产，如果按时推进将打开全新收入来源"
    },
    {
        "event": "美国EV税收抵免政策变化",
        "expected_date": "2026",
        "impact": "negative",
        "description": "$7,500联邦税收抵免到期将直接冲击EV需求和交付量"
    },
    {
        "event": "Q1 2026财报（预计4月底）",
        "expected_date": "2026-04-28",
        "impact": "neutral",
        "description": "管理层预期2026年包含'艰难的季度'，Q1可能是交付量和利润率的低点"
    }
]

# --- blind_spots ---
r0["blind_spots"] = [
    "Argus未量化能源业务的独立估值贡献——Energy Storage Q4收入$3.84B同比+25%，可能被低估",
    "未讨论FSD订阅收入的增长潜力和对毛利率的提升作用",
    "未考虑SpaceX/xAI合并对Tesla的潜在协同效应",
    "未分析Tesla在中国市场的具体竞争格局和份额变化",
    "未提及Supercharger网络开放（NACS标准）带来的充电业务收入潜力"
]

# --- supplement data_points for each view ---
for v in r0["views"]:
    if v["topic"] == "FSD/自动驾驶":
        v["data_points"] = [
            "2026年资本支出计划超$200亿（2025年仅$90亿），主要用于自动驾驶和Optimus扩产",
            "估值高度依赖未经验证的长期赌注如robotaxi和AI",
            "近期回报可见性很差，资本消耗速度极快",
            "R&D支出从2021年$2.6B增至2025年$6.4B（+147%），占Revenue 6.8%"
        ]
    elif v["topic"] == "交付量/销量":
        v["data_points"] = [
            "Q4交付量418,227辆（11,642 Model S/X + 406,585 Model 3/Y），同比下降16%",
            "2025全年交付约164万辆，同比下降约9%",
            "联邦$7,500 EV税收抵免到期+消费者兴趣减弱导致需求放缓",
            "管理层预期2026年仅温和的整体收入和交付增长",
            "CEO Musk曾在2025Q2末表示2026年将包含'艰难的季度'"
        ]
    elif v["topic"] == "毛利率":
        v["data_points"] = [
            "Q4 GAAP毛利率20.1%（去年同期16.3%），环比改善380个基点",
            "改善归因于更高的平均售价（ASP）和更优产品组合",
            "但定价压力导致毛利率增长不一致，前瞻性盈利预期持续下调",
            "Gross Profit Margin: 2023年18.2%→2024年17.9%→2025年18.0%，基本持平",
            "Operating Margin: 2023年9.2%→2024年7.9%→2025年5.1%，持续恶化"
        ]
    elif v["topic"] == "Robotaxi":
        v["data_points"] = [
            "Robotaxi和AI投资正以极快速度消耗资本",
            "近期回报可见性差，需验证EV交付量企稳或加速",
            "需看到毛利率可持续恢复才能更加看好",
            "2026年资本支出$20B+中大部分用于自动驾驶技术扩展"
        ]
    elif v["topic"] == "能源业务":
        v["data_points"] = [
            "Energy Generation and Storage Q4收入$3.837B，同比增长25%（去年$3.061B）",
            "反映电池存储需求强劲及毛利率表现扩大",
            "全年Services and Other收入同比增18%至$3.371B",
            "能源业务是Tesla少数保持强劲增长的业务线"
        ]
    elif v["topic"] == "估值":
        v["data_points"] = [
            "以2026E EPS $2.03计算，P/E约205倍；以2027E $2.95计算，P/E约141倍",
            "14年年均P/E区间117-245x",
            "P/B 16.9x（历史区间14.1-42.9x）",
            "P/S 14.2x（历史区间6.7-16.8x），接近历史高端",
            "P/CF 91.1x（历史区间33.9-73.5x），超出历史区间",
            "EV/EBITDA 127.9x，低于历史区间136.8-214.1x的低端",
            "Market Cap $1.56T，是GM+Ford之和的11.7倍"
        ]

# Also fill in analyst and institution_en
r0["analyst"] = "Bill Selesky"
r0["institution_en"] = "Argus Research"

print("Report 0 (Argus) updated successfully")
print(f"  chart_insights: {len(r0['chart_insights'])}")
print(f"  risk_factors: {len(r0['risk_factors'])}")
print(f"  catalysts: {len(r0['catalysts'])}")
print(f"  blind_spots: {len(r0['blind_spots'])}")
for v in r0["views"]:
    print(f"  view '{v['topic']}': {len(v['data_points'])} data_points")

# Save intermediate
with open(DATA_PATH, "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\nReport 0 saved to TSLA.json")
