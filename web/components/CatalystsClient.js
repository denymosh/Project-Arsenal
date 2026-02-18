"use client";
/**
 * 催化剂日历客户端组件
 */
import AppShell from '@/components/AppShell';

export default function CatalystsClient({ catalysts, tickers }) {
    const allCatalysts = (catalysts?.catalysts || [])
        .sort((a, b) => new Date(a.date) - new Date(b.date));

    const months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];

    // 按月分组
    const grouped = {};
    allCatalysts.forEach(c => {
        const key = c.date.substring(0, 7); // YYYY-MM
        if (!grouped[key]) grouped[key] = [];
        grouped[key].push(c);
    });

    return (
        <AppShell>
            <div className="page-header animate-fade-in">
                <h1>📅 催化剂日历</h1>
                <div className="subtitle">
                    共 {allCatalysts.length} 个催化剂事件
                </div>
            </div>

            {Object.keys(grouped).length === 0 ? (
                <div className="empty-state animate-fade-in">
                    <div className="emoji">📭</div>
                    <p>暂无催化剂事件</p>
                </div>
            ) : (
                Object.entries(grouped).map(([monthKey, items]) => {
                    const [year, month] = monthKey.split('-');
                    return (
                        <div key={monthKey} className="section animate-fade-in">
                            <div className="section-title">
                                <span className="icon">📆</span>
                                {year}年{parseInt(month)}月
                            </div>
                            {items.map((c, i) => {
                                const d = new Date(c.date);
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
                                                <span>{c.institution || ''}</span>
                                                <span>{c.importance === 'high' ? '🔴 高' : c.importance === 'medium' ? '🟡 中' : '🟢 低'}</span>
                                                {c.related_views && c.related_views.length > 0 && (
                                                    <span>| {c.related_views.join(', ')}</span>
                                                )}
                                            </div>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    );
                })
            )}
        </AppShell>
    );
}
