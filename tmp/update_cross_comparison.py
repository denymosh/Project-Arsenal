#!/usr/bin/env python3
"""Update TSLA.json cross_comparison based on all 5 reports."""
import json, os

DATA_PATH = os.path.expanduser("~/openclaw-workspace-superbrain/Project/antigravity-research/luminescent-hubble/data/TSLA.json")

with open(DATA_PATH, "r") as f:
    data = json.load(f)

# Build cross_comparison
data["cross_comparison"] = {
    "consensus_matrix": {
        "FSD/自动驾驶": {
            "bullish": 2,   # Morningstar简版, Morningstar完整版
            "neutral": 0,
            "bearish": 2,   # Argus, Zacks(隐含)
            "not_mentioned": 1  # Stock Traders Daily(技术面为主)
        },
        "交付量/销量": {
            "bullish": 0,
            "neutral": 2,   # Morningstar简版, Zacks
            "bearish": 3,   # Argus, Morningstar完整版, Stock Traders Daily
            "not_mentioned": 0
        },
        "Robotaxi": {
            "bullish": 2,   # Morningstar简版, Morningstar完整版
            "neutral": 0,
            "bearish": 2,   # Argus, Zacks
            "not_mentioned": 1  # Stock Traders Daily
        },
        "毛利率/盈利能力": {
            "bullish": 0,
            "neutral": 3,   # Morningstar简版, Morningstar完整版, Argus
            "bearish": 1,   # Zacks
            "not_mentioned": 1  # Stock Traders Daily
        },
        "估值": {
            "bullish": 0,
            "neutral": 1,   # Morningstar完整版(P/FVE=1.05, 3星)
            "bearish": 3,   # Argus(P/E 205x), Zacks(P/S 15.4x), Stock Traders Daily
            "not_mentioned": 1  # Morningstar简版(与完整版重叠)
        },
        "能源业务": {
            "bullish": 3,   # Argus, Morningstar简版, Morningstar完整版
            "neutral": 1,   # Zacks
            "bearish": 0,
            "not_mentioned": 1  # Stock Traders Daily
        },
        "Optimus/机器人": {
            "bullish": 2,   # Morningstar完整版, Zacks
            "neutral": 0,
            "bearish": 0,
            "not_mentioned": 3  # Argus, Morningstar简版, Stock Traders Daily
        },
        "技术面/交易信号": {
            "bullish": 0,
            "neutral": 1,   # Stock Traders Daily(震荡区间)
            "bearish": 0,
            "not_mentioned": 4  # 其他4份基本面研报
        }
    },
    "major_divergences": [
        {
            "topic": "FSD/Robotaxi估值",
            "divergence": "major",
            "description": "Morningstar给予FSD $70/股+Robotaxi $120/股+Optimus $80/股的具体估值（合计$270/股，占FVE $400的67.5%），而Argus认为这些是'未经验证的长期赌注'，不给予任何估值溢价。Zacks持中性但警告近期现金流压力。"
        },
        {
            "topic": "2026年交付量预期",
            "divergence": "moderate",
            "description": "Morningstar完整版预计2026年交付降至156万辆（同比-5%），而Zacks和Argus预期温和增长。分歧核心在于EV税收抵免到期的影响程度。"
        },
        {
            "topic": "目标价/公允价值",
            "divergence": "major",
            "description": "Morningstar FVE $400（P/FVE=1.05，适当估值），Zacks目标价$452（16.15x P/S），Argus无目标价（HOLD），Stock Traders Daily目标$463.82。范围$400-$464，但估值方法论差异巨大。"
        },
        {
            "topic": "资本支出影响",
            "divergence": "moderate",
            "description": "Zacks强调$20B资本支出将严重压制近期现金流（2026E FCFF为负$9.37B），Argus也持谨慎态度。Morningstar则认为这是向'真实世界AI'转型的必要投入，长期回报可期。"
        }
    ],
    "highest_conviction_view": "能源业务看好（80%机构bullish/neutral，Q4收入$3.84B同比+25%，是唯一无争议的增长亮点）",
    "most_contrarian_view": "FSD/Robotaxi估值（Morningstar给$190/股估值 vs Argus认为零估值，分歧最大的单一议题）",
    "themes": [
        {
            "theme": "AI转型 vs 汽车基本面",
            "description": "所有研报的核心分歧：Tesla是否已从汽车制造商成功转型为AI公司。Morningstar按AI公司估值（FSD+Robotaxi+Optimus占67.5%），Argus/Zacks仍按汽车公司框架评估。"
        },
        {
            "theme": "短期阵痛 vs 长期愿景",
            "description": "2025年交付下降9%、利润下降47%、2026年$20B资本支出——所有机构都承认短期压力，但对'阵痛期'持续时间和长期回报的判断截然不同。"
        },
        {
            "theme": "估值泡沫还是合理溢价",
            "description": "P/E 205x、P/S 16.5x——Argus和Zacks认为估值过高，Morningstar认为P/FVE=1.05属于适当估值（但其FVE本身就包含大量AI溢价）。Stock Traders Daily从技术面看到$380-$460震荡区间。"
        }
    ],
    "consensus": {
        "overall_rating": "持有/中性",
        "rating_distribution": "0 买入, 4 持有/中性, 0 卖出（Stock Traders Daily为技术面买入但基于短期交易）",
        "target_price_range": "$400-$464",
        "target_price_median": "$426",
        "key_agreement": "所有机构一致认为：(1)短期交付和利润面临压力；(2)能源业务是确定性增长点；(3)2026年$20B+资本支出将考验现金流",
        "key_disagreement": "AI/Robotaxi/Optimus的估值贡献（从零到$270/股），以及Tesla是否应按汽车公司还是AI公司估值"
    }
}

# Also update each report's individual cross_comparison field
report_ids = [r.get("id","") for r in data["reports"]]
for i, r in enumerate(data["reports"]):
    vs_others = []
    for j, other in enumerate(data["reports"]):
        if i == j:
            continue
        # Find a divergence topic
        if r.get("institution") == "Argus Research" and other.get("institution") in ["Morningstar", "Morningstar（完整版）"]:
            vs_others.append({
                "compared_with": other.get("id",""),
                "topic": "FSD/Robotaxi估值",
                "divergence": "major",
                "description": f"Argus认为AI/Robotaxi是未经验证的长期赌注（零估值），{other.get('institution')}给予FSD+Robotaxi+Optimus合计$270/股估值"
            })
        elif r.get("institution") == "Morningstar" and other.get("institution") == "Argus Research":
            vs_others.append({
                "compared_with": other.get("id",""),
                "topic": "FSD/Robotaxi估值",
                "divergence": "major",
                "description": "Morningstar给予FSD $70/股+Robotaxi $120/股估值，Argus认为这些是未经验证的长期赌注"
            })
        elif r.get("institution") == "Zacks Equity Research" and other.get("institution") == "Morningstar（完整版）":
            vs_others.append({
                "compared_with": other.get("id",""),
                "topic": "资本支出影响",
                "divergence": "moderate",
                "description": "Zacks强调$20B资本支出将严重压制近期现金流，Morningstar完整版认为是必要的AI转型投入"
            })
    if vs_others:
        r["cross_comparison"] = {
            "vs_previous_reports": vs_others[:3],
            "consensus_position": f"{r.get('institution')}评级{r.get('rating')}，目标价${r.get('target_price',0)}"
        }

with open(DATA_PATH, "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Cross comparison updated successfully")
print(f"  themes: {len(data['cross_comparison']['themes'])}")
print(f"  major_divergences: {len(data['cross_comparison']['major_divergences'])}")
print(f"  consensus: {bool(data['cross_comparison']['consensus'])}")
