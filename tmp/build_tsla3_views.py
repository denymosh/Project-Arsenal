import json

path = '/Users/aibrain/openclaw-workspace-superbrain/Project/antigravity-research/luminescent-hubble/tmp/tsla_report3_analysis.json'
with open(path, 'r') as f:
    data = json.load(f)

views = [
    {
        "topic": "交付量/销量",
        "stance": "bearish",
        "confidence": "high",
        "summary": "2025年交付量连续第二年同比下滑，降幅从2024年的1%扩大至8%以上。Q4交付418,227辆同比降16%，低于Zacks预期的448,384辆。美国EV市场份额从2022年63%降至50%以下。Model S/X将于2026年Q2停产。管理层仅预期温和增长。",
        "data_points": [
            "Q4交付量418,227辆，同比下降16%，低于Zacks预期448,384辆",
            "Q4生产434,358辆（Model 3/Y 422,652辆 + 其他11,706辆），同比降5%",
            "2025全年交付约164万辆（Model 3/Y 158万 + 其他50,850辆），同比降8%+",
            "美国EV市场份额从2020年约80%降至2022年63%再降至目前50%以下",
            "Q4汽车收入$177亿，同比下降11%，低于Zacks预期$193亿",
            "Model S/X计划2026年Q2停产",
            "2025全年营收$94,827M（Q1 $19,335M + Q2 $22,496M + Q3 $28,095M + Q4 $24,901M）"
        ],
        "predictions": [
            {
                "metric": "2026年全年营收",
                "predicted_value": "$96,351M",
                "deadline": "2027-01-31",
                "comparison_to_consensus": "inline"
            },
            {
                "metric": "2026年Q1营收",
                "predicted_value": "$21,045M",
                "deadline": "2026-04-30",
                "comparison_to_consensus": "inline"
            },
            {
                "metric": "2027年全年营收",
                "predicted_value": "$118,734M",
                "deadline": "2028-01-31",
                "comparison_to_consensus": "inline"
            }
        ]
    },
    {
        "topic": "毛利率",
        "stance": "neutral",
        "confidence": "medium",
        "summary": "Q4汽车毛利率（不含租赁和监管信贷）17.2%，高于去年同期12.8%，环比改善显著。但运营利润率5.7%同比下降50个基点。监管信贷销售同比下降28%，这一曾经支撑盈利的收入源正在萎缩。定价压力和竞争加剧使毛利率前景不确定。",
        "data_points": [
            "Q4汽车毛利率（不含租赁和信贷）17.2%，去年同期12.8%，改善440个基点",
            "Q4运营利润率5.7%，同比下降50个基点，但优于Zacks预期5.3%",
            "Q4监管信贷销售$5.42亿，同比下降21.7%",
            "2025全年监管信贷销售同比下降28%",
            "净利润率TTM仅4.00%，ROE仅4.86%",
            "Q4 EPS $0.50，优于预期$0.45但低于去年同期$0.73"
        ],
        "predictions": [
            {
                "metric": "2026年全年EPS",
                "predicted_value": "$3.20",
                "deadline": "2027-01-31",
                "comparison_to_consensus": "inline"
            },
            {
                "metric": "2026年Q1 EPS",
                "predicted_value": "$0.61",
                "deadline": "2026-04-30",
                "comparison_to_consensus": "inline"
            },
            {
                "metric": "2027年全年EPS",
                "predicted_value": "$4.53",
                "deadline": "2028-01-31",
                "comparison_to_consensus": "inline"
            }
        ]
    },
    {
        "topic": "FSD/自动驾驶",
        "stance": "neutral",
        "confidence": "medium",
        "summary": "Tesla正用端到端AI模型升级FSD（Supervised），在Austin和加州湾区测试robotaxi。正开发定制AI推理芯片，目标2027-2028年量产。Cybercab和Optimus预计2026年量产。$200亿资本支出主要投向AI/自动驾驶/机器人，加强长期叙事但有意义的贡献仍需时间。",
        "data_points": [
            "2026年资本支出计划约$200亿，远超2025年约$85亿和2024年峰值$113亿",
            "FSD（Supervised）正在用端到端AI模型升级",
            "定制AI推理芯片目标2027-2028年量产",
            "Cybercab（两座自动驾驶车）预计2026年量产",
            "Optimus人形机器人正在安装第一代生产线，准备量产",
            "Q4资本支出$23.9亿"
        ],
        "predictions": [
            {
                "metric": "AI推理芯片量产",
                "predicted_value": "2027-2028年",
                "deadline": "2028-12-31",
                "comparison_to_consensus": "inline"
            },
            {
                "metric": "2026年资本支出",
                "predicted_value": "约$200亿",
                "deadline": "2027-01-31",
                "comparison_to_consensus": "inline"
            }
        ]
    },
    {
        "topic": "Robotaxi",
        "stance": "neutral",
        "confidence": "medium",
        "summary": "Robotaxi服务已在Austin和加州湾区运营，预计2026上半年扩展至7个新城市（达拉斯、休斯顿、凤凰城、迈阿密、奥兰多、坦帕、拉斯维加斯）。公司认为在robotaxi方面具有强大的成本和规模优势。但有意义的收入贡献可能需要时间。",
        "data_points": [
            "Robotaxi已在Austin和加州湾区进行早期无人驾驶测试",
            "2026上半年计划扩展至7个新城市：达拉斯、休斯顿、凤凰城、迈阿密、奥兰多、坦帕、拉斯维加斯",
            "Tesla认为自身在robotaxi领域具有强大的成本和规模优势",
            "Cybercab两座自动驾驶车预计2026年量产",
            "$200亿资本支出中相当部分用于自动驾驶基础设施"
        ],
        "predictions": [
            {
                "metric": "Robotaxi新城市扩展",
                "predicted_value": "7个新城市",
                "deadline": "2026-06-30",
                "comparison_to_consensus": "inline"
            }
        ]
    },
    {
        "topic": "能源业务",
        "stance": "bullish",
        "confidence": "high",
        "summary": "能源发电和存储业务是Tesla最亮眼的板块。Q4收入$38.4亿同比增25%，能源存储部署14.2GWh。过去三年储能部署CAGR达168%。Megapack 3和Megablock即将投产。超充网络持续扩展至77,682个连接器，NACS标准被Ford、GM、Mercedes等采用。",
        "data_points": [
            "Q4能源发电和存储收入$38.4亿，同比增长25%，超Zacks预期$34亿",
            "Q4能源存储部署14.2GWh",
            "过去三年能源存储部署CAGR达168%",
            "Megapack 3和Megablock即将投产以满足需求增长",
            "超充网络Q4末达77,682个连接器（超77,000个）",
            "Ford、GM、Mercedes等已采用Tesla NACS充电标准",
            "Q4服务及其他收入$34亿，同比增18%"
        ],
        "predictions": []
    },
    {
        "topic": "估值",
        "stance": "bearish",
        "confidence": "high",
        "summary": "当前P/S 15.38X远高于行业3.4X和S&P 500的5.62X。5年P/S中位数仅8.21X。P/E TTM 257.7X，P/E F1 130.33X。Value Style Score F（最差）。Zacks目标价$452基于16.15X前瞻12个月营收。Zacks Rank 4-Sell，EPS预期持续下调（F1 4周下调6.2%，12周下调12.2%）。",
        "data_points": [
            "P/S F12M: 15.38X vs 行业3.4X vs S&P 500 5.62X",
            "P/S 5年范围: 3.03X-23.37X，中位数8.21X",
            "EV/Sales TTM: 16.57X vs 行业3.41X",
            "P/B TTM: 19.50X vs 行业8.07X vs S&P 500 8.65X",
            "P/E TTM: 257.7X; P/E F1: 130.33X; PEG F1: 2.1X",
            "EV/EBITDA: 134.12X",
            "Value Style Score: F（最差）; VGM Score: D",
            "Zacks Rank: 4-Sell; F1 EPS 4周下调6.2%，12周下调12.2%",
            "Earnings ESP: -3.5%（负值暗示下季可能miss）",
            "目标价$452基于16.15X前瞻12个月营收"
        ],
        "predictions": [
            {
                "metric": "6-12个月目标价",
                "predicted_value": "$452",
                "deadline": "2027-02-02",
                "comparison_to_consensus": "above"
            }
        ]
    },
    {
        "topic": "财务健康/资产负债表",
        "stance": "bullish",
        "confidence": "high",
        "summary": "Tesla资产负债表强健，为大规模资本支出提供缓冲。现金/等价物/投资$441亿，长期负债率仅7.58%远低于行业40%。利息覆盖倍数16.6X远高于行业5.08X。流动比率2.16。但Q4自由现金流$14.2亿同比降30%（去年$20.3亿），$200亿资本支出将显著消耗现金储备。",
        "data_points": [
            "现金/等价物/投资: $441亿（2024年末$366亿）",
            "长期负债率: 7.58% vs 行业40%",
            "利息覆盖倍数: 16.6X vs 行业5.08X",
            "流动比率: 2.16",
            "Q4经营现金流$38.1亿，同比降$10亿",
            "Q4资本支出$23.9亿; Q4自由现金流$14.2亿（去年$20.3亿）",
            "长期债务和融资租赁$67.4亿（2024年末$57.5亿）"
        ],
        "predictions": []
    },
    {
        "topic": "竞争格局",
        "stance": "bearish",
        "confidence": "high",
        "summary": "竞争全面加剧。美国市场面临GM、Ford、Rivian、Lucid等传统和新势力挑战，市场份额持续流失。中国市场面临BYD、NIO、XPeng、Li等本土品牌激烈竞争。Tesla是唯一有份额可失的玩家，其他所有竞争者都在抢夺其份额。车型老化也是拖累因素。",
        "data_points": [
            "美国EV市场份额从2020年约80%降至2022年63%再降至目前50%以下",
            "Tesla是唯一有份额可失的玩家，所有其他竞争者都在增长",
            "中国市场面临BYD、NIO、XPeng、Li等本土品牌竞争",
            "传统车企GM、Ford、Mercedes加速EV转型",
            "新势力Rivian、Lucid持续抢占高端市场",
            "车型老化（Model 3/Y为主力但设计已数年未大改）"
        ],
        "predictions": []
    }
]

data['report']['views'] = views

with open(path, 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Added {len(views)} views")
