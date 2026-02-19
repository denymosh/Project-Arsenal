"use client";
/**
 * 标的卡片组件 — 首页展示每个标的的概览
 */
import Link from 'next/link';

export default function TickerCard({ ticker, index }) {
    const { symbol, name_en, name_cn, sector, data } = ticker;
    const consensus = data?.current_consensus || {};
    const totalReports = consensus.total_reports || 0;
    const hasData = totalReports > 0;

    // 评级样式
    const getRatingClass = (rating) => {
        if (!rating) return 'no-data';
        const lower = rating.toLowerCase();
        if (['强买', '买入', '增持'].some(r => lower.includes(r))) return 'buy';
        if (['卖出', '减持', '强卖'].some(r => lower.includes(r))) return 'sell';
        return 'hold';
    };

    // 情感颜色
    const sentimentColor = (score) => {
        if (score === null || score === undefined) return 'var(--text-muted)';
        if (score > 0.3) return 'var(--green)';
        if (score < -0.3) return 'var(--red)';
        return 'var(--yellow)';
    };

    // 情感百分比条
    const sentimentPercent = consensus.sentiment_avg
        ? ((consensus.sentiment_avg + 1) / 2) * 100
        : 50;

    return (
        <Link
            href={`/ticker/${symbol}`}
            className={`ticker-card animate-fade-in delay-${Math.min(index + 1, 4)}`}
            id={`ticker-card-${symbol}`}
        >
            {/* 顶部: 代码 + 行业标签 */}
            <div className="ticker-card-top">
                <div>
                    <div className="ticker-symbol">{symbol}</div>
                    <div className="ticker-name">{name_cn} · {name_en}</div>
                </div>
                <span className="ticker-sector">{sector}</span>
            </div>

            {/* 指标行 */}
            {hasData ? (
                <>
                    <div className="ticker-metrics">
                        <div className="ticker-metric">
                            <div className="ticker-metric-label">共识评级</div>
                            <div className="ticker-metric-value">
                                <span className={`rating-badge ${getRatingClass(consensus.rating)}`}>
                                    {consensus.rating || '—'}
                                </span>
                            </div>
                        </div>
                        <div className="ticker-metric">
                            <div className="ticker-metric-label">目标均价</div>
                            <div className="ticker-metric-value mono">
                                {consensus.avg_target_price
                                    ? `$${consensus.avg_target_price.toFixed(0)}`
                                    : '—'}
                            </div>
                        </div>
                        <div className="ticker-metric">
                            <div className="ticker-metric-label">研报数</div>
                            <div className="ticker-metric-value mono">{totalReports}</div>
                        </div>
                    </div>

                    {/* 情感条 */}
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.7rem', color: 'var(--text-muted)' }}>
                        <span>看空</span>
                        <span style={{ color: sentimentColor(consensus.sentiment_avg), fontWeight: 700, fontFamily: 'var(--font-mono)' }}>
                            {consensus.sentiment_avg !== null && consensus.sentiment_avg !== undefined
                                ? (consensus.sentiment_avg > 0 ? '+' : '') + consensus.sentiment_avg.toFixed(2)
                                : '—'}
                        </span>
                        <span>看多</span>
                    </div>
                    <div className="sentiment-bar-container">
                        <div
                            className="sentiment-bar"
                            style={{
                                width: `${sentimentPercent}%`,
                                background: `linear-gradient(90deg, var(--red) 0%, var(--yellow) 50%, var(--green) 100%)`
                            }}
                        />
                    </div>
                </>
            ) : (
                <div className="empty-state" style={{ padding: '24px 0' }}>
                    <div style={{ fontSize: '1.5rem', marginBottom: '8px' }}>📭</div>
                    <p style={{ fontSize: '0.8rem' }}>暂无研报数据</p>
                </div>
            )}
        </Link>
    );
}
