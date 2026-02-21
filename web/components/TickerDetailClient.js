"use client";
/**
 * 标的详情页客户端组件
 * 包含: 观点热力图 + 研报时间线 + 目标价图 + 分歧面板 + 预测追踪 + 图表洞察
 */
import React from 'react';
import AppShell from '@/components/AppShell';
import Link from 'next/link';
import {
    BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
    ReferenceLine, Cell, ScatterChart, Scatter, CartesianGrid
} from 'recharts';

function normalizeInstitution(name) {
    return (name || '').toString().trim().toLowerCase();
}

function getLatestReportsByInstitution(reports) {
    const sorted = [...(reports || [])].sort((a, b) => new Date(b.date) - new Date(a.date));
    const seen = new Set();
    const latest = [];

    sorted.forEach((report) => {
        const key = normalizeInstitution(report.institution);
        if (!key || seen.has(key)) return;
        seen.add(key);
        latest.push(report);
    });

    return latest;
}

// ========== 观点热力图 ==========
function normalizeTopic(topic) {
    const t = (topic || '').toString();
    if (!t) return null;
    if (t.includes('数据中心')) return '数据中心';
    if (t.includes('AI芯片') || t.includes('gpu') || t.includes('GPU')) return 'AI芯片';
    if (t.includes('游戏')) return '游戏';
    if (t.includes('汽车')) return '汽车';
    if (t.includes('毛利率') || t.includes('利润率') || t.includes('盈利能力')) return '毛利率';
    if (t.includes('估值') || t.includes('prvit') || t.includes('PRVit') || t.includes('未来增长')) return '估值';
    if (t.includes('行业周期')) return '行业周期';
    return null;
}

function ViewsHeatmap({ reports }) {
    if (!reports || reports.length === 0) return null;

    const stanceMap = {
        bullish: { label: '看多', cls: 'bullish' },
        neutral: { label: '中性', cls: 'neutral' },
        bearish: { label: '看空', cls: 'bearish' },
    };

    const mappedReports = reports.map((report) => {
        const mapped = [];
        const seen = new Set();
        (report.views || []).forEach((v) => {
            const dim = normalizeTopic(v.topic);
            if (!dim || seen.has(dim)) return;
            seen.add(dim);
            mapped.push({ ...v, topic: dim });
        });
        return { ...report, views: mapped };
    });

    const dimCount = {};
    mappedReports.forEach((r) => {
        (r.views || []).forEach((v) => {
            dimCount[v.topic] = (dimCount[v.topic] || 0) + 1;
        });
    });

    const dimensions = Object.keys(dimCount)
        .filter((dim) => dimCount[dim] >= 2)
        .sort();

    if (dimensions.length === 0) return null;

    const institutions = mappedReports.map(r => r.institution);

    return (
        <div className="card section">
            <div className="section-title"><span className="icon">🔥</span> 观点热力图（可比维度）</div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '8px' }}>
                仅展示至少被 2 家机构覆盖的维度，非同口径内容自动归入时间线。
            </div>
            <div style={{ overflowX: 'auto' }}>
                <div
                    className="heatmap-grid"
                    style={{
                        gridTemplateColumns: `140px repeat(${institutions.length}, 1fr)`,
                    }}
                >
                    <div className="heatmap-cell header">维度</div>
                    {institutions.map((inst, i) => (
                        <div key={i} className="heatmap-cell header">{inst}</div>
                    ))}

                    {dimensions.map(dim => (
                        <React.Fragment key={dim}>
                            <div className="heatmap-cell header" style={{ textAlign: 'left', fontWeight: 600 }}>
                                {dim}
                            </div>
                            {mappedReports.map((report, ri) => {
                                const view = report.views?.find(v => v.topic === dim);
                                if (!view) {
                                    return <div key={`${dim}-${ri}`} className="heatmap-cell" style={{ color: 'var(--text-muted)', fontSize: '0.7rem' }}>—</div>;
                                }
                                const stance = stanceMap[view.stance] || { label: view.stance, cls: '' };
                                return (
                                    <div
                                        key={`${dim}-${ri}`}
                                        className={`heatmap-cell ${stance.cls}`}
                                        title={view.summary}
                                    >
                                        {stance.label}
                                    </div>
                                );
                            })}
                        </React.Fragment>
                    ))}
                </div>
            </div>
        </div>
    );
}

// ========== 研报时间线 ==========
function ReportTimeline({ reports }) {
    if (!reports || reports.length === 0) return null;

    const sorted = [...reports].sort((a, b) => new Date(b.date) - new Date(a.date));

    const getRatingClass = (rating) => {
        if (!rating) return 'no-data';
        const lower = rating.toLowerCase();
        if (['强买', '买入', '增持'].some(r => lower.includes(r))) return 'buy';
        if (['卖出', '减持', '强卖'].some(r => lower.includes(r))) return 'sell';
        return 'hold';
    };

    return (
        <div className="card section">
            <div className="section-title"><span className="icon">📜</span> 研报时间线</div>
            <div className="timeline">
                {sorted.map((report, i) => (
                    <div key={report.id || i} className="timeline-item">
                        <div className="timeline-date">{report.date}</div>
                        <div className="timeline-institution">{report.institution}</div>
                        <div className="timeline-rating" style={{ marginTop: '4px' }}>
                            <span className={`rating-badge ${getRatingClass(report.rating)}`}>
                                {report.rating}
                            </span>
                            <span style={{ marginLeft: '8px', fontFamily: 'var(--font-mono)', fontWeight: 700 }}>
                                ${report.target_price}
                            </span>
                            <span style={{
                                marginLeft: '12px',
                                fontFamily: 'var(--font-mono)',
                                fontWeight: 600,
                                color: report.sentiment_score > 0.3 ? 'var(--green)' : report.sentiment_score < -0.3 ? 'var(--red)' : 'var(--yellow)'
                            }}>
                                {report.sentiment_score > 0 ? '+' : ''}{report.sentiment_score.toFixed(2)}
                            </span>
                        </div>
                        {report.views && report.views.length > 0 && (
                            <div style={{ marginTop: '8px', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                                {report.views.slice(0, 2).map((v, vi) => (
                                    <div key={vi} style={{ marginTop: '4px' }}>
                                        <span style={{
                                            color: v.stance === 'bullish' ? 'var(--green)' : v.stance === 'bearish' ? 'var(--red)' : 'var(--yellow)',
                                            fontWeight: 600
                                        }}>
                                            {v.stance === 'bullish' ? '🟢' : v.stance === 'bearish' ? '🔴' : '🟡'} {v.topic}
                                        </span>
                                        : {v.summary.substring(0, 80)}...
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
}

// ========== 目标价分布图 ==========
function TargetPriceChart({ reports, consensus }) {
    if (!reports || reports.length === 0) return null;

    const chartData = reports.map(r => ({
        name: `${r.institution} (${r.date || 'N/A'})`,
        target: r.target_price,
        sentiment: r.sentiment_score,
    }));

    const avg = consensus?.avg_target_price || 0;

    return (
        <div className="chart-container">
            <div className="chart-title">目标价分布</div>
            <ResponsiveContainer width="100%" height={200}>
                <BarChart data={chartData} layout="vertical" margin={{ left: 80, right: 20, top: 5, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                    <XAxis type="number" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                    <YAxis type="category" dataKey="name" tick={{ fill: '#94a3b8', fontSize: 12 }} width={80} />
                    <Tooltip
                        contentStyle={{ background: '#1e293b', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', fontSize: '0.85rem' }}
                        labelStyle={{ color: '#f1f5f9' }}
                    />
                    {avg > 0 && <ReferenceLine x={avg} stroke="#818cf8" strokeDasharray="5 5" label={{ value: `均值$${avg.toFixed(0)}`, fill: '#818cf8', fontSize: 11 }} />}
                    <Bar dataKey="target" radius={[0, 4, 4, 0]}>
                        {chartData.map((entry, i) => (
                            <Cell
                                key={i}
                                fill={entry.sentiment > 0.3 ? '#10b981' : entry.sentiment < -0.3 ? '#ef4444' : '#f59e0b'}
                                fillOpacity={0.8}
                            />
                        ))}
                    </Bar>
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}

// ========== 分歧面板 ==========
function DivergencePanel({ divergences }) {
    if (!divergences || divergences.length === 0) {
        return (
            <div className="card section">
                <div className="section-title"><span className="icon">⚡</span> 分歧分析</div>
                <div className="empty-state" style={{ padding: '16px 0' }}>
                    <p style={{ fontSize: '0.85rem' }}>✅ 各机构观点基本一致，暂无重大分歧</p>
                </div>
            </div>
        );
    }

    return (
        <div className="card section">
            <div className="section-title"><span className="icon">⚡</span> 分歧分析</div>
            {divergences.map((d, i) => (
                <div key={i} className={`divergence-item ${d.severity}`}>
                    <div style={{ fontWeight: 700, marginBottom: '4px' }}>
                        {d.severity === 'major' ? '🔴' : d.severity === 'moderate' ? '🟡' : '🟢'} {d.topic}
                    </div>
                    <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '4px' }}>
                        {d.description || ''}
                    </div>
                    <div style={{ display: 'flex', gap: '16px', fontSize: '0.8rem' }}>
                        {d.bulls && d.bulls.length > 0 && (
                            <span><span className="text-green font-bold">看多:</span> {d.bulls.join(', ')}</span>
                        )}
                        {d.bears && d.bears.length > 0 && (
                            <span><span className="text-red font-bold">看空:</span> {d.bears.join(', ')}</span>
                        )}
                    </div>
                </div>
            ))}
        </div>
    );
}

// ========== 预测追踪 ==========
function PredictionTracker({ reports }) {
    // 收集所有预测
    const allPredictions = [];
    (reports || []).forEach(r => {
        (r.views || []).forEach(v => {
            (v.predictions || []).forEach(p => {
                allPredictions.push({
                    ...p,
                    institution: r.institution,
                    topic: v.topic,
                });
            });
        });
    });

    if (allPredictions.length === 0) return null;

    return (
        <div className="card section">
            <div className="section-title"><span className="icon">🎯</span> 预测追踪</div>
            <div style={{ overflowX: 'auto' }}>
                <table className="data-table">
                    <thead>
                        <tr>
                            <th>机构</th>
                            <th>维度</th>
                            <th>指标</th>
                            <th>预测值</th>
                            <th>验证期限</th>
                            <th>状态</th>
                        </tr>
                    </thead>
                    <tbody>
                        {allPredictions.map((p, i) => {
                            const statusIcon = p.accurate === true ? '✅' : p.accurate === false ? '❌' : '⏳';
                            const consensusIcon = p.comparison_to_consensus === 'above' ? '⬆️' : p.comparison_to_consensus === 'below' ? '⬇️' : '➡️';
                            return (
                                <tr key={i}>
                                    <td style={{ fontWeight: 600 }}>{p.institution}</td>
                                    <td><span className="tag">{p.topic}</span></td>
                                    <td>{p.metric}</td>
                                    <td className="mono font-bold">{p.predicted_value}</td>
                                    <td className="mono" style={{ fontSize: '0.8rem' }}>{p.deadline}</td>
                                    <td>{statusIcon} {consensusIcon}</td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

// ========== 图表洞察面板 ==========
function ChartInsightsPanel({ reports }) {
    // 收集所有图表洞察
    const allInsights = [];
    (reports || []).forEach(r => {
        (r.chart_insights || []).forEach(ci => {
            allInsights.push({ ...ci, institution: r.institution });
        });
    });

    if (allInsights.length === 0) return null;

    const typeIcons = {
        line: '📉', bar: '📊', scatter: '🔵', heatmap: '🟥', table: '📋', flow: '🔄'
    };

    return (
        <div className="card section">
            <div className="section-title"><span className="icon">📈</span> 图表视觉洞察 ({allInsights.length})</div>
            <div style={{ display: 'grid', gap: '12px' }}>
                {allInsights.map((ci, i) => (
                    <div key={i} className="card" style={{ padding: '16px', background: 'var(--bg-glass)' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                            <span style={{ fontSize: '1.2rem' }}>{typeIcons[ci.chart_type] || '📊'}</span>
                            <span style={{ fontWeight: 700, fontSize: '0.9rem' }}>{ci.chart_name}</span>
                            <span className="tag" style={{ marginLeft: 'auto' }}>{ci.institution}</span>
                        </div>
                        <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '8px' }}>
                            {ci.description}
                        </p>
                        {ci.key_observations && ci.key_observations.length > 0 && (
                            <div style={{ marginBottom: '8px' }}>
                                <div style={{ fontSize: '0.7rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '4px' }}>关键视觉信号</div>
                                {ci.key_observations.slice(0, 3).map((obs, oi) => (
                                    <div key={oi} style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', padding: '2px 0' }}>
                                        👁️ {obs}
                                    </div>
                                ))}
                            </div>
                        )}
                        {ci.investment_implication && (
                            <div style={{
                                fontSize: '0.8rem',
                                padding: '8px 12px',
                                background: 'var(--purple-dim)',
                                borderRadius: '6px',
                                color: 'var(--text-primary)',
                                borderLeft: '3px solid var(--purple)'
                            }}>
                                💡 {ci.investment_implication}
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
}

// ========== 共识矩阵 ==========
function ConsensusMatrix({ matrix }) {
    if (!matrix || Object.keys(matrix).length === 0) return null;

    return (
        <div className="card section">
            <div className="section-title"><span className="icon">🔥</span> 共识矩阵</div>
            <table className="data-table">
                <thead>
                    <tr>
                        <th>维度</th>
                        <th>🟢 看多</th>
                        <th>🟡 中性</th>
                        <th>🔴 看空</th>
                        <th>未提及</th>
                    </tr>
                </thead>
                <tbody>
                    {Object.entries(matrix).map(([dim, counts]) => {
                        const total = counts.bullish + counts.neutral + counts.bearish;
                        const dominant = Math.max(counts.bullish, counts.neutral, counts.bearish);
                        return (
                            <tr key={dim}>
                                <td style={{ fontWeight: 600 }}>{dim}</td>
                                <td className="text-green font-bold">{counts.bullish || '—'}</td>
                                <td className="text-yellow font-bold">{counts.neutral || '—'}</td>
                                <td className="text-red font-bold">{counts.bearish || '—'}</td>
                                <td className="text-muted">{counts.not_mentioned || 0}</td>
                            </tr>
                        );
                    })}
                </tbody>
            </table>
        </div>
    );
}

// ========== 主组件 ==========
export default function TickerDetailClient({ tickerInfo, tickerData }) {
    const consensus = tickerData?.current_consensus || {};
    const reports = tickerData?.reports || [];
    const latestReports = getLatestReportsByInstitution(reports);
    const dimensions = tickerData?.view_dimensions || tickerInfo?.default_dimensions || [];
    const crossComparison = tickerData?.cross_comparison || {};

    const sentimentColor = (score) => {
        if (score > 0.3) return 'var(--green)';
        if (score < -0.3) return 'var(--red)';
        return 'var(--yellow)';
    };

    const getRatingClass = (rating) => {
        if (!rating) return 'no-data';
        const lower = rating.toLowerCase();
        if (['强买', '买入', '增持'].some(r => lower.includes(r))) return 'buy';
        if (['卖出', '减持', '强卖'].some(r => lower.includes(r))) return 'sell';
        return 'hold';
    };

    const hasData = reports.length > 0;

    return (
        <AppShell>
            {/* 页头 */}
            <div className="page-header animate-fade-in">
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '4px' }}>
                    <Link href="/" style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>← 返回总览</Link>
                </div>
                <div style={{ display: 'flex', alignItems: 'baseline', gap: '12px' }}>
                    <h1>{tickerInfo?.symbol || tickerData?.ticker}</h1>
                    <span style={{ fontSize: '1rem', color: 'var(--text-secondary)' }}>
                        {tickerInfo?.name_cn || tickerData?.name_cn} · {tickerInfo?.name_en || tickerData?.name_en}
                    </span>
                </div>
                {tickerInfo?.sector && <span className="ticker-sector">{tickerInfo.sector}</span>}
            </div>

            {!hasData ? (
                <div className="empty-state animate-fade-in">
                    <div className="emoji">📭</div>
                    <p>暂无研报数据，请先分析研报后再查看</p>
                </div>
            ) : (
                <>
                    {/* 概览统计 */}
                    <div className="stats-grid animate-fade-in delay-1">
                        <div className="stat-card">
                            <div className="stat-label">共识评级</div>
                            <div className="stat-value">
                                <span className={`rating-badge ${getRatingClass(consensus.rating)}`} style={{ fontSize: '1.1rem' }}>
                                    {consensus.rating}
                                </span>
                            </div>
                        </div>
                        <div className="stat-card">
                            <div className="stat-label">平均目标价</div>
                            <div className="stat-value mono">${consensus.avg_target_price?.toFixed(0) || '—'}</div>
                            {consensus.min_target_price && (
                                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                                    区间: ${consensus.min_target_price} - ${consensus.max_target_price}
                                </div>
                            )}
                        </div>
                        <div className="stat-card">
                            <div className="stat-label">情感均值</div>
                            <div className="stat-value mono" style={{ color: sentimentColor(consensus.sentiment_avg) }}>
                                {consensus.sentiment_avg !== null && consensus.sentiment_avg !== undefined
                                    ? (consensus.sentiment_avg > 0 ? '+' : '') + consensus.sentiment_avg.toFixed(2)
                                    : '—'}
                            </div>
                        </div>
                        <div className="stat-card">
                            <div className="stat-label">研报数量</div>
                            <div className="stat-value mono">{consensus.total_reports || 0}</div>
                        </div>
                    </div>

                    {/* 目标价图表 */}
                    <TargetPriceChart reports={latestReports} consensus={consensus} />

                    {/* 观点热力图 */}
                    <ViewsHeatmap reports={latestReports} />

                    {/* 共识矩阵 */}
                    <ConsensusMatrix matrix={crossComparison.consensus_matrix} />

                    {/* 分歧面板 */}
                    <DivergencePanel divergences={crossComparison.major_divergences} />

                    {/* 两列布局: 时间线 + 图表洞察 */}
                    <div className="grid-2">
                        <ReportTimeline reports={reports} />
                        <ChartInsightsPanel reports={reports} />
                    </div>

                    {/* 预测追踪 */}
                    <PredictionTracker reports={reports} />
                </>
            )}
        </AppShell>
    );
}
