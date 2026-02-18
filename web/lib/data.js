/**
 * 研报分析系统 - 数据加载工具
 * 
 * 从 data/ 目录读取 JSON 数据
 * 服务器端组件使用 fs 直接读取
 */
import fs from 'fs';
import path from 'path';

// 数据目录 — 优先使用 web/data/（Vercel构建时由prebuild脚本复制），
// 其次使用 ../data/（本地开发时）
const DATA_DIR_LOCAL = path.join(process.cwd(), 'data');
const DATA_DIR_PARENT = path.join(process.cwd(), '..', 'data');
const DATA_DIR = fs.existsSync(DATA_DIR_LOCAL) ? DATA_DIR_LOCAL : DATA_DIR_PARENT;

/**
 * 读取JSON文件
 */
function readJson(filename) {
    const filepath = path.join(DATA_DIR, filename);
    if (!fs.existsSync(filepath)) return null;
    const content = fs.readFileSync(filepath, 'utf-8');
    return JSON.parse(content);
}

/**
 * 加载所有标的列表
 */
export function loadTickers() {
    return readJson('tickers.json');
}

/**
 * 加载单个标的数据
 */
export function loadTickerData(symbol) {
    return readJson(`${symbol}.json`);
}

/**
 * 加载记分板
 */
export function loadScorecard() {
    return readJson('scorecard.json');
}

/**
 * 加载催化剂日历
 */
export function loadCatalysts() {
    return readJson('catalysts.json');
}

/**
 * 加载所有标的数据（用于首页汇总）
 */
export function loadAllTickerData() {
    const tickers = loadTickers();
    if (!tickers) return [];

    return tickers.tickers.map(t => {
        const data = loadTickerData(t.symbol);
        return {
            ...t,
            data: data || {
                ticker: t.symbol,
                current_consensus: { total_reports: 0 },
                reports: [],
                sentiment_history: [],
                cross_comparison: { consensus_matrix: {}, major_divergences: [] }
            }
        };
    });
}

/**
 * 获取评级显示文本和样式类
 */
export function getRatingInfo(rating) {
    if (!rating) return { label: '暂无', className: 'no-data' };

    const bullish = ['强买', '买入', '增持', 'buy', 'overweight', 'outperform'];
    const bearish = ['卖出', '减持', '强卖', 'sell', 'underweight', 'underperform'];

    const lower = rating.toLowerCase();
    if (bullish.some(b => lower.includes(b))) return { label: rating, className: 'buy' };
    if (bearish.some(b => lower.includes(b))) return { label: rating, className: 'sell' };
    return { label: rating, className: 'hold' };
}

/**
 * 格式化情感分数为颜色
 */
export function sentimentColor(score) {
    if (score === null || score === undefined) return 'var(--text-muted)';
    if (score > 0.3) return 'var(--green)';
    if (score < -0.3) return 'var(--red)';
    return 'var(--yellow)';
}

/**
 * 情感分数转百分比（用于进度条，-1到1转为0到100）
 */
export function sentimentToPercent(score) {
    if (score === null || score === undefined) return 50;
    return ((score + 1) / 2) * 100;
}
