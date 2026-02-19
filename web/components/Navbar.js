"use client";
/**
 * 导航栏组件
 */
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Navbar() {
    const pathname = usePathname();

    const links = [
        { href: '/', label: '总览' },
        { href: '/catalysts', label: '催化剂' },
        { href: '/scorecard', label: '记分板' },
    ];

    return (
        <nav className="navbar">
            <Link href="/" className="navbar-brand">
                <span className="logo-icon">📊</span>
                <span>研报分析</span>
            </Link>
            <div className="navbar-links">
                {links.map(link => (
                    <Link
                        key={link.href}
                        href={link.href}
                        className={pathname === link.href ? 'active' : ''}
                    >
                        {link.label}
                    </Link>
                ))}
            </div>
        </nav>
    );
}
