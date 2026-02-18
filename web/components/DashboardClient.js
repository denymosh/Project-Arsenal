"use client";
/**
 * 首页Dashboard客户端包装器
 */
import AppShell from '@/components/AppShell';
import TickerCard from '@/components/TickerCard';

export default function DashboardClient({ tickers, catalysts, scorecard }) {
    // 汇总统计
    const totalReports = tickers.reduce((sum, t) => sum + (t.data?.current_consensus?.total_reports || 0), 0);
    const tickersWithData = tickers.filter(t => (t.data?.current_consensus?.total_reports || 0) > 0);
    const avgSentiment = tickersWithData.length > 0
        ? tickersWithData.reduce((sum, t) => sum + (t.data.current_consensus.sentiment_avg || 0), 0) / tickersWithData.length
        : null;
    const totalCatalysts = catalysts?.catalysts?.length || 0;
    const totalInstitutions = scorecard?.institutions?.length || 0;

    // 即将到来的催化剂（未来30天）
    const now = new Date();
    const upcoming = (catalysts?.catalysts || [])
        .filter(c => {
            const d = new Date(c.date);
            return d >= now && (d - now) < 30 * 24 * 3600 * 1000;
        })
        .sort((a, b) => new Date(a.date) - new Date(b.date))
        .slice(0, 5);

    return (
        <AppShell>
            {/* 页头 */}
            <div className="page-header animate-fade-in">
                <h1>📊 研报分析总览</h1>
                <div className="subtitle">
                    跟踪 {tickers.length} 个标的 · {totalReports} 篇研报 · {totalInstitutions} 家机构
                </div>
            </div>

            {/* 统计卡片 */}
            <div className="stats-grid">
                <div className="stat-card animate-fade-in delay-1">
                    <div className="stat-label">跟踪标的</div>
                    <div className="stat-value">{tickers.length}</div>
                    <div className="stat-change positive">{tickersWithData.length} 有分析数据</div>
                </div>
                <div className="stat-card animate-fade-in delay-2">
                    <div className="stat-label">研报总数</div>
                    <div className="stat-value mono">{totalReports}</div>
                </div>
                <div className="stat-card animate-fade-in delay-3">
                    <div className="stat-label">综合情绪</div>
                    <div className="stat-value" style={{ color: avgSentiment > 0.3 ? 'var(--green)' : avgSentiment < -0.3 ? 'var(--red)' : 'var(--yellow)' }}>
                        {avgSentiment !== null ? (avgSentiment > 0 ? '+' : '') + avgSentiment.toFixed(2) : '—'}
                    </div>
                </div>
                <div className="stat-card animate-fade-in delay-4">
                    <div className="stat-label">待验证催化剂</div>
                    <div className="stat-value mono">{totalCatalysts}</div>
                    <div className="stat-change positive">{upcoming.length} 个即将到来</div>
                </div>
            </div>

            {/* 标的卡片网格 */}
            <div className="section">
                <div className="section-title">
                    <span className="icon">🎯</span> 标的概览
                </div>
                <div className="ticker-grid">
                    {tickers.map((ticker, i) => (
                        <TickerCard key={ticker.symbol} ticker={ticker} index={i} />
                    ))}
                </div>
            </div>

            {/* 即将到来的催化剂 */}
            {upcoming.length > 0 && (
                <div className="section animate-fade-in">
                    <div className="section-title">
                        <span className="icon">📅</span> 即将到来的催化剂
                    </div>
                    {upcoming.map((c, i) => {
                        const d = new Date(c.date);
                        const months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
                        return (
                            <div key={c.id || i} className="catalyst-item">
                                <div className="catalyst-date-box">
                                    <div className="month">{months[d.getMonth()]}</div>
                                    <div className="day">{d.getDate()}</div>
                                </div>
                                <div className="catalyst-details">
                                    <div className="catalyst-event">
                                        <span className={`importance-dot ${c.importance}`}></span>
                                        {c.event}
                                    </div>
                                    <div className="catalyst-meta">
                                        <span className="tag">{c.ticker}</span>
                                        <span>{c.importance === 'high' ? '🔴 高' : c.importance === 'medium' ? '🟡 中' : '🟢 低'}</span>
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                </div>
            )}
        </AppShell>
    );
}
