import json

path = '/Users/aibrain/openclaw-workspace-superbrain/Project/antigravity-research/luminescent-hubble/tmp/tsla_report3_analysis.json'
with open(path, 'r') as f:
    data = json.load(f)

chart_insights = [
    {
        "chart_name": "Price, Consensus & EPS Surprise",
        "chart_type": "line",
        "source_file": "TSLA_-Tesla,-Inc_p1_img3.png",
        "description": "2022-2027年Tesla股价走势与EPS共识预期及实际惊喜的叠加图。黑色实线为股价，彩色虚线为各年度EPS共识预期轨迹，绿色/红色箭头标记EPS超预期/不及预期。",
        "key_observations": [
            "2023-2024年EPS共识预期持续大幅下调（紫色虚线从约$5.5降至约$1.7），反映盈利预期恶化",
            "2025年EPS共识（蓝色虚线）同样经历显著下调，从约$3.5降至约$1.7",
            "2026-2027年EPS预期（绿色/棕色线）刚开始但已出现下调趋势",
            "股价在2024年底至2025年初出现大幅反弹（从约$150升至$450+），与EPS下调形成背离",
            "Q4 2025 EPS $0.50超预期（绿色箭头），但此前多个季度出现miss（红色箭头）"
        ],
        "data_not_in_text": [
            "2023年初EPS共识约$5.5，到2024年底降至约$1.7，累计下调约70%，显示盈利预期崩塌的严重程度",
            "股价与EPS预期的背离在2024年Q4-2025年Q1最为极端：EPS预期持续下调但股价翻倍，暗示市场定价完全基于AI/robotaxi叙事而非基本面"
        ],
        "investment_implication": "EPS共识预期的持续下调趋势尚未逆转，2026E预期已开始下调（4周降6.2%）。股价与盈利的极端背离意味着任何AI/robotaxi叙事的动摇都可能导致剧烈回调。"
    },
    {
        "chart_name": "Sales and EPS Growth Rates (Y/Y %)",
        "chart_type": "bar",
        "source_file": "TSLA_-Tesla,-Inc_p1_img7.png",
        "description": "2023-2027年Tesla营收和EPS同比增长率柱状图。绿色柱为营收增长，红色/粉色柱为EPS增长（负值），斜线柱为预测值。",
        "key_observations": [
            "2023年营收增长18.8%但EPS下降23.3%，利润率压缩明显",
            "2024年营收仅增0.9%但EPS大降22.4%，增长几乎停滞",
            "2025年营收下降2.9%且EPS暴跌31.4%，为最差年份",
            "2026E预期营收仅增1.6%但EPS大幅反弹92.8%，反弹主要靠低基数效应",
            "2027E预期营收增长23.2%、EPS增长41.6%，增长加速"
        ],
        "data_not_in_text": [
            "连续三年（2023-2025）EPS负增长的视觉冲击力极强，累计EPS从2022年峰值下降超60%",
            "2026E营收仅增1.6%但EPS预期增92.8%的巨大剪刀差，暗示市场预期运营杠杆大幅改善，但这一假设风险极高"
        ],
        "investment_implication": "2026年EPS 92.8%的反弹预期建立在极低基数上（2025年EPS仅$1.66），且营收仅增1.6%意味着几乎全靠利润率改善。如果毛利率未能如期恢复，EPS反弹幅度将大打折扣。"
    },
    {
        "chart_name": "Sales Historical and Estimates",
        "chart_type": "bar",
        "source_file": "TSLA_-Tesla,-Inc_p2_img1.png",
        "description": "2021-2027年Tesla年度营收柱状图，深绿色为实际值，浅绿色为预测值。Y轴范围0-$120B。",
        "key_observations": [
            "营收从2021年约$54B稳步增长至2023年约$97B，但2024-2025年增长停滞在$95-97B区间",
            "2026E预期$96.4B几乎与2025年持平，增长率仅1.6%",
            "2027E预期$118.7B才出现明显增长跳跃（+23.2%）",
            "2024-2026年形成明显的营收平台期，持续约3年"
        ],
        "data_not_in_text": [
            "视觉上2024-2026年三根柱子几乎等高，形成罕见的3年营收停滞平台，对于一家P/S 15X+的成长股极为不利",
            "2027年的增长跳跃暗示市场预期新产品（低价Model、Cybercab）将在2027年开始贡献，但这增加了执行风险"
        ],
        "investment_implication": "3年营收停滞期对于当前15X+ P/S估值构成严重挑战。如果2027年增长未能兑现，估值压缩风险极大。投资者需要极高的信念才能在营收零增长期持有如此高估值的股票。"
    },
    {
        "chart_name": "EPS Historical and Estimates",
        "chart_type": "bar",
        "source_file": "TSLA_-Tesla,-Inc_p2_img3.png",
        "description": "2021-2027年Tesla年度EPS柱状图。深绿色为实际值，浅绿色为预测值。Y轴范围$0-$4.5。",
        "key_observations": [
            "EPS在2022年达到峰值约$4.0，此后连续三年下滑",
            "2023年约$3.1，2024年约$2.4，2025年仅$1.66，累计从峰值下降约58%",
            "2026E $3.20预期恢复至2023年水平，2027E $4.53预期超越2022年峰值",
            "EPS走势呈现明显的V型反转预期"
        ],
        "data_not_in_text": [
            "从2022年峰值$4.0到2025年谷底$1.66的下降幅度达58%，视觉上呈现陡峭的下坡",
            "预期的V型反转需要EPS在2年内从$1.66增长至$4.53（+173%），这一增速在Tesla历史上前所未有"
        ],
        "investment_implication": "V型EPS反转预期极为激进。2026-2027年EPS需要从$1.66增长至$4.53，年均复合增长65%+。任何执行偏差都将导致预期下调，而当前P/E 130X+的估值对预期下调极度敏感。"
    },
    {
        "chart_name": "Consensus Estimate vs 12-Month EPS vs Price",
        "chart_type": "line",
        "source_file": "TSLA_-Tesla,-Inc_p2_img5.png",
        "description": "2022-2029年Tesla共识EPS预期（绿色虚线）、12个月滚动EPS（蓝色虚线）与股价（灰色实线）的三线叠加图。左轴为EPS，右轴为股价。",
        "key_observations": [
            "12个月滚动EPS（蓝色线）从2022年峰值约$4.0持续下降至2025年约$1.7",
            "共识预期（绿色虚线）在2025年后开始上翘，预期2027-2029年EPS持续增长至$4.0+",
            "股价在2024年底出现与EPS趋势完全脱钩的大幅上涨",
            "2022-2024年股价与EPS走势高度相关，但2024年Q4后完全背离"
        ],
        "data_not_in_text": [
            "共识预期线显示分析师预期EPS将在2027年左右回到2022年峰值水平，意味着盈利能力需要5年才能恢复",
            "股价已经提前反映了2027-2028年的EPS预期，当前价格隐含的远期P/E约100X（以2027E $4.53计算）"
        ],
        "investment_implication": "股价已完全脱离当前盈利基本面，完全定价于远期AI/robotaxi预期。这创造了一个二元结果：如果长期叙事兑现，当前价格合理；如果执行延迟或不及预期，回调空间巨大（下行至$200-250区间）。"
    },
    {
        "chart_name": "Valuation Multiples Comparison Table",
        "chart_type": "table",
        "source_file": "TSLA_-Tesla,-Inc_p6_img1.jpeg",
        "description": "TSLA估值倍数与行业、板块、S&P 500的全面对比表，包含P/S F12M、EV/Sales TTM、P/B TTM三个维度的当前值、5年高/低/中位数。",
        "key_observations": [
            "P/S F12M 15.38X是行业3.4X的4.5倍，是S&P 500 5.62X的2.7倍",
            "EV/Sales TTM 16.57X是行业3.41X的4.9倍",
            "P/B TTM 19.50X是行业8.07X的2.4倍，但远低于5年高点44.29X",
            "P/S 5年中位数8.21X，当前15.38X高出中位数87%",
            "所有估值指标均显著高于行业和大盘"
        ],
        "data_not_in_text": [
            "P/B 5年高点44.29X出现在2021年泡沫期，当前19.50X虽低于峰值但仍是行业的2.4倍",
            "EV/Sales 5年低点3.93X（2022年底）到当前16.57X，反弹超4倍，显示估值弹性极大",
            "行业P/S中位数仅2.35X，Tesla的15.38X意味着市场给予其约6.5倍的行业溢价"
        ],
        "investment_implication": "Tesla的估值溢价完全建立在AI/自动驾驶/机器人的长期叙事上。P/S 15.38X vs 行业3.4X的4.5倍溢价意味着市场预期Tesla的长期利润率和增长将远超传统车企。如果这些预期未能兑现，估值向行业均值回归将意味着股价下跌75%+。"
    },
    {
        "chart_name": "TSLA vs Industry Price Performance",
        "chart_type": "line",
        "source_file": "TSLA_-Tesla,-Inc_p7_img5.png",
        "description": "Tesla股价（灰色实线）与Automotive-Domestic行业指数（紫色虚线）的相对表现对比图，时间跨度约2020-2026年。",
        "key_observations": [
            "2021年Tesla股价大幅跑赢行业，随后2022年暴跌时跑输行业",
            "2023年Tesla反弹但行业表现更稳定",
            "2024年底Tesla再次大幅跑赢行业，走势与行业完全脱钩",
            "行业指数走势相对平稳，Tesla波动率远高于行业（Beta 1.86）"
        ],
        "data_not_in_text": [
            "Tesla与行业的相关性在2024年Q4后几乎降至零，行业横盘而Tesla暴涨，说明Tesla的定价已完全脱离汽车行业基本面",
            "行业指数在2022-2025年期间基本持平，而Tesla经历了从峰值跌70%再反弹300%的剧烈波动"
        ],
        "investment_implication": "Tesla与汽车行业的完全脱钩意味着传统汽车估值框架已不适用。投资者需要用科技/AI框架来评估Tesla，但这也意味着如果AI叙事退潮，Tesla可能重新向行业估值靠拢，下行风险巨大。"
    }
]

data['report']['chart_insights'] = chart_insights

with open(path, 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Added {len(chart_insights)} chart_insights")
print("Final JSON ready.")
