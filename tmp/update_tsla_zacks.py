import json

# Load existing TSLA data
data_path = '/Users/aibrain/openclaw-workspace-superbrain/Project/antigravity-research/luminescent-hubble/data/TSLA.json'
with open(data_path, 'r') as f:
    ticker_data = json.load(f)

# Load our new analysis
analysis_path = '/Users/aibrain/openclaw-workspace-superbrain/Project/antigravity-research/luminescent-hubble/tmp/tsla_report3_analysis.json'
with open(analysis_path, 'r') as f:
    new_analysis = json.load(f)

# Find the existing Zacks report
zacks_idx = None
for i, report in enumerate(ticker_data['reports']):
    if report['id'] == 'tsla-zacks-20260202':
        zacks_idx = i
        break

if zacks_idx is None:
    print("ERROR: Zacks report not found in existing data!")
    exit(1)

print(f"Found Zacks report at index {zacks_idx}")

# Update the existing report with enriched data
existing = ticker_data['reports'][zacks_idx]
new_report = new_analysis['report']

# Update chart_insights (was empty)
existing['chart_insights'] = new_report['chart_insights']
print(f"Added {len(new_report['chart_insights'])} chart_insights")

# Update views with enriched version (more data_points, confidence, predictions)
existing['views'] = new_report['views']
print(f"Updated to {len(new_report['views'])} views")

# Add fields that were missing
existing['key_metrics'] = new_report.get('key_metrics')
existing['key_assumptions'] = new_report.get('key_assumptions', [])
existing['risk_factors'] = new_report.get('risk_factors', [])
existing['blind_spots'] = new_report.get('blind_spots', [])
existing['catalysts'] = new_report.get('catalysts', [])
existing['cross_comparison'] = new_report.get('cross_comparison')
existing['previous_rating'] = new_report.get('previous_rating')

# Update view_dimensions if new topics added
for view in new_report['views']:
    if view['topic'] not in ticker_data['view_dimensions']:
        ticker_data['view_dimensions'].append(view['topic'])
        print(f"Added new dimension: {view['topic']}")

# Save
with open(data_path, 'w') as f:
    json.dump(ticker_data, f, ensure_ascii=False, indent=2)

print(f"\nSuccessfully updated TSLA.json")
print(f"Zacks report now has:")
print(f"  - {len(existing['views'])} views")
print(f"  - {len(existing['chart_insights'])} chart_insights")
print(f"  - {len(existing.get('catalysts', []))} catalysts")
print(f"  - {len(existing.get('key_assumptions', []))} key_assumptions")
print(f"  - {len(existing.get('risk_factors', []))} risk_factors")
print(f"  - {len(existing.get('blind_spots', []))} blind_spots")
