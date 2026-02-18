import "./globals.css";

export const metadata = {
  title: "研报分析系统 | Research Report Analyzer",
  description: "多机构研报交叉验证与回溯追踪系统 — TSLA, NVDA, RKLB, ONDS, META, GOOGL",
};

export default function RootLayout({ children }) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
