"use client";
/**
 * 应用外壳 — 包含密码锁和导航栏
 */
import PasswordGate from './PasswordGate';
import Navbar from './Navbar';

export default function AppShell({ children }) {
    return (
        <PasswordGate>
            <Navbar />
            <main className="main-content">
                {children}
            </main>
        </PasswordGate>
    );
}
