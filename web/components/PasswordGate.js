"use client";
/**
 * 密码锁组件 — 简单的前端访问控制
 * 密码: 6868 (发发)
 */
import { useState, useEffect } from 'react';

const CORRECT_PIN = '6868';
const STORAGE_KEY = 'rr_auth';

export default function PasswordGate({ children }) {
    const [authed, setAuthed] = useState(false);
    const [pin, setPin] = useState('');
    const [error, setError] = useState(false);
    const [checking, setChecking] = useState(true);

    useEffect(() => {
        // 检查本地存储
        const saved = localStorage.getItem(STORAGE_KEY);
        if (saved === 'true') {
            setAuthed(true);
        }
        setChecking(false);
    }, []);

    const handleSubmit = (value) => {
        if (value === CORRECT_PIN) {
            localStorage.setItem(STORAGE_KEY, 'true');
            setAuthed(true);
            setError(false);
        } else if (value.length >= 4) {
            setError(true);
            setPin('');
            setTimeout(() => setError(false), 1500);
        }
    };

    const handleChange = (e) => {
        const val = e.target.value.replace(/\D/g, '').slice(0, 4);
        setPin(val);
        if (val.length === 4) {
            handleSubmit(val);
        }
    };

    // 初始化加载中
    if (checking) {
        return (
            <div className="password-gate">
                <div style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                    加载中...
                </div>
            </div>
        );
    }

    // 已验证通过
    if (authed) return children;

    // 显示密码输入
    return (
        <div className="password-gate">
            <div className="password-box animate-fade-in">
                <div style={{ fontSize: '2.5rem', marginBottom: '16px' }}>🔐</div>
                <h1>研报分析系统</h1>
                <p>请输入4位访问码</p>
                <input
                    type="password"
                    className="password-input"
                    value={pin}
                    onChange={handleChange}
                    placeholder="• • • •"
                    autoFocus
                    maxLength={4}
                    inputMode="numeric"
                />
                <div className={`password-error ${error ? 'visible' : ''}`}>
                    访问码错误，请重试
                </div>
            </div>
        </div>
    );
}
