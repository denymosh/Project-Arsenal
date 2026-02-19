/**
 * 催化剂日历页 — 服务器组件
 */
import { loadCatalysts, loadTickers } from '@/lib/data';
import CatalystsClient from '@/components/CatalystsClient';

export const metadata = {
    title: '催化剂日历 | 研报分析系统',
    description: '跟踪所有研报中提及的催化剂事件和时间节点',
};

export default function CatalystsPage() {
    const catalysts = loadCatalysts();
    const tickers = loadTickers();
    return <CatalystsClient catalysts={catalysts} tickers={tickers} />;
}
