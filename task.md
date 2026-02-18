# 研报分析系统 - 任务进度

## 当前状态: 阶段三 - Web仪表盘（阶段一✅ 阶段二✅）

## 方案决策记录

| 日期 | 决策 | 说明 |
|------|------|------|
| 2026-02-17 | 采用"本地AI + Vercel Web"方案 | Antigravity当AI分析层，Vercel免费版部署静态Web仪表盘 |
| 2026-02-17 | Antigravity即AI层 | 不需要单独AI API，用户在Antigravity选什么模型就用什么分析 |
| 2026-02-17 | Python脚本只管数据 | 不调用AI API，只负责: 读写JSON、共识计算、MD生成、回溯验证、git push |
| 2026-02-17 | 关注6个标的 | TSLA, NVDA, RKLB, ONDS, META, GOOGL |
| 2026-02-17 | 无API Key依赖 | 零成本运行 |
| 2026-02-17 | 前端图表用Recharts | Python只输出JSON，前端用Recharts渲染交互式图表 |
| 2026-02-17 | PDF不入Git | .gitignore排除originals/，只推JSON和MD |
| 2026-02-17 | "打脸"分析 + 靠谱度权重 | 机构历史准确率影响分析参考权重 |
| 2026-02-17 | 纯SSG构建 | 按标的分割JSON，6个标的规模SSG足够 |

## 任务清单

### 阶段一：基础设施搭建 ✅
- [x] 1. 确定技术方案和架构
- [x] 2. 编写实施计划 (implementation_plan.md)
- [x] 3. 创建项目目录结构（所有标的文件夹 + 子目录）
- [x] 4. 初始化Python项目（uv + pyproject.toml）
- [ ] 5. 初始化Next.js项目（App Router + Recharts）⬅️ 下一步
- [x] 6. 创建初始JSON数据文件（空结构 + Schema）
- [x] 7. 编写分析报告MD模板（report_generator.py内置）
- [x] 8. 配置.gitignore

### 阶段二：本地数据管理工具 ✅
- [x] 9. 实现数据模型定义 (models.py - Pydantic)
- [x] 10. 实现JSON数据读写管理 (data_manager.py)
- [x] 11. 实现上下文加载脚本 (load_context.py)
- [x] 12. 实现分析保存脚本 (save_analysis.py)
- [x] 13. 实现共识计算模块 (consensus.py)
- [x] 14. 实现交叉验证数据准备 (cross_validator.py)
- [x] 15. 实现分析报告MD生成 (report_generator.py)
- [x] 16. 实现市场数据拉取 (market_data.py)
- [x] 17. 实现回溯验证引擎 (backtest_engine.py + backtest.py)
- [x] 18. 实现自动git push (auto_push.py)
- [x] 19. 端到端测试 ✅ 模拟高盛TSLA研报走通全流程
- [x] 19b. 新增ChartInsight模型 — 支持PDF图表视觉洞察结构化存储
- [x] 19c. 新增extract_images.py — PDF图片批量提取工具
- [x] 19d. report_generator.py增加📈图表视觉洞察章节渲染
- [x] 19e. GOOGL三篇研报补充11条图表洞察（Morningstar 2条 + ISS EVA 6条 + STD 3条）

### 阶段三：Web仪表盘
- [ ] 20. 设计全局样式和设计系统（深色主题、CSS变量）
- [ ] 21. 实现密码锁组件 (PasswordGate.js)
- [ ] 22. 实现全局布局和导航 (Layout, Navbar)
- [ ] 23. 实现首页Dashboard - 标的卡片 + 情绪仪表盘
- [ ] 24. 实现首页Dashboard - 总览统计
- [ ] 25. 实现单标的深度视图 - 观点热力图 (ViewsHeatmap)
- [ ] 26. 实现单标的深度视图 - 研报时间线 (ReportTimeline)
- [ ] 27. 实现单标的深度视图 - 目标价vs现价图 (TargetPriceChart)
- [ ] 28. 实现单标的深度视图 - 分歧分析面板 (DivergencePanel)
- [ ] 29. 实现单标的深度视图 - 预测追踪表格 (PredictionTracker)
- [ ] 30. 实现回溯验证记分板 - 准确率排行 (AccuracyTable)
- [ ] 31. 实现回溯验证记分板 - "靠谱度"徽章 (ReliabilityBadge)
- [ ] 32. 实现回溯验证记分板 - 已验证观点列表 (VerifiedList)
- [ ] 33. 实现催化剂日历 (CatalystCalendar)
- [ ] 34. 响应式设计优化

### 阶段四：部署和联调
- [ ] 35. 初始化GitHub私有仓库
- [ ] 36. 配置Vercel部署（连接GitHub）
- [ ] 37. 构建时数据注入流程验证
- [ ] 38. 端到端全流程测试
- [ ] 39. 编写使用文档 (README.md)

### 阶段五：自动化增强（后期）
- [ ] 40. Watchdog 文件夹监控（新PDF自动触发）
- [ ] 41. 定时回溯验证（财报日自动触发）

## 备注
- AI分析层: 由Antigravity直接承担，用户选什么模型就用什么模型
- Python脚本: 纯数据管理工具，不调用任何AI API
- 优先级: 阶段二（数据工具）> 阶段三（Web仪表盘）
- 阶段二完成后即可开始实际分析研报
