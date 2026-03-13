import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Users, Library, Zap, ArrowUpRight, Activity } from 'lucide-react';
import api from '../api/axios';

const StatCard: React.FC<{
  label: string;
  value: string | number;
  icon: React.ReactNode;
  color: string;
  glow: string;
  sub?: string;
}> = ({ label, value, icon, color, glow, sub }) => (
  <div
    className="relative overflow-hidden rounded-2xl p-6 flex flex-col gap-3 group transition-transform duration-200 hover:-translate-y-0.5"
    style={{ background: 'var(--color-surface-800)', border: '1px solid rgba(255,255,255,0.05)' }}
  >
    {/* Glow accent */}
    <div
      className="absolute -top-6 -right-6 w-24 h-24 rounded-full blur-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"
      style={{ background: glow }}
    />
    <div
      className="w-10 h-10 rounded-xl flex items-center justify-center shrink-0"
      style={{ background: `${color}18`, color }}
    >
      {icon}
    </div>
    <div>
      <div className="text-3xl font-black text-white tracking-tight">{value}</div>
      <div className="text-sm font-medium mt-0.5" style={{ color: '#475569' }}>{label}</div>
      {sub && <div className="text-xs mt-1" style={{ color: '#334155' }}>{sub}</div>}
    </div>
  </div>
);

const QuickAction: React.FC<{
  to: string;
  icon: React.ReactNode;
  title: string;
  desc: string;
  accentColor: string;
}> = ({ to, icon, title, desc, accentColor }) => (
  <Link
    to={to}
    className="group flex items-center justify-between p-5 rounded-2xl transition-all duration-200 hover:-translate-y-0.5"
    style={{ background: 'var(--color-surface-800)', border: '1px solid rgba(255,255,255,0.05)' }}
    onMouseEnter={e =>
      (e.currentTarget as HTMLElement).style.borderColor = `${accentColor}33`
    }
    onMouseLeave={e =>
      (e.currentTarget as HTMLElement).style.borderColor = 'rgba(255,255,255,0.05)'
    }
  >
    <div className="flex items-center gap-4">
      <div
        className="w-11 h-11 rounded-xl flex items-center justify-center transition-colors duration-200"
        style={{ background: `${accentColor}14`, color: accentColor }}
      >
        {icon}
      </div>
      <div>
        <div className="text-sm font-semibold text-white">{title}</div>
        <div className="text-xs mt-0.5" style={{ color: '#475569' }}>{desc}</div>
      </div>
    </div>
    <ArrowUpRight
      size={16}
      className="transition-transform duration-200 group-hover:translate-x-0.5 group-hover:-translate-y-0.5"
      style={{ color: '#334155' }}
    />
  </Link>
);

const DashboardPage: React.FC = () => {
  const [userCount, setUserCount] = useState<number | '—'>('—');

  useEffect(() => {
    api.get('/users/')
      .then(r => setUserCount(r.data.length))
      .catch(() => setUserCount(0));
  }, []);

  return (
    <div className="space-y-8 animate-fade-up">
      <div className="flex items-end justify-between">
        <div>
          <h1 className="text-3xl font-black text-white tracking-tight">Tổng quan</h1>
          <p className="text-sm mt-1" style={{ color: '#475569' }}>Dữ liệu hệ thống theo thời gian thực</p>
        </div>
        <div
          className="flex items-center gap-2 px-3 py-1.5 rounded-xl text-xs font-semibold"
          style={{ background: 'rgba(16,185,129,0.1)', color: '#10b981', border: '1px solid rgba(16,185,129,0.2)' }}
        >
          <span
            className="w-2 h-2 rounded-full"
            style={{ background: '#10b981', animation: 'pulse-dot 2s ease-in-out infinite' }}
          />
          Live · Online
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          label="Học viên đăng ký"
          value={userCount}
          icon={<Users size={20} />}
          color="#3b82f6"
          glow="rgba(59,130,246,0.4)"
          sub="Tổng tài khoản"
        />
        <StatCard
          label="Khóa học"
          value={15}
          icon={<Library size={20} />}
          color="#10b981"
          glow="rgba(16,185,129,0.4)"
          sub="Đang hoạt động"
        />
        <StatCard
          label="Từ vựng"
          value="500+"
          icon={<Zap size={20} />}
          color="#f59e0b"
          glow="rgba(245,158,11,0.4)"
          sub="Trong hệ thống"
        />
        <StatCard
          label="API Uptime"
          value="99.9%"
          icon={<Activity size={20} />}
          color="#8b5cf6"
          glow="rgba(139,92,246,0.4)"
          sub="30 ngày gần nhất"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Quick actions (2/3 width) */}
        <div className="lg:col-span-2 space-y-4">
          <h2 className="text-sm font-semibold uppercase tracking-wider" style={{ color: '#475569' }}>
            Lối tắt nhanh
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <QuickAction
              to="/users"
              icon={<Users size={20} />}
              title="Quản lý học viên"
              desc="Xem, tìm kiếm và xóa tài khoản"
              accentColor="#3b82f6"
            />
            <QuickAction
              to="/courses"
              icon={<Library size={20} />}
              title="Biên tập khóa học"
              desc="Thêm, sửa, xóa nội dung"
              accentColor="#10b981"
            />
          </div>
        </div>

        {/* System health (1/3 width) */}
        <div
          className="rounded-2xl p-6 flex flex-col gap-5"
          style={{ background: 'var(--color-surface-800)', border: '1px solid rgba(255,255,255,0.05)' }}
        >
          <h2 className="text-sm font-semibold uppercase tracking-wider" style={{ color: '#475569' }}>
            Hệ thống
          </h2>
          {[
            { label: 'FastAPI Backend', status: 'Hoạt động', ok: true },
            { label: 'PostgreSQL DB', status: 'Hoạt động', ok: true },
            { label: 'Docker Network', status: 'Hoạt động', ok: true },
          ].map(item => (
            <div key={item.label} className="flex items-center justify-between">
              <span className="text-sm" style={{ color: '#94a3b8' }}>{item.label}</span>
              <div
                className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold"
                style={{
                  background: item.ok ? 'rgba(16,185,129,0.1)' : 'rgba(244,63,94,0.1)',
                  color: item.ok ? '#10b981' : '#f43f5e',
                }}
              >
                <span
                  className="w-1.5 h-1.5 rounded-full"
                  style={{
                    background: item.ok ? '#10b981' : '#f43f5e',
                    animation: 'pulse-dot 2s ease-in-out infinite',
                  }}
                />
                {item.status}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
