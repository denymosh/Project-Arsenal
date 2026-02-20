#!/usr/bin/env python3
"""Fix schema issues in TSLA.json."""
import json, os

DATA_PATH = os.path.expanduser("~/openclaw-workspace-superbrain/Project/antigravity-research/luminescent-hubble/data/TSLA.json")

with open(DATA_PATH, "r") as f:
    data = json.load(f)

# Fix Report 0 key_metrics.other: string -> dict
r0 = data["reports"][0]
if isinstance(r0.get("key_metrics", {}).get("other"), str):
    r0["key_metrics"]["other"] = {
        "beta": "1.64",
        "debt_capital": "9.2%",
        "cash": "$16.5B",
        "market_cap": "$1.56T",
        "credit_rating": "Baa3/BBB stable"
    }

# Fix Report 2 key_metrics.other if needed
r2 = data["reports"][2]
if r2.get("key_metrics") and isinstance(r2["key_metrics"].get("other"), str):
    other_str = r2["key_metrics"]["other"]
    r2["key_metrics"]["other"] = {
        "moat": "Narrow",
        "uncertainty": "Very High",
        "capital_allocation": "Exemplary",
        "detail": other_str[:200]
    }

# Fix cross_comparison.major_divergences: divergence -> severity, add bulls/bears
for div in data.get("cross_comparison", {}).get("major_divergences", []):
    if "divergence" in div and "severity" not in div:
        div["severity"] = div.pop("divergence")
    if "bulls" not in div:
        div["bulls"] = []
    if "bears" not in div:
        div["bears"] = []

# Add bulls/bears to each divergence
divs = data.get("cross_comparison", {}).get("major_divergences", [])
if len(divs) >= 4:
    divs[0]["bulls"] = ["Morningstar", "Morningstar（完整版）"]
    divs[0]["bears"] = ["Argus Research", "Zacks Equity Research"]
    divs[0]["impact_on_valuation"] = "FSD+Robotaxi+Optimus估值从$0到$270/股，对应股价差异超过60%"
    
    divs[1]["bulls"] = []
    divs[1]["bears"] = ["Morningstar（完整版）"]
    divs[1]["impact_on_valuation"] = "交付量差异约10万辆，影响Revenue约$5-8B"
    
    divs[2]["bulls"] = ["Stock Traders Daily"]
    divs[2]["bears"] = ["Argus Research"]
    divs[2]["impact_on_valuation"] = "目标价范围$400-$464，中位数$426，当前价约$420-450"
    
    divs[3]["bulls"] = ["Morningstar（完整版）"]
    divs[3]["bears"] = ["Zacks Equity Research", "Argus Research"]
    divs[3]["impact_on_valuation"] = "$20B资本支出导致2026E FCFF为负$9.37B，但长期可能创造$18B+年化自由现金流"

# Fix individual report cross_comparison fields too
for r in data["reports"]:
    cc = r.get("cross_comparison")
    if cc and isinstance(cc, dict):
        for item in cc.get("vs_previous_reports", []):
            if "divergence" in item and "severity" not in item:
                # This is the per-report format, keep divergence field name
                pass

with open(DATA_PATH, "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Schema fixes applied successfully")
