import json

analysis = {
    "ticker": "TSLA",
    "report": {
        "date": "2026-02-02",
        "institution": "Zacks Equity Research",
        "institution_en": "Zacks Equity Research",
        "analyst": "",
        "rating": "中性",
        "previous_rating": "看空",
        "target_price": 452.0,
        "previous_target_price": None,
        "sentiment_score": -0.10,
        "views": [],
        "key_metrics": {
            "revenue_estimate": "2026E: $96,351M; 2027E: $118,734M",
            "eps_estimate": "2026E: $3.20; 2027E: $4.53",
            "growth_rate": "2026E营收增长1.6% YoY; 2026E EPS增长92.8% YoY",
            "margin_estimate": "Q4汽车毛利率17.2%(不含租赁和信贷); 运营利润率5.7%",
            "other": {
                "P/E_F1": "130.33",
                "P/S_TTM": "17.03",
                "PEG_F1": "2.1",
                "P/B_TTM": "19.50",
                "EV/EBITDA": "134.12",
                "debt_to_equity": "0.08",
                "current_ratio": "2.16",
                "free_cash_flow_Q4": "$1.42B",
                "cash_position": "$44.1B",
                "zacks_rank": "4-Sell",
                "style_scores": "VGM:D (Value:F, Growth:C, Momentum:B)"
            }
        },
        "key_assumptions": [
            "EV市场需求持续疲软，竞争加剧导致Tesla美国市场份额降至50%以下",
            "2026年$200亿资本支出将压制近期现金流，但支撑长期AI/自动驾驶转型",
            "Robotaxi 2026上半年扩展至7个新城市，但有意义的收入贡献仍需时间",
            "监管信贷销售持续下降（2025年同比降28%），不再是可靠利润来源",
            "能源存储业务保持强劲增长势头，Megapack 3和Megablock将推动部署量",
            "Model S/X将于2026年Q2停产，产品线聚焦Model 3/Y和Cybertruck"
        ],
        "risk_factors": [
            "EV交付量连续第二年下滑，2025年降幅扩大至8%以上",
            "$200亿资本支出远超历史峰值$11.3B，财务压力显著",
            "美国EV市场份额从2022年63%降至50%以下，竞争持续侵蚀",
            "中国市场面临BYD、NIO、XPeng、Li等本土品牌激烈竞争",
            "监管信贷销售同比下降28%，美国政策变化取消燃油经济性罚款",
            "联邦$7,500 EV税收抵免到期风险",
            "Zacks Rank 4-Sell，短期估值修正压力"
        ],
        "blind_spots": [
            "未详细分析Optimus人形机器人的商业化时间表和潜在市场规模",
            "未讨论SpaceX/xAI与Tesla的潜在协同效应",
            "未评估Tesla保险业务的增长潜力和利润贡献",
            "未分析Tesla在印度等新兴市场的扩张计划",
            "未讨论电池技术（4680电池）的成本下降曲线对毛利率的影响"
        ],
        "catalysts": [
            {
                "event": "Q1 2026财报发布",
                "expected_date": "2026-04-28",
                "importance": "high",
                "related_views": ["交付量/销量", "毛利率", "估值"]
            },
            {
                "event": "Robotaxi扩展至7个新城市",
                "expected_date": "2026-06-30",
                "importance": "high",
                "related_views": ["Robotaxi", "FSD/自动驾驶"]
            },
            {
                "event": "Model S/X停产",
                "expected_date": "2026-06-30",
                "importance": "medium",
                "related_views": ["交付量/销量", "毛利率"]
            },
            {
                "event": "Cybercab量产启动",
                "expected_date": "2026-12-31",
                "importance": "high",
                "related_views": ["Robotaxi", "FSD/自动驾驶"]
            }
        ],
        "chart_insights": [],
        "cross_comparison": {
            "vs_previous_reports": [
                {
                    "compared_with": "tsla-argus-20260130",
                    "topic": "整体评级",
                    "divergence": "minor",
                    "description": "Zacks中性 vs Argus持有，方向一致但Zacks给出明确目标价$452而Argus未给目标价"
                },
                {
                    "compared_with": "tsla-morningstar-20260203",
                    "topic": "目标价",
                    "divergence": "moderate",
                    "description": "Zacks目标价$452 vs Morningstar公允价值$400，分歧13%。Zacks基于16.15X前瞻P/S，Morningstar基于DCF"
                },
                {
                    "compared_with": "tsla-argus-20260130",
                    "topic": "Robotaxi前景",
                    "divergence": "moderate",
                    "description": "Zacks中性看待robotaxi扩展（提供具体7城市名单），Argus则明确看空认为资本消耗过快"
                }
            ],
            "consensus_position": "Zacks处于三份研报的中间位置：比Argus略乐观（从Underperform上调至Neutral），但比Morningstar更谨慎（未给予长期AI/robotaxi高估值）"
        }
    }
}

# Save base
with open('/Users/aibrain/openclaw-workspace-superbrain/Project/antigravity-research/luminescent-hubble/tmp/tsla_report3_analysis.json', 'w') as f:
    json.dump(analysis, f, ensure_ascii=False, indent=2)

print("Base saved. Now adding views and chart_insights...")
