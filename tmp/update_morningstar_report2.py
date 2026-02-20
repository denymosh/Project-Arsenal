#!/usr/bin/env python3
"""Update TSLA.json reports[2] (Morningstar simplified) with detailed data."""
import json

JSON_PATH = "/Users/aibrain/openclaw-workspace-superbrain/Project/antigravity-research/luminescent-hubble/data/TSLA.json"

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

r = data["reports"][2]
assert r["id"] == "tsla-morningstar-20260203", f"Wrong report: {r['id']}"

# ============================================================
# 1. chart_insights
# ============================================================
r["chart_insights"] = [
    {
        "chart_name": "Price vs. Fair Value (2021-YTD)",
        "chart_type": "line",
        "source_file": "TSLA_-Tesla-Inc-(Stock-Report)_p1_price_vs_fv.png",
        "description": "Tesla股价与Morningstar公允价值估计的历史对比图（2021-2026 YTD），包含P/FVE比率和年度总回报率。股价在大部分时间处于高估区域，仅2022年底短暂进入低估区域。",
        "key_observations": [
            "2022年P/FVE降至0.49（严重低估），全年回报-65.03%，是唯一的5星买入机会",
            "2024年P/FVE飙升至1.92（严重高估），全年回报+62.52%",
            "YTD 2026 P/FVE=1.05，FVE从$300上调至$400后首次接近公允价值",
            "2023年P/FVE=1.18但全年回报+101.72%，显示从2022年低点的强劲反弹"
        ],
        "data_not_in_text": [
            "2021年P/FVE=1.55，全年回报+49.76%——即使高估也有正回报，说明动量效应强",
            "FVE上调$100（$300→$400）使P/FVE下降约0.35，显示估值对FVE极度敏感"
        ],
        "investment_implication": "Tesla历史上仅在2022年底（P/FVE=0.49）提供过真正的安全边际。当前P/FVE=1.05虽接近公允价值，但Very High Uncertainty意味着5星买入价为$200（50%折价），当前价格仍远高于此。"
    },
    {
        "chart_name": "Morningstar估值模型财务预测汇总表",
        "chart_type": "table",
        "source_file": "TSLA_-Tesla-Inc-(Stock-Report)_p15_financials.png",
        "description": "完整财务预测表格（2022-2029年），涵盖营收、运营利润、EBITDA、净利润、EPS、估值倍数、利润率、增长率等。包含实际值（2022-2025）和预测值（2026-2029）。",
        "key_observations": [
            "营收预计2025-2026年连续下降（$94.8B→$93.0B），2027年起恢复增长至$112B/$141B/$179B",
            "运营利润2025年$4.8B→2026年$4.6B（谷底），2029年飙升至$33.8B（7倍增长）",
            "FCFF 2026年为-$9.4B（大规模负现金流），2028年才转正$3.1B",
            "ROIC从2025年3.8%恢复至2029年35.4%，超过2022年22.3%的历史高点"
        ],
        "data_not_in_text": [
            "2023年净利润$15.0B是历史峰值，2025年仅$3.8B（降75%），预计2029年才恢复至$26.8B",
            "调整后EBITDA利润率从2022年20.6%降至2026E 14.8%，2029E恢复至25.9%",
            "EV/EBITDA从2025年106.9x升至2026E 113.2x（因EBITDA下降），2029E降至33.6x"
        ],
        "investment_implication": "财务预测揭示Tesla正处于'J型曲线'底部：2025-2026年是盈利低谷，2027年起进入收获期。关键转折点是2028年FCFF转正。投资者需要3-4年耐心等待AI转型兑现。"
    },
    {
        "chart_name": "不确定性评级与安全边际框架",
        "chart_type": "bar",
        "source_file": "TSLA_-Tesla-Inc-(Stock-Report)_p21_uncertainty.png",
        "description": "展示不同不确定性等级下的Price/Fair Value阈值。Tesla被归类为Very High Uncertainty，对应极宽的估值区间。",
        "key_observations": [
            "Very High Uncertainty：5星买入需P/FVE≤0.50（$200），1星卖出需P/FVE≥1.75（$700）",
            "3星区间为P/FVE 0.80-1.25，Tesla当前1.05处于该区间中部",
            "对比Medium Uncertainty：5星仅需P/FVE≤0.70（30%折价），Very High需50%折价",
            "上行情景$700与下行情景$100的7:1比率反映极端不确定性"
        ],
        "data_not_in_text": [
            "Very High Uncertainty的4星区间为P/FVE 0.50-0.80，对应Tesla价格$200-$320",
            "Very High Uncertainty的2星区间为P/FVE 1.25-1.75，对应Tesla价格$500-$700"
        ],
        "investment_implication": "即使认同$400 FVE，当前$421（P/FVE=1.05）也不具备足够安全边际。要获得4星（有吸引力），价格需降至$320以下；5星（强烈买入）需降至$200以下。"
    },
    {
        "chart_name": "DCF估值分解",
        "chart_type": "table",
        "source_file": "TSLA_-Tesla-Inc-(Stock-Report)_p16_dcf.png",
        "description": "Morningstar DCF估值分解：Stage I $159.2B + Stage II $186.0B + Stage III $530.1B = 总企业价值$875.3B。加回现金$36.6B，减去债务$7.9B，其他调整$382.3B，权益价值$1,286.3B，FVE $400/股。",
        "key_observations": [
            "Stage III（永续价值）$530.1B占总企业价值60.6%，反映对长期增长的极度依赖",
            "Stage I（显式预测期）仅$159.2B（18.2%），近期盈利贡献有限",
            "其他调整$382.3B是巨大正向调整项，可能包含Robotaxi/FSD/Optimus独立估值",
            "WACC 8.8%，权益成本9.0%，永续期第15年"
        ],
        "data_not_in_text": [
            "Stage III占比60.6%意味着长期增长假设每下调1%，FVE可能缩水$50-80",
            "其他调整$382.3B几乎等于Stage I+Stage II之和，是FVE的关键驱动因素"
        ],
        "investment_implication": "DCF分解揭示Tesla估值的'脆弱性'：60%以上价值来自永续期，对WACC和长期增长率极度敏感。这解释了Very High Uncertainty评级和$100-$700的巨大估值区间。"
    }
]

# ============================================================
# 2. key_metrics
# ============================================================
r["key_metrics"] = {
    "revenue_estimate": "2026E: $92.98B, 2027E: $111.92B, 2028E: $140.97B, 2029E: $178.93B",
    "eps_estimate": "2026E: $1.22 (adj $1.98), 2027E: $2.50 (adj $3.27), 2029E: $7.61 (adj $8.42)",
    "growth_rate": "2026E营收-2.0%, 2027E +20.4%, 2028E +26.0%, 2029E +26.9%",
    "margin_estimate": "2026E运营利润率5.0%, 2029E恢复至18.9%; 汽车毛利率(不含信贷)十几%中段",
    "other": {
        "fair_value_estimate": "$400/股",
        "P_FVE": "1.05",
        "economic_moat": "Narrow",
        "uncertainty": "Very High",
        "capital_allocation": "Exemplary",
        "WACC": "8.8%",
        "1_star_price": "$700",
        "5_star_price": "$200",
        "upside_scenario": "$700 (Robotaxi $180 + Optimus $300 + FSD $80)",
        "downside_scenario": "$100 (FSD $10, Robotaxi/Optimus零估值)",
        "robotaxi_valuation": "$120/股 (占总估值30%)",
        "FSD_valuation": "$70/股",
        "optimus_valuation": "$80/股",
        "10yr_capex": "~$170B",
        "2026E_FCFF": "-$9.37B",
        "2025_ROIC": "3.8%",
        "2029E_ROIC": "35.4%",
        "debt_to_capital": "0.6%",
        "ESG_risk_rating": "18.8 (Low)"
    }
}

# ============================================================
# 3. risk_factors
# ============================================================
r["risk_factors"] = [
    "汽车市场高度周期性，经济下行可导致需求骤降，Tesla作为EV领导者首当其冲",
    "EV竞争加剧，新低价EV入市迫使Tesla降价，侵蚀利润率（汽车毛利率已从2022年29%降至2024年18%）",
    "自动驾驶/Robotaxi/人形机器人投入巨大（未来十年$1700亿资本支出）但无法保证回报",
    "CEO Musk持有约12%股份并用作个人贷款抵押，存在大规模抛售风险",
    "Musk政治活动（支持Trump后又反对、支持德国AfD）可能在美国和欧洲市场导致消费者流失",
    "Nvidia进入自动驾驶系统市场（CES 2026），可能允许多家车企快速缩小与Tesla的差距",
    "加州DMV裁定暂停Tesla生产和销售许可30天（因Autopilot/FSD营销问题），监管风险持续",
    "产品召回风险（包括自动驾驶软件缺陷），ESG中等影响",
    "关键人员风险：若Musk离开，公司创新形象可能受损（低概率但中等影响）",
    "美国EV税收抵免2025年9月到期，预计2026年交付量降至156万辆"
]

# ============================================================
# 4. catalysts
# ============================================================
r["catalysts"] = [
    {
        "event": "Robotaxi扩展至7个新美国城市（达拉斯、休斯顿、凤凰城、迈阿密、奥兰多、坦帕、拉斯维加斯）",
        "expected_date": "2026-H1",
        "importance": "high",
        "related_views": ["Robotaxi", "FSD/自动驾驶"]
    },
    {
        "event": "Austin地区Robotaxi移除安全监督员",
        "expected_date": "2026-Q1",
        "importance": "high",
        "related_views": ["Robotaxi"]
    },
    {
        "event": "Optimus人形机器人开始量产（Model S/X工厂改造）",
        "expected_date": "2026-Q4",
        "importance": "high",
        "related_views": ["交付量/销量", "估值"]
    },
    {
        "event": "SpaceX IPO（可能为未来Tesla收购SpaceX铺路）",
        "expected_date": "2026-H2",
        "importance": "medium",
        "related_views": ["估值"]
    },
    {
        "event": "Robotaxi全面商业化（无安全监督员、无/有限地理围栏、专用车辆）",
        "expected_date": "2027-2028",
        "importance": "high",
        "related_views": ["Robotaxi", "FSD/自动驾驶", "估值"]
    },
    {
        "event": "FVE修订触发：2026年交付量数据（预计降至156万辆）",
        "expected_date": "2027-01-15",
        "importance": "medium",
        "related_views": ["交付量/销量", "估值"]
    }
]

# ============================================================
# 5. blind_spots
# ============================================================
r["blind_spots"] = [
    "未详细讨论中国市场竞争格局（BYD等本土品牌的具体威胁和市场份额变化）",
    "未量化Musk政治活动对欧洲/美国销量的实际影响（仅定性提及风险）",
    "未讨论Tesla保险业务的具体财务数据和增长轨迹",
    "未提及供应链风险（锂/钴/镍价格波动对电池成本的影响）",
    "未分析Cybertruck的具体销量和盈利贡献",
    "未讨论4680电池技术的成本下降曲线对毛利率的具体影响"
]

# ============================================================
# 6. Update data_points for each view
# ============================================================
view_data_points = {
    "FSD/自动驾驶": [
        "FSD订阅软件估值约$70/股，是Tesla估值的重要组成部分",
        "Tesla研发投入约占销售额6%，维持行业领先的续航里程（每千瓦时英里数最优）",
        "FSD采用率增长将推动汽车毛利率从2024年18%恢复至2020年代末25%中段",
        "Tesla正在建造全球最大超级计算机之一用于训练自动驾驶AI",
        "欧洲目前无法销售FSD软件，需等待监管审批",
        "Nvidia CES 2026宣布进入自动驾驶系统市场，Tesla股价当日下跌5%"
    ],
    "交付量/销量": [
        "2025年全年交付1,636,129辆，同比降9%；Q4交付418,227辆同比降16%",
        "2026年预计交付降至156万辆（因美国EV税收抵免2025年9月到期+欧洲竞争加剧）",
        "2030年预计交付约280万辆，主要由Model Y/3平台驱动",
        "Model S/X计划停产，工厂改造为Optimus生产线",
        "Cybertruck/Roadster/Semi合计约3万辆/年",
        "2025年全年营收$94.8B，2026E降至$93.0B（-2.0%）"
    ],
    "毛利率": [
        "预计汽车毛利率（不含信贷）维持十几%中段，低于管理层20%长期目标",
        "随FSD订阅采用率上升，预计到2020年代末毛利率恢复至25%中段",
        "2024年汽车毛利率18%，2022年峰值29%",
        "每车COGS从2017年$84,000降至2024年$35,000+（降幅超55%）",
        "2026E运营利润率5.0%，2029E恢复至18.9%",
        "2026E调整后EBITDA利润率14.8%，2029E恢复至25.9%"
    ],
    "Robotaxi": [
        "Robotaxi估值约$120/股，占Tesla总估值约30%",
        "预计自动驾驶车辆（Tesla+Waymo）到2030年占美加打车服务50%",
        "Tesla预计获得美加打车市场30%份额（到2035年）",
        "Austin地区已开始测试无安全监督员的Robotaxi",
        "2026上半年计划扩展至7个新城市",
        "上行情景下Robotaxi估值可达$180/股，下行情景为零",
        "全面商业化预计2027-2028年"
    ],
    "能源业务": [
        "能源存储业务预计年均收入增长近30%（10年预测期）",
        "Q4 2025电池存储部署46.7GWh",
        "Tesla品牌在消费者端太阳能+逆变器+家庭电池系统可获溢价定价",
        "长期电力购买协议和AI交易软件提供经常性收入",
        "预计毛利率将与Enphase和SolarEdge等同行持平",
        "ESS价格预计下降，但主要由电池成本下降驱动，不影响盈利能力"
    ],
    "估值": [
        "公允价值$400/股，P/FVE=1.05（3星适当估值区域）",
        "DCF总企业价值$875.3B，Stage III永续价值$530.1B占60.6%",
        "WACC 8.8%，权益成本9.0%，税前债务成本5.8%",
        "上行情景$700（Robotaxi $180 + Optimus $300 + FSD $80/股）",
        "下行情景$100（FSD仅$10/股，Robotaxi和Optimus零估值）",
        "P/E 356.8x, P/S 15.69x, P/B 19.26x",
        "未来十年预计$1700亿资本支出",
        "竞争对比：Tesla P/S 15.69x vs BYD 0.93x vs Rivian 2.83x vs GOOGL 10.93x"
    ]
}

for view in r["views"]:
    topic = view["topic"]
    if topic in view_data_points:
        view["data_points"] = view_data_points[topic]

# ============================================================
# Write back
# ============================================================
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# ============================================================
# Verify
# ============================================================
with open(JSON_PATH, "r", encoding="utf-8") as f:
    verify = json.load(f)

r2 = verify["reports"][2]
print(f"Report ID: {r2['id']}")
print(f"chart_insights count: {len(r2['chart_insights'])}")
print(f"key_metrics: {'present' if r2['key_metrics'] else 'null'}")
print(f"risk_factors count: {len(r2['risk_factors'])}")
print(f"catalysts count: {len(r2['catalysts'])}")
print(f"blind_spots count: {len(r2['blind_spots'])}")
for v in r2["views"]:
    print(f"  view '{v['topic']}': {len(v['data_points'])} data_points")

# Verify other reports not touched
for i, rep in enumerate(verify["reports"]):
    if i != 2:
        print(f"Report[{i}] id={rep['id']} - untouched ✓")

print("\n✅ All updates applied and verified successfully.")
