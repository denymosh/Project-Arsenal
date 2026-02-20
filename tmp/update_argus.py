#!/usr/bin/env python3
"""Update TSLA.json reports[0] (Argus Research) with chart_insights, key_metrics, risk_factors, catalysts, blind_spots, and view data_points."""

import json
import os

DATA_PATH = "/Users/aibrain/openclaw-workspace-superbrain/Project/antigravity-research/luminescent-hubble/data/TSLA.json"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

report = data["reports"][0]
assert report["id"] == "tsla-argus-20260130", f"Expected tsla-argus-20260130, got {report['id']}"

# ── 1. chart_insights ──
report["chart_insights"] = [
    {
        "chart_name": "Price & EPS/Revenue Overview (Page 1)",
        "chart_type": "line+bar",
        "source_file": "Argus_TSLA_4Q25_p1.png",
        "description": "第1页综合概览图：包含2024Q1-2027Q4股价走势（含200日均线）、季度/年度EPS柱状图、季度/年度Revenue柱状图，以及Key Statistics面板。股价图显示52周高$498.83/低$214.25，200日均线从~$200上升至~$400。",
        "key_observations": [
            "股价在2025Q4触及52周高点$498.83后回落至$449.06（1月30日收盘），回撤约10%",
            "200日均线从2024年初~$200稳步上升至当前~$400，长期趋势仍向上",
            "EPS呈下降趋势：2024全年$2.29→2025全年$1.67（-27%），但2026E $2.03和2027E $2.95预示反弹",
            "Revenue同样承压：2024 $97.7B→2025 $94.8B（-2.9%），但2026E $105.3B和2027E $122.2B预期恢复增长",
            "季度EPS波动明显：2025年Q1仅$0.27为全年最低，Q3/Q4均为$0.50"
        ],
        "data_not_in_text": [
            "200日均线斜率在2025年下半年明显趋缓，从陡峭上升转为平缓，暗示长期动能减弱",
            "季度Revenue在2025Q3达$28.1B为全年峰值，Q4回落至$24.9B（-11.4%），季节性波动显著",
            "2027E季度EPS呈逐季递增趋势（$0.59→$0.72→$0.82→$0.82），暗示盈利改善预期集中在下半年"
        ],
        "investment_implication": "股价已从高点回撤10%但仍远高于200日均线，技术面尚未破坏。EPS和Revenue的2026-2027E反弹预期是支撑当前估值的关键——若实际数据不及预期，股价可能向200日均线（~$400）回归。"
    },
    {
        "chart_name": "Growth & Valuation Analysis Tables (Page 2)",
        "chart_type": "table",
        "source_file": "Argus_TSLA_4Q25_p2.png",
        "description": "第2页上半部分包含2021-2025年完整的Growth Analysis表格（Revenue/COGS/Gross Profit/SG&A/R&D/Operating Income/Net Income/EPS）、Growth Rates表格和Valuation Analysis表格（P/E/P/S/P/CF的历史高低区间）。",
        "key_observations": [
            "Revenue从2021年$53.8B增长至2023年$96.8B（+80%），但2024-2025年增长停滞（$97.7B→$94.8B）",
            "Operating Income从2022年峰值$13.8B暴跌至2025年$4.8B（-65%），反映严重的利润率压缩",
            "R&D支出从2021年$2.6B飙升至2025年$6.4B（+147%），是利润下降的重要推手",
            "2025年P/E区间461.9-198.4，即使在52周低点时P/E仍高达198倍",
            "EPS增长率2025年为-47.1%，连续两年大幅负增长（2024年-52.6%）"
        ],
        "data_not_in_text": [
            "SG&A从2022年$3.9B增至2025年$5.8B（+49%），增速远超Revenue，管理费用控制不力",
            "税率从2021年11%飙升至2025年27%，税负加重进一步侵蚀净利润",
            "2023年Net Income $15.0B包含大额税收优惠（税率为负），剔除后实际盈利能力远低于表面数字",
            "Sustainable Growth Rate从2022年33.4%骤降至2025年6.8%，反映内生增长动力严重不足"
        ],
        "investment_implication": "Growth表格揭示Tesla正经历'增长陷阱'：Revenue停滞+R&D/SG&A飙升=Operating Income暴跌。Sustainable Growth Rate仅6.8%与P/E 200+的估值严重不匹配。除非AI/Robotaxi投资在2027年后开始产生回报，否则当前估值难以维持。"
    },
    {
        "chart_name": "Financial Strength & Risk Analysis Tables (Page 2)",
        "chart_type": "table",
        "source_file": "Argus_TSLA_4Q25_p2.png",
        "description": "第2页下半部分包含2023-2025年Financial Strength表格（Cash/Working Capital/Current Ratio/Debt Ratios）、Ratios表格（Margins/ROA/ROE）和Risk Analysis表格（Cash Cycle/CF-CapEx/Interest Coverage）。",
        "key_observations": [
            "现金从2023年$16.4B微增至2025年$16.5B，基本持平，但Working Capital从$20.9B增至$36.9B（+77%）",
            "LT Debt/Equity从2023年10.4%升至2025年14.8%，杠杆率小幅上升",
            "Net Margin从2023年15.5%（含税收优惠）骤降至2025年4.0%，盈利能力大幅恶化",
            "ROE从2023年27.9%降至2025年4.9%，资本回报率严重下滑",
            "Operating Income/Interest Expense从2023年64.9倍降至2025年16.6倍，利息覆盖能力下降但仍充裕"
        ],
        "data_not_in_text": [
            "Cash Flow/Cap Ex从2023年1.5倍升至2025年1.7倍，说明尽管盈利下降，经营现金流仍能覆盖资本支出",
            "Cash Cycle从2023年4.8天延长至2025年13.9天，运营效率下降，资金周转变慢",
            "Gross Margin在2023-2025年几乎持平（18.2%→18.0%），说明毛利率已触底企稳，利润下降主要来自费用端"
        ],
        "investment_implication": "财务健康度尚可但趋势恶化。ROE从28%降至5%是最令人担忧的信号。好消息是毛利率已企稳在18%，且现金流仍能覆盖CapEx。但2026年$200亿CapEx计划将严重考验资产负债表——Cash Flow/Cap Ex比率可能降至1.0以下。"
    },
    {
        "chart_name": "Peer & Industry Scatterplot (Page 3)",
        "chart_type": "scatter",
        "source_file": "Argus_TSLA_4Q25_p3.png",
        "description": "第3页散点图以5年增长率（X轴）和P/E（Y轴）展示TSLA与同行的定位。TSLA位于右上角（高增长高P/E），GM和Ford位于左下角（低增长低P/E）。配合详细的Peer比较表格。",
        "key_observations": [
            "TSLA 5年增长率105%、P/E 205.2倍，远离GM（7%增长、P/E 7.2）和Ford（4%增长、P/E 13.0）",
            "TSLA市值$1.56T是GM（$78B）的20倍、Ford（$55B）的28倍，但Net Margin仅4.0%",
            "GM和Ford均获BUY评级，而TSLA为HOLD，Argus认为传统车企更具投资价值",
            "TSLA 1年EPS增长45.3%高于GM（10.0%）和Ford（31.5%），但这是从低基数反弹"
        ],
        "data_not_in_text": [
            "散点图中TSLA与GM/Ford的距离极远，视觉上几乎不在同一象限，说明市场已将TSLA视为完全不同类型的公司",
            "Ford的Net Margin 2.5%与TSLA的4.0%差距不大，但P/E差距达15.8倍（205.2 vs 13.0），溢价完全来自增长预期"
        ],
        "investment_implication": "散点图直观展示了TSLA的'估值孤岛'地位——它既不是传统车企（估值太高），也不完全是科技公司（利润率太低）。如果市场重新将TSLA归类为车企，估值可能向GM/Ford靠拢（P/E 7-13倍），意味着90%+的下行空间。"
    },
    {
        "chart_name": "Valuation Comparison Bar Charts (Page 3)",
        "chart_type": "bar",
        "source_file": "Argus_TSLA_4Q25_p3.png",
        "description": "第3页右侧的估值对比条形图，将TSLA在P/E、P/S、P/B、PEG、5年增长率、Debt/Capital六个维度上与Market和Sector进行1-5评分对比（1=最Value，5=最Growth）。",
        "key_observations": [
            "TSLA在P/E、P/S、P/B、5年增长率上均获5分（最Growth），无论对比Market还是Sector",
            "Debt/Capital获1分（最Value），说明Tesla杠杆率远低于市场和行业平均",
            "PEG评分为Market 2分、Sector 3分，是唯一不在极端值的指标",
            "六个维度中五个为极端值（5或1），说明TSLA在几乎所有估值维度上都是异常值"
        ],
        "data_not_in_text": [
            "PEG评分2-3（而非5）暗示TSLA的增长率部分抵消了高P/E，但仍偏贵",
            "Debt/Capital获1分（最低杠杆）与P/E获5分（最高估值）的组合，说明TSLA的高估值并非由杠杆驱动，而是纯粹的增长溢价"
        ],
        "investment_implication": "TSLA在Argus估值框架中是极端的Growth股——几乎所有估值指标都处于最高档。唯一的'Value'特征是低杠杆。这意味着TSLA的投资逻辑完全依赖增长兑现，任何增长放缓都将导致估值重估。PEG 2-3暗示即使考虑增长，估值仍偏高。"
    }
]

# ── 2. key_metrics ──
report["key_metrics"] = {
    "revenue_estimate": "$105.3B (FY2026E), $122.2B (FY2027E)",
    "eps_estimate": "$2.03 (FY2026E), $2.95 (FY2027E)",
    "growth_rate": "-2.9% Revenue YoY (2025), 21.56% 1yr EPS Growth Forecast, 105% 5yr EPS Growth Forecast",
    "margin_estimate": "18.0% Gross Margin, 5.1% Operating Margin, 4.0% Net Margin (2025)",
    "valuation_multiple": "P/E 205.2x, P/S 16.48x, P/B 16.86x",
    "other": {
        "beta": "1.64",
        "debt_capital": "9.2%",
        "cash": "$16.5B",
        "market_cap": "$1.56T",
        "current_ratio": "2.16",
        "ROE": "7.2%",
        "ROA": "2.9%",
        "working_capital": "$36.9B",
        "LT_debt_equity": "14.8%",
        "institutional_ownership": "49.08%",
        "financial_strength_rating": "Medium",
        "credit_rating": "Baa3/stable (Moody's), BBB/stable (S&P)",
        "total_debt": "$8.376B",
        "cash_equivalents": "$44.059B",
        "book_value_per_share": "$24.70"
    }
}

# ── 3. risk_factors ──
report["risk_factors"] = [
    "核心EV需求放缓：联邦$7,500税收抵免到期+消费者兴趣减弱，Q4交付量同比下降16%至418,227辆",
    "竞争加剧：GM、Ford等传统车企加速EV转型，Tesla美国EV市场份额约50%面临持续侵蚀",
    "盈利能力恶化：2025年EPS $1.08同比下降47.1%，Operating Income从$13.8B(2022)降至$4.8B(2025)，降幅65%",
    "估值依赖未经验证的长期赌注：Robotaxi、AI、Optimus等业务正以极快速度消耗资本（2026年CapEx>$200亿），但近期回报可见性差",
    "定价压力导致毛利率增长不一致：尽管Q4毛利率改善至20.1%，但前瞻性盈利预期持续下调（2026E EPS从$2.26下调至$2.03）",
    "宏观经济风险：全球经济疲软、消费者偏好变化和支出模式改变可能进一步抑制EV需求",
    "原材料和零部件成本上升风险：更高的关税成本和更高的单车平均成本已在Q4财报中体现",
    "制造中断风险：供应链问题可能影响生产和交付节奏",
    "CEO Musk多重角色风险：同时担任SpaceX CEO和SolarCity非执行主席，精力分散可能影响Tesla运营"
]

# ── 4. catalysts ──
report["catalysts"] = [
    {
        "event": "2026年重资本支出计划启动（>$200亿 vs 2025年$90亿）",
        "expected_date": "2026-Q1",
        "importance": "high",
        "related_views": ["FSD/自动驾驶", "Robotaxi"]
    },
    {
        "event": "Robotaxi和自动驾驶技术规模化推进",
        "expected_date": "2026-H1",
        "importance": "high",
        "related_views": ["FSD/自动驾驶", "Robotaxi"]
    },
    {
        "event": "Optimus人形机器人量产启动",
        "expected_date": "2026-H2",
        "importance": "medium",
        "related_views": ["FSD/自动驾驶"]
    },
    {
        "event": "EV交付量企稳或加速（Argus升级条件）",
        "expected_date": "2026-Q2",
        "importance": "high",
        "related_views": ["交付量/销量", "毛利率"]
    },
    {
        "event": "毛利率可持续恢复确认（Argus升级条件）",
        "expected_date": "2026-Q2",
        "importance": "high",
        "related_views": ["毛利率", "估值"]
    },
    {
        "event": "AI和能源业务持续增长验证",
        "expected_date": "2026-Q2",
        "importance": "medium",
        "related_views": ["能源业务"]
    }
]

# ── 5. blind_spots ──
report["blind_spots"] = [
    "未提供目标价：Argus对TSLA未设定目标价，投资者缺乏明确的估值锚点，难以评估上行/下行空间",
    "未量化AI/Robotaxi/Optimus的潜在收入贡献：仅定性描述为'未经验证的长期赌注'，未建模这些业务在不同情景下的财务影响",
    "未讨论中国市场竞争格局：BYD等本土品牌对Tesla全球交付量的威胁未被提及，而中国是Tesla第二大市场",
    "未分析能源业务的独立估值：能源发电和存储Q4收入$38.4亿同比增25%，但报告未评估该业务的独立价值或对整体估值的贡献",
    "未评估Musk政治活动对品牌和销量的影响：Musk近期的政治参与可能在美国和欧洲市场造成消费者流失，报告完全未提及",
    "未讨论$7,500联邦EV税收抵免到期后的具体影响建模：仅提及'政府激励到期'但未量化对交付量和定价的影响"
]

# ── 6. views data_points ──
# View 0: FSD/自动驾驶
report["views"][0]["data_points"] = [
    "2026年资本支出计划>$200亿（2025年仅$90亿），主要用于自动驾驶、Robotaxi和Optimus扩产",
    "管理层在4Q25电话会（1月28日）强调将持续向AI和能源增长转型",
    "Argus认为估值高度依赖未经验证的长期赌注，近期回报可见性差",
    "需要看到EV交付量企稳/加速+毛利率可持续恢复，才能对股票更加看好",
    "5年EPS增长预测105%，但主要依赖AI/自动驾驶业务的长期兑现"
]

# View 1: 交付量/销量
report["views"][1]["data_points"] = [
    "Q4交付418,227辆（Model S/X 11,642辆 + Model 3/Y 406,585辆），同比下降16%",
    "Q4总收入下降3%至$24.901B，汽车部门收入下降11%至$17.693B",
    "2025全年调整后净利润$5.858B（$1.67/股），2024年为$7.960B（$2.29/股）",
    "管理层预期2026年温和的整体收入和交付增长",
    "Argus下调2026E EPS至$2.03（原$2.26），反映更慢的车辆销售和利润率压力",
    "Argus首次给出2027E EPS $2.95，隐含更高的收入和利润增长",
    "服务及其他收入增长18%至$3.371B",
    "CEO Musk在2025年Q2末曾预警2026年将包含一些'艰难的季度'"
]

# View 2: 毛利率
report["views"][2]["data_points"] = [
    "Q4 GAAP毛利率20.1%（去年同期16.3%），环比改善380个基点",
    "毛利率改善归因于更高的平均售价（ASP）和更优产品组合",
    "2025全年Gross Margin 18.0%（2024年17.9%，2023年18.2%），基本持平",
    "Operating Margin从2023年9.2%降至2025年5.1%，主要因R&D从$4.0B升至$6.4B、SG&A从$4.8B升至$5.8B",
    "Net Margin从2023年15.5%（含税收优惠）降至2025年4.0%",
    "Argus认为定价压力导致毛利率增长不一致，前瞻性盈利预期持续下调"
]

# View 3: Robotaxi
report["views"][3]["data_points"] = [
    "管理层在4Q25电话会强调2026年>$200亿CapEx中相当部分用于Robotaxi规模化",
    "Argus认为Robotaxi和AI投资正以极快速度消耗资本，近期回报可见性差",
    "在验证EV交付量企稳或加速、毛利率可持续恢复之前，Argus无法更加看好该股",
    "Argus将Q4业绩视为'异常值'（anomaly），不认为代表趋势性改善"
]

# View 4: 能源业务
report["views"][4]["data_points"] = [
    "Q4能源发电和存储收入$3.837B，同比增长25%（去年同期$3.061B）",
    "能源业务增长反映电池存储需求强劲及毛利率表现扩大",
    "服务及其他收入Q4增长18%至$3.371B",
    "能源业务是Q4财报中为数不多的亮点，部分抵消了汽车业务的疲软"
]

# View 5: 估值
report["views"][5]["data_points"] = [
    "以2026E EPS $2.03计算，当前P/E约205倍；以2027E EPS $2.95计算，P/E约141倍",
    "14年年均P/E区间117-245倍，当前205倍处于区间中上部",
    "P/B 16.9倍（历史区间14.1-42.9），P/S 14.2倍（历史区间6.7-16.8），P/CF 91.1倍（历史区间33.9-73.5）",
    "P/EBITDA 127.9倍，低于历史区间低端136.8-214.1",
    "52周价格区间$214.25-$498.83，当前交易价高于中点",
    "2025年P/E区间461.9-198.4，P/S区间18.6-8.0，Price/Cash Flow区间111.6-47.9",
    "Argus使用同行比较、历史倍数和股息折现模型进行估值"
]

# ── Write back ──
with open(DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# ── Verify ──
with open(DATA_PATH, "r", encoding="utf-8") as f:
    verify = json.load(f)

r = verify["reports"][0]
print(f"chart_insights count: {len(r['chart_insights'])}")
print(f"key_metrics: {r['key_metrics'] is not None}")
print(f"risk_factors count: {len(r['risk_factors'])}")
print(f"catalysts count: {len(r['catalysts'])}")
print(f"blind_spots count: {len(r['blind_spots'])}")
for i, v in enumerate(r["views"]):
    print(f"  view[{i}] '{v['topic']}' data_points: {len(v['data_points'])}")

print("\n✅ All fields updated successfully for reports[0] (Argus Research)")
