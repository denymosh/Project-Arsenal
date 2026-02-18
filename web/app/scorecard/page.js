/**
 * 记分板页面 — 服务器组件
 */
import { loadScorecard } from '@/lib/data';
import ScorecardClient from '@/components/ScorecardClient';

export const metadata = {
    title: '机构记分板 | 研报分析系统',
    description: '机构分析师的历史预测准确率排行和可靠度评估',
};

export default function ScorecardPage() {
    const scorecard = loadScorecard();
    return <ScorecardClient scorecard={scorecard} />;
}
