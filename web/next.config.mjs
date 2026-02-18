/** @type {import('next').NextConfig} */
const nextConfig = {
  /* 
   * Vercel部署配置
   * - 纯SSG静态导出，零服务器成本
   * - 数据在构建时通过 getStaticProps/SSG 内嵌
   */

  // 禁用图片优化（无外部图片服务器）
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
