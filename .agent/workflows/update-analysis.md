---
description: 新增/更新标的研报后的完整操作流程（从PDF到部署上线）
---

# 研报分析更新工作流

## 概述

当你收到新的研报PDF，或需要更新某个标的的分析数据时，按以下步骤操作。

---

## 第一步：放置研报PDF

将新的研报PDF文件放入对应标的的 `reports/{TICKER}/originals/` 目录。

例如：
```
reports/TSLA/originals/2026-03-01_Morgan_Stanley_TSLA.pdf
```

如果是新标的，确保已在 `data/tickers.json` 中注册。

---

## 第二步：分析研报（与AI对话）

在对话中告诉助手分析新的研报。助手会：

1. 读取PDF提取关键信息
2. 按照 `models.py` 中的数据模型结构化数据
3. 生成分析维度（views）、预测（predictions）、风险/催化剂等
4. 如有图表，提取图表视觉洞察（chart_insights）

---

## 第三步：保存分析数据

// turbo
助手会运行 `save_analysis.py` 将分析结果保存：

```powershell
cd analyzer
uv run python save_analysis.py {TICKER}
```

这会：
- 更新 `data/{TICKER}.json`（结构化数据）
- 生成 `reports/{TICKER}/analysis/` 下的Markdown分析报告
- 更新 `reports/{TICKER}/_summary.md` 汇总报告

---

## 第四步：推送到GitHub

// turbo
```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
git add -A
git commit -m "analysis: 更新{TICKER}研报分析"
git push origin master
```

---

## 第五步：重新部署到Vercel

// turbo
```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
cd web
Copy-Item -Recurse -Force "..\data" ".\data"
npx vercel deploy --prod --yes
Remove-Item -Recurse -Force ".\data"
```

部署完成后访问线上地址即可看到更新。

---

## 快速命令汇总（一键更新部署）

```powershell
# 在项目根目录执行
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
git add -A; git commit -m "update: 研报数据更新"; git push origin master
cd web; Copy-Item -Recurse -Force "..\data" ".\data"; npx vercel deploy --prod --yes; Remove-Item -Recurse -Force ".\data"; cd ..
```

---

## 补充：新增标的

如果要跟踪全新的标的：

1. 编辑 `data/tickers.json`，添加新条目：
```json
{
  "symbol": "AAPL",
  "name_en": "Apple Inc.",
  "name_cn": "苹果",
  "sector": "消费电子/服务",
  "default_dimensions": ["iPhone", "服务业务", "AI", "中国市场", "利润率", "估值"]
}
```

2. 创建初始数据文件 `data/AAPL.json`（可以先放空壳结构）
3. 创建目录 `reports/AAPL/originals/` 并放入研报PDF
4. 按上述流程分析 → 保存 → 推送 → 部署

---

## 项目结构速查

```
luminescent-hubble/
├── analyzer/          # Python分析管线
│   ├── lib/           # 核心库（models, consensus, report_generator等）
│   ├── save_analysis.py   # 保存分析结果
│   ├── extract_images.py  # PDF图片提取
│   └── pyproject.toml     # Python依赖
├── data/              # 结构化JSON数据（核心数据源）
│   ├── tickers.json   # 标的列表
│   ├── GOOGL.json     # 各标的分析数据
│   ├── catalysts.json # 催化剂日历
│   └── scorecard.json # 机构记分板
├── reports/           # Markdown分析报告
│   └── {TICKER}/
│       ├── originals/ # PDF研报原件（不入Git）
│       └── analysis/  # 生成的分析报告
├── web/               # Next.js仪表盘
│   ├── app/           # 页面路由
│   ├── components/    # UI组件
│   └── lib/data.js    # 数据加载
├── vercel.json        # Vercel部署配置
└── .gitignore
```

## 线上地址

- **生产环境**: https://web-nine-taupe-91.vercel.app
- **密码**: 6868
- **GitHub**: https://github.com/player0xne/research-report-analyzer
