"use client";
/**
 * 应用外壳 — 导航栏 + 主内容
 */
import Navbar from './Navbar';

export default function AppShell({ children }) {
    return (
        <>
            <Navbar />
            <main className="main-content">
                {children}
            </main>
        </>
    );
}
