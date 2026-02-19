# Local AI Run Guide

## 1) Prepare env (optional)
- `run_local_ai_analysis.py` still supports `.env.local_ai` for OpenAI-compatible endpoints.
- `auto_analyze_and_deploy.py` uses the superbrain OpenClaw model path directly and does not require `.env.local_ai`.

## 2) Prepare report text
Place a text/markdown file for the new report, for example:
- `reports/TSLA/originals/2026-02-18_report.md`

## 3) Run analysis and save
```bash
cd analyzer
python3 run_local_ai_analysis.py TSLA \
  --report-file ../reports/TSLA/originals/2026-02-18_report.md \
  --model <your-model-id>
```

## 4) Optional auto push + deploy
```bash
python3 run_local_ai_analysis.py TSLA \
  --report-file ../reports/TSLA/originals/2026-02-18_report.md \
  --model <your-model-id> \
  --auto-push
```

`--auto-push` calls `auto_push.py` (git add/commit/push). Vercel auto-deploy depends on your repo integration.

## 5) One-command newest-report automation
```bash
cd analyzer
python3 auto_analyze_and_deploy.py NVDA
```

Behavior:
- selects newest unprocessed PDF in `reports/NVDA/originals`
- extracts PDF text to `tmp/*.md`
- runs local model analysis
- saves structured result into project data
- auto git push (which triggers Vercel if integrated)
- tracks processed files in `memory/analyzed_reports_tracker.json`
