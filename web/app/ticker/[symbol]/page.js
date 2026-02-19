/**
 * 标的详情页 — 服务器组件
 * 路由: /ticker/[symbol]
 */
import { loadTickers, loadTickerData } from '@/lib/data';
import TickerDetailClient from '@/components/TickerDetailClient';
import { notFound } from 'next/navigation';

// 生成静态路径（SSG）
export async function generateStaticParams() {
    const tickers = loadTickers();
    if (!tickers) return [];
    return tickers.tickers.map(t => ({ symbol: t.symbol }));
}

// 动态元数据
export async function generateMetadata({ params }) {
    const { symbol } = await params;
    const tickers = loadTickers();
    const info = tickers?.tickers?.find(t => t.symbol === symbol);
    return {
        title: `${symbol} ${info?.name_cn || ''} | 研报分析`,
        description: `${symbol} (${info?.name_en || ''}) 研报交叉分析与预测追踪`,
    };
}

export default async function TickerDetailPage({ params }) {
    const { symbol } = await params;
    const tickers = loadTickers();
    const tickerInfo = tickers?.tickers?.find(t => t.symbol === symbol);

    if (!tickerInfo) notFound();

    const tickerData = loadTickerData(symbol);

    return (
        <TickerDetailClient
            tickerInfo={tickerInfo}
            tickerData={tickerData || { ticker: symbol, reports: [], current_consensus: {}, cross_comparison: {} }}
        />
    );
}
