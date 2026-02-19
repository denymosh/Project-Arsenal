"use client";
/**
 * 机构记分板客户端组件
 */
import AppShell from '@/components/AppShell';

// 可靠度徽章
function ReliabilityBadge({ score }) {
    if (score === null || score === undefined) {
        return <span className="tag" style={{ color: 'var(--text-muted)' }}>待评估</span>;
    }

    const pct = Math.round(score * 100);
    let color, label;
    if (pct >= 80) { color = 'var(--green)'; label = '极可靠'; }
    else if (pct >= 60) { color = 'var(--blue)'; label = '可靠'; }
    else if (pct >= 40) { color = 'var(--yellow)'; label = '一般'; }
    else { color = 'var(--red)'; label = '不可靠'; }

    return (
        <span style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '6px',
            padding: '4px 12px',
            borderRadius: '99px',
            fontSize: '0.75rem',
            fontWeight: 700,
            color: color,
            background: `${color}15`,
            border: `1px solid ${color}30`,
        }}>
            {pct}% {label}
        </span>
    );
}

export default function ScorecardClient({ scorecard }) {
    const institutions = scorecard?.institutions || [];

    return (
        <AppShell>
            <div className="page-header animate-fade-in">
                <h1>🏆 机构记分板</h1>
                <div className="subtitle">
                    {institutions.length} 家机构 · 基于历史预测准确率的可靠度排名
                </div>
            </div>

            {institutions.length === 0 ? (
                <div className="empty-state animate-fade-in">
                    <div className="emoji">📊</div>
                    <p>暂无机构评分数据，需要更多研报和回溯验证结果</p>
                </div>
            ) : (
                <div className="card animate-fade-in delay-1" style={{ overflow: 'auto' }}>
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th>排名</th>
                                <th>机构</th>
                                <th>英文名</th>
                                <th>研报总数</th>
                                <th>准确预测</th>
                                <th>准确率</th>
                                <th>可靠度</th>
                            </tr>
                        </thead>
                        <tbody>
                            {institutions
                                .sort((a, b) => (b.accuracy || 0) - (a.accuracy || 0))
                                .map((inst, i) => (
                                    <tr key={inst.name_cn || inst.name_en || i}>
                                        <td style={{ fontWeight: 700, color: i < 3 ? 'var(--yellow)' : 'var(--text-muted)' }}>
                                            {i < 3 ? ['🥇', '🥈', '🥉'][i] : `#${i + 1}`}
                                        </td>
                                        <td style={{ fontWeight: 600 }}>{inst.name_cn || inst.name}</td>
                                        <td className="text-muted">{inst.name_en || ''}</td>
                                        <td className="mono">{inst.total_reports || 0}</td>
                                        <td className="mono">{inst.accurate_calls || 0}</td>
                                        <td className="mono" style={{
                                            fontWeight: 700,
                                            color: (inst.accuracy || 0) >= 0.7 ? 'var(--green)' : (inst.accuracy || 0) >= 0.4 ? 'var(--yellow)' : 'var(--red)'
                                        }}>
                                            {inst.accuracy !== null && inst.accuracy !== undefined
                                                ? `${Math.round(inst.accuracy * 100)}%`
                                                : '—'}
                                        </td>
                                        <td><ReliabilityBadge score={inst.reliability} /></td>
                                    </tr>
                                ))}
                        </tbody>
                    </table>
                </div>
            )}
        </AppShell>
    );
}
