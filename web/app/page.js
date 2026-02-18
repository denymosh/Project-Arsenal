/**
 * 首页 — 研报分析总览Dashboard
 * 服务器组件：从文件系统加载数据，传递给客户端组件
 */
import { loadAllTickerData, loadCatalysts, loadScorecard } from '@/lib/data';
import DashboardClient from '@/components/DashboardClient';

export default function HomePage() {
  const tickers = loadAllTickerData();
  const catalysts = loadCatalysts();
  const scorecard = loadScorecard();

  return (
    <DashboardClient
      tickers={tickers}
      catalysts={catalysts}
      scorecard={scorecard}
    />
  );
}
