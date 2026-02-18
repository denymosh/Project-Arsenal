# 研报分析系统 - 实施计划

## 项目概述

构建一个**研报分析系统**，由两部分组成：
1. **本地数据管理工具**（Python脚本）：负责数据存储、共识计算、回溯验证、报告生成
2. **Web可视化仪表盘**（Next.js + Vercel SSG）：静态展示分析结果、共识对比、回溯验证、催化剂日历

**AI分析层由 Antigravity 直接承担**——用户在 Antigravity 中选用什么模型（Gemini 3 Pro / Claude Opus 4.6 等），
就用该模型进行分析。Python脚本不调用任何AI API，只负责数据管理和文件生成。

## 关注标的

TSLA、NVDA、RKLB、ONDS、META、GOOGL

## 核心设计原则

1. **Antigravity即AI层**：不需要单独的AI API集成，分析由用户当前选用的Antigravity模型完成
2. **Python脚本只管数据**：读写JSON、计算共识、生成MD、回溯验证、git push
3. **无API Key依赖**：零成本运行分析流程
4. **前端用Recharts交互式图表**：Python不生成图片，只输出JSON数据
5. **PDF不入Git**：.gitignore排除原始研报文件，只推送JSON和MD
6. **按标的分割数据**：每个标的一个JSON文件，前端按需加载

## 技术架构

```
┌───────────────────────────────────────────────────────────────────────┐
│                         完整工作流程                                    │
│                                                                       │
│  ┌─────────────────┐     ┌──────────────────────┐     ┌────────────┐ │
│  │  用户 + 研报      │     │  Antigravity (AI层)   │     │  Python脚本 │ │
│  │                  │     │                      │     │  (数据层)   │ │
│  │ 选择AI模型       │     │ • 阅读研报内容         │     │            │ │
│  │ 提供研报内容      │──→  │ • 加载历史上下文       │──→  │ 保存分析MD  │ │
│  │ (文字/截图/PDF)  │     │ • 深度分析+交叉对比    │     │ 更新JSON   │ │
│  │                  │     │ • 输出结构化分析结果    │     │ 计算共识    │ │
│  └─────────────────┘     └──────────────────────┘     │ 自动git push│ │
│                                                       └──────┬─────┘ │
│                                                              │       │
│                          ┌───────────────────────────────────┘       │
│                          ▼                                           │
│                   ┌──────────────┐     ┌──────────────────────┐      │
│                   │  GitHub仓库   │──→  │  Vercel (Web仪表盘)   │      │
│                   │  (自动推送)   │     │  • 标的总览Dashboard  │      │
│                   │              │     │  • 观点热力图         │      │
│                   │  data/*.json │     │  • 回溯记分板         │      │
│                   │  reports/    │     │  • 催化剂日历         │      │
│                   └──────────────┘     └──────────────────────┘      │
└───────────────────────────────────────────────────────────────────────┘
```

## 项目目录结构

```
luminescent-hubble/
├── .gitignore                      # 忽略PDF、node_modules等
├── implementation_plan.md          # 实施计划（本文件）
├── task.md                         # 任务进度跟踪
├── README.md                       # 项目使用文档
│
├── analyzer/                       # 本地数据管理工具（Python）
│   ├── pyproject.toml              # Python项目配置 (uv管理)
│   │
│   ├── load_context.py             # 入口1: 加载标的历史上下文
│   │                               # 用法: uv run python load_context.py TSLA
│   │                               # 输出: 该标的已有研报列表、共识数据、机构靠谱度
│   │                               # 供Antigravity阅读后进行交叉对比分析
│   │
│   ├── save_analysis.py            # 入口2: 保存分析结果
│   │                               # 用法: uv run python save_analysis.py TSLA --input=analysis.json
│   │                               # 功能: 保存分析JSON、生成MD、更新共识、更新催化剂
│   │
│   ├── backtest.py                 # 入口3: 回溯验证
│   │                               # 用法: uv run python backtest.py TSLA
│   │                               # 功能: 拉取最新市场数据，对比历史预测，更新记分板
│   │
│   ├── auto_push.py                # 入口4: 自动git commit + push
│   │                               # 用法: uv run python auto_push.py "更新TSLA分析"
│   │
│   └── lib/
│       ├── __init__.py
│       ├── data_manager.py         # JSON数据读/写/更新/合并
│       ├── consensus.py            # 共识计算：评级/目标价/情感汇总
│       ├── cross_validator.py      # 交叉验证数据准备：多研报对比矩阵
│       ├── backtest_engine.py      # 回溯验证：预测 vs 实际数据
│       ├── report_generator.py     # 分析报告MD文件生成
│       ├── market_data.py          # 市场数据拉取（yfinance）
│       └── models.py              # 数据模型定义（Pydantic dataclass）
│
├── data/                           # 结构化数据（本地生成，Web读取，入Git）
│   ├── tickers.json                # 标的列表和元信息
│   ├── TSLA.json                   # TSLA所有研报结构化数据
│   ├── NVDA.json                   # NVDA所有研报结构化数据
│   ├── RKLB.json
│   ├── ONDS.json
│   ├── META.json
│   ├── GOOGL.json
│   ├── scorecard.json              # 分析师/机构准确率 + "靠谱度"追踪
│   └── catalysts.json              # 催化剂日历数据
│
├── reports/                        # 研报文件和分析报告
│   ├── TSLA/
│   │   ├── _summary.md             # TSLA研报汇总对比（自动生成）
│   │   ├── originals/              # 原始研报存档（不入Git）
│   │   │   └── 2026-02-17_高盛_买入.pdf
│   │   └── analysis/               # 分析报告（入Git）
│   │       └── 2026-02-17_高盛_买入_分析.md
│   ├── NVDA/
│   │   ├── _summary.md
│   │   ├── originals/
│   │   └── analysis/
│   ├── RKLB/
│   │   ├── originals/
│   │   └── analysis/
│   ├── ONDS/
│   │   ├── originals/
│   │   └── analysis/
│   ├── META/
│   │   ├── originals/
│   │   └── analysis/
│   └── GOOGL/
│       ├── originals/
│       └── analysis/
│
└── web/                            # Next.js Web仪表盘
    ├── package.json
    ├── next.config.js
    ├── vercel.json                 # Vercel部署配置
    ├── public/
    ├── src/
    │   ├── app/
    │   │   ├── layout.js           # 全局布局（含密码锁逻辑）
    │   │   ├── page.js             # 首页 - 标的总览Dashboard
    │   │   ├── ticker/[id]/
    │   │   │   └── page.js         # 单标的深度视图
    │   │   ├── scorecard/
    │   │   │   └── page.js         # 回溯验证记分板
    │   │   └── calendar/
    │   │       └── page.js         # 催化剂日历
    │   ├── components/
    │   │   ├── Layout/
    │   │   │   ├── Navbar.js       # 导航栏
    │   │   │   └── Footer.js       # 页脚
    │   │   ├── Dashboard/
    │   │   │   ├── TickerCard.js    # 标的卡片（含情绪仪表盘）
    │   │   │   └── OverviewStats.js # 总览统计
    │   │   ├── Charts/
    │   │   │   ├── SentimentGauge.js    # 情绪仪表盘 (Recharts)
    │   │   │   ├── TargetPriceChart.js  # 目标价 vs 现价图 (Recharts)
    │   │   │   ├── ConsensusRadar.js    # 共识雷达图 (Recharts)
    │   │   │   └── MetricsTrend.js      # 关键指标趋势图 (Recharts)
    │   │   ├── Ticker/
    │   │   │   ├── ViewsHeatmap.js      # 观点热力图（多机构多维度）
    │   │   │   ├── ReportTimeline.js    # 研报时间线
    │   │   │   ├── DivergencePanel.js   # 分歧分析面板
    │   │   │   └── PredictionTracker.js # 预测追踪表格
    │   │   ├── Scorecard/
    │   │   │   ├── AccuracyTable.js     # 准确率排行表
    │   │   │   ├── ReliabilityBadge.js  # "靠谱度"徽章组件
    │   │   │   └── VerifiedList.js      # 已验证观点列表
    │   │   ├── Calendar/
    │   │   │   └── CatalystCalendar.js  # 催化剂日历组件
    │   │   └── Auth/
    │   │       └── PasswordGate.js      # 前端密码锁
    │   ├── lib/
    │   │   ├── dataLoader.js       # 静态JSON数据加载（SSG getStaticProps）
    │   │   └── utils.js            # 工具函数（格式化、颜色映射等）
    │   └── styles/
    │       └── globals.css         # 全局样式 + CSS变量/设计token
    └── vercel.json                 # Vercel部署配置
```

## 详细工作流程

### 流程1：分析新研报

```
步骤1: 用户在Antigravity中提供研报
       "帮我分析这篇TSLA研报 [粘贴内容/截图]"

步骤2: Antigravity运行上下文加载脚本
       > uv run python load_context.py TSLA
       脚本输出:
       - 已有研报数量、最近的分析记录
       - 当前共识评级和目标价区间
       - 各机构靠谱度评分
       - 待验证的预测列表

步骤3: Antigravity结合历史上下文 + 新研报内容，进行分析:
       - 提取核心观点、评级、目标价
       - 情感打分 (-1到1)
       - 与历史研报交叉对比
       - 标注分歧点和共识
       - 识别关键假设和风险盲点
       - 提取催化剂时间节点

步骤4: Antigravity将分析结果写入临时JSON文件
       然后运行保存脚本:
       > uv run python save_analysis.py TSLA --input=tmp_analysis.json
       脚本执行:
       a. 读取分析JSON
       b. 生成分析MD → reports/TSLA/analysis/YYYY-MM-DD_机构_评级_分析.md
       c. 更新 data/TSLA.json（追加新报告 + 重算共识 + 更新交叉对比矩阵）
       d. 更新 data/catalysts.json（新增催化剂事件）
       e. 更新 data/scorecard.json（如有新的机构首次出现）
       f. 重新生成 reports/TSLA/_summary.md

步骤5: 自动推送
       > uv run python auto_push.py "新增TSLA高盛研报分析"
       → GitHub收到推送 → Vercel自动重新构建 → 网站更新
```

### 流程2：回溯验证（财报发布后）

```
步骤1: 用户在Antigravity中触发
       "TSLA Q1交付数据已公布，实际42.3万辆，帮我回溯验证"

步骤2: Antigravity运行回溯脚本
       > uv run python backtest.py TSLA --event="Q1交付" --actual="423000"
       脚本执行:
       a. 查找 data/TSLA.json 中所有关于"Q1交付量"的预测
       b. 逐一对比预测值 vs 实际值
       c. 更新每个预测的 verified/actual_value/accurate 字段
       d. 重新计算各机构的准确率
       e. 更新 data/scorecard.json
       f. 更新 data/catalysts.json（标记已验证）

步骤3: Antigravity展示回溯结果:
       "高盛预测42万 → 实际42.3万 ✅ 偏差0.7%
        摩根预测39-41万 → 实际42.3万 ❌ 低估3.2-8.5%"

步骤4: 自动推送更新
```

### 流程3：查看汇总（无需运行脚本）

```
用户直接访问 Vercel 部署的网站查看:
- 标的总览Dashboard
- 观点热力图
- 回溯记分板
- 催化剂日历
```

## 数据Schema设计

### 分析结果输入格式（Antigravity输出 → save_analysis.py 接收）

Antigravity 分析完研报后，将结构化结果写入临时JSON文件：

```json
{
  "ticker": "TSLA",
  "report": {
    "date": "2026-02-17",
    "institution": "高盛",
    "institution_en": "Goldman Sachs",
    "analyst": "Mark Delaney",
    "rating": "买入",
    "previous_rating": null,
    "target_price": 420,
    "previous_target_price": null,
    "sentiment_score": 0.8,
    "views": [
      {
        "topic": "FSD",
        "stance": "bullish",
        "confidence": "high",
        "summary": "FSD V13将在Q2大规模推送，订阅率预计达15%",
        "data_points": ["FSD V12.5已在100万辆车上激活", "用户满意度调查85%正面"],
        "predictions": [
          {
            "metric": "FSD订阅率",
            "predicted_value": "15%",
            "deadline": "2026-Q2",
            "comparison_to_consensus": "above"
          }
        ]
      }
    ],
    "key_metrics": {
      "revenue_estimate": "$28B (Q1)",
      "eps_estimate": "$0.85",
      "growth_rate": "18% YoY",
      "margin_estimate": "18.5%"
    },
    "key_assumptions": [
      "Model 2将在2026下半年量产",
      "FSD监管在加州获批"
    ],
    "risk_factors": ["竞争加剧", "宏观利率环境"],
    "blind_spots": ["Elon分散精力于xAI/SpaceX的管理风险"],
    "catalysts": [
      {
        "event": "Q1交付数据公布",
        "expected_date": "2026-04-02",
        "importance": "high",
        "related_views": ["交付量"]
      }
    ],
    "cross_comparison": {
      "vs_previous_reports": [
        {
          "compared_with": "20260210_morgan",
          "topic": "FSD",
          "divergence": "major",
          "description": "高盛预测订阅率15%，远高于摩根的10%预期"
        }
      ],
      "consensus_position": "略偏乐观，目标价高于共识均值12%"
    }
  }
}
```

### 标的数据文件 (data/TSLA.json)

```json
{
  "ticker": "TSLA",
  "name_en": "Tesla Inc.",
  "name_cn": "特斯拉",
  "current_consensus": {
    "rating": "买入",
    "avg_target_price": 365,
    "min_target_price": 280,
    "max_target_price": 420,
    "sentiment_avg": 0.65,
    "total_reports": 3,
    "last_updated": "2026-02-22"
  },
  "view_dimensions": ["FSD", "交付量", "毛利率", "Robotaxi", "能源业务", "估值"],
  "reports": ["...（同上述report结构，追加存储）"],
  "cross_comparison": {
    "consensus_matrix": {
      "FSD": {"bullish": 2, "neutral": 0, "bearish": 1, "not_mentioned": 0},
      "交付量": {"bullish": 3, "neutral": 0, "bearish": 0, "not_mentioned": 0}
    },
    "major_divergences": [
      {
        "topic": "Robotaxi",
        "severity": "major",
        "description": "高盛和花旗看多，摩根谨慎",
        "bulls": ["高盛", "花旗"],
        "bears": ["摩根"],
        "impact_on_valuation": "目标价差异的主要驱动因素"
      }
    ]
  },
  "sentiment_history": [
    {"date": "2026-02-17", "institution": "高盛", "score": 0.8},
    {"date": "2026-02-22", "institution": "摩根", "score": 0.3}
  ]
}
```

### 记分板数据 (data/scorecard.json)

```json
{
  "institutions": [
    {
      "name": "高盛",
      "name_en": "Goldman Sachs",
      "reliability_score": 0.83,
      "reliability_tier": "A",
      "total_predictions": 15,
      "verified_predictions": 12,
      "accurate_predictions": 10,
      "accuracy_rate": 0.833,
      "by_ticker": {
        "TSLA": {"total": 5, "verified": 4, "accurate": 3, "rate": 0.75},
        "NVDA": {"total": 4, "verified": 3, "accurate": 3, "rate": 1.0}
      },
      "recent_verified": [
        {
          "date": "2026-01-28",
          "ticker": "NVDA",
          "prediction": "Q4营收超$380亿",
          "actual": "Q4营收$392亿",
          "accurate": true,
          "deviation_pct": 3.2
        }
      ],
      "accuracy_trend": [
        {"period": "2025-H2", "rate": 0.78},
        {"period": "2026-H1", "rate": 0.88}
      ]
    }
  ],
  "reliability_tiers": {
    "S": {"min_rate": 0.9, "label": "极其靠谱", "weight": 1.5},
    "A": {"min_rate": 0.8, "label": "非常靠谱", "weight": 1.2},
    "B": {"min_rate": 0.65, "label": "一般", "weight": 1.0},
    "C": {"min_rate": 0.5, "label": "不太靠谱", "weight": 0.7},
    "D": {"min_rate": 0.0, "label": "反向指标", "weight": 0.3}
  },
  "last_updated": "2026-02-22"
}
```

### 催化剂日历 (data/catalysts.json)

```json
{
  "catalysts": [
    {
      "id": "tsla_q1_delivery",
      "date": "2026-04-02",
      "ticker": "TSLA",
      "event": "Q1交付数据公布",
      "importance": "high",
      "related_reports": ["20260217_goldman", "20260222_morgan"],
      "predictions_to_verify": [
        {"report_id": "20260217_goldman", "institution": "高盛", "metric": "Q1交付量", "value": "42万"},
        {"report_id": "20260222_morgan", "institution": "摩根", "metric": "Q1交付量", "value": "39-41万"}
      ],
      "verified": false,
      "actual_result": null
    }
  ],
  "last_updated": "2026-02-22"
}
```

## 实施阶段

### 阶段一：基础设施搭建（当前）
1. ✅ 确定技术方案和架构
2. ⬜ 创建项目目录结构（所有标的文件夹 + 子目录）
3. ⬜ 初始化Python项目（uv + pyproject.toml）
4. ⬜ 初始化Next.js项目（App Router + Recharts）
5. ⬜ 创建初始JSON数据文件（空结构）
6. ⬜ 编写分析报告MD模板
7. ⬜ 配置.gitignore

### 阶段二：本地数据管理工具
8. ⬜ 实现数据模型定义 (models.py - Pydantic)
9. ⬜ 实现JSON数据读写管理 (data_manager.py)
10. ⬜ 实现上下文加载脚本 (load_context.py)
11. ⬜ 实现分析保存脚本 (save_analysis.py)
12. ⬜ 实现共识计算模块 (consensus.py)
13. ⬜ 实现交叉验证数据准备 (cross_validator.py)
14. ⬜ 实现分析报告MD生成 (report_generator.py)
15. ⬜ 实现市场数据拉取 (market_data.py)
16. ⬜ 实现回溯验证引擎 (backtest_engine.py + backtest.py)
17. ⬜ 实现自动git push (auto_push.py)
18. ⬜ 端到端测试（用模拟数据走通全流程）

### 阶段三：Web仪表盘
19. ⬜ 设计全局样式和设计系统（深色主题、CSS变量）
20. ⬜ 实现密码锁组件 (PasswordGate.js)
21. ⬜ 实现全局布局和导航 (Layout, Navbar)
22. ⬜ 实现首页Dashboard（标的卡片 + 情绪仪表盘 + 总览统计）
23. ⬜ 实现单标的深度视图 - 观点热力图
24. ⬜ 实现单标的深度视图 - 研报时间线
25. ⬜ 实现单标的深度视图 - 目标价 vs 现价图 (Recharts)
26. ⬜ 实现单标的深度视图 - 分歧分析面板
27. ⬜ 实现单标的深度视图 - 预测追踪表格
28. ⬜ 实现回溯验证记分板（准确率排行 + "靠谱度"徽章）
29. ⬜ 实现催化剂日历
30. ⬜ 响应式设计优化

### 阶段四：部署和联调
31. ⬜ 初始化GitHub私有仓库
32. ⬜ 配置Vercel部署（连接GitHub）
33. ⬜ 构建时数据注入流程验证
34. ⬜ 端到端全流程测试
35. ⬜ 编写使用文档 (README.md)

### 阶段五：自动化增强（后期）
36. ⬜ Watchdog 文件夹监控（新PDF自动触发）
37. ⬜ 定时回溯验证（财报日自动触发）

## 技术栈总结

| 组件 | 技术选择 | 理由 |
|------|---------|------|
| AI分析层 | Antigravity (用户选择的模型) | 零额外成本、无API Key、模型自由切换 |
| Python包管理 | uv | 用户指定 |
| 数据模型 | Pydantic | 类型安全、数据验证 |
| 市场数据 | yfinance | 免费、稳定 |
| Web框架 | Next.js (App Router, SSG) | Vercel原生支持 |
| 图表库 | Recharts | React生态、交互性强 |
| 样式 | Vanilla CSS | 最大灵活性 |
| 部署 | Vercel免费版 | 零成本、自动构建 |
| 版本控制 | GitHub私有仓库 | 代码+数据+自动部署 |

## .gitignore 规则

```
# 原始研报PDF（体积大，不入Git）
reports/*/originals/

# Python
__pycache__/
*.pyc
.venv/

# 临时分析文件
tmp_*.json

# Node.js
node_modules/
.next/

# 系统文件
.DS_Store
Thumbs.db
```
