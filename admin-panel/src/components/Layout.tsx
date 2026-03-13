import React, { useState } from 'react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  LayoutDashboard, Users, Library, LogOut, Settings,
  ChevronLeft, ChevronRight, Bell
} from 'lucide-react';

const navItems = [
  { to: '/', icon: LayoutDashboard, label: 'Tổng quan' },
  { to: '/users', icon: Users, label: 'Người dùng' },
  { to: '/courses', icon: Library, label: 'Khóa học' },
  { to: '/settings', icon: Settings, label: 'Cài đặt' },
];

const Layout: React.FC = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div className="flex min-h-screen" style={{ background: 'var(--color-surface-900)' }}>
      {/* Sidebar */}
      <aside
        className="sticky top-0 h-screen flex flex-col shrink-0 transition-all duration-300 ease-in-out"
        style={{
          width: collapsed ? '72px' : '240px',
          borderRight: '1px solid rgba(255,255,255,0.04)',
          background: 'var(--color-surface-800)',
        }}
      >
        {/* Logo */}
        <div
          className="flex items-center gap-3 px-4 py-5"
          style={{ borderBottom: '1px solid rgba(255,255,255,0.04)', minHeight: '64px' }}
        >
          <div
            className="shrink-0 w-9 h-9 rounded-xl flex items-center justify-center text-white font-black text-sm"
            style={{ background: 'linear-gradient(135deg, #3b82f6, #6366f1)' }}
          >
            V
          </div>
          {!collapsed && (
            <div className="overflow-hidden">
              <div className="font-bold text-sm text-white leading-tight">VocabAdmin</div>
              <div className="text-xs" style={{ color: '#334155' }}>Management System</div>
            </div>
          )}
        </div>

        {/* Nav */}
        <nav className="flex-1 p-3 space-y-1">
          {navItems.map(({ to, icon: Icon, label }) => (
            <NavLink
              key={to}
              to={to}
              end={to === '/'}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-150 group ${
                  isActive
                    ? 'text-white'
                    : 'text-slate-500 hover:text-slate-200'
                }`
              }
              style={({ isActive }) =>
                isActive
                  ? {
                      background: 'linear-gradient(135deg, rgba(59,130,246,0.18) 0%, rgba(99,102,241,0.12) 100%)',
                      boxShadow: 'inset 0 0 0 1px rgba(99,102,241,0.2)',
                    }
                  : {}
              }
            >
              {({ isActive }) => (
                <>
                  <Icon
                    size={18}
                    className="shrink-0"
                    color={isActive ? '#60a5fa' : undefined}
                  />
                  {!collapsed && <span className="truncate">{label}</span>}
                </>
              )}
            </NavLink>
          ))}
        </nav>

        {/* Collapse toggle */}
        <div className="p-3" style={{ borderTop: '1px solid rgba(255,255,255,0.04)' }}>
          <button
            onClick={() => setCollapsed(!collapsed)}
            className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-slate-500 hover:text-slate-200 hover:bg-white/5 transition-all text-sm font-medium"
          >
            {collapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
            {!collapsed && <span>Thu gọn</span>}
          </button>
          <button
            onClick={() => { logout(); navigate('/login'); }}
            className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all text-sm font-medium mt-1"
            style={{ color: '#64748b' }}
            onMouseEnter={e => {
              (e.currentTarget as HTMLElement).style.background = 'rgba(244,63,94,0.08)';
              (e.currentTarget as HTMLElement).style.color = '#f87171';
            }}
            onMouseLeave={e => {
              (e.currentTarget as HTMLElement).style.background = '';
              (e.currentTarget as HTMLElement).style.color = '#64748b';
            }}
          >
            <LogOut size={18} className="shrink-0" />
            {!collapsed && <span>Đăng xuất</span>}
          </button>
        </div>
      </aside>

      {/* Main content */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top bar */}
        <header
          className="sticky top-0 z-10 flex items-center justify-between px-8 h-16 shrink-0"
          style={{
            background: 'rgba(13,17,23,0.8)',
            backdropFilter: 'blur(12px)',
            borderBottom: '1px solid rgba(255,255,255,0.04)',
          }}
        >
          <div className="text-sm font-semibold text-slate-400">Chào mừng quay trở lại 👋</div>
          <div className="flex items-center gap-3">
            <button className="w-9 h-9 rounded-xl flex items-center justify-center text-slate-400 hover:text-white hover:bg-white/8 transition-all relative">
              <Bell size={17} />
              <span
                className="absolute top-2 right-2 w-2 h-2 rounded-full"
                style={{ background: '#3b82f6' }}
              />
            </button>
            <div
              className="w-9 h-9 rounded-xl flex items-center justify-center text-sm font-bold text-white"
              style={{ background: 'linear-gradient(135deg, #3b82f6, #6366f1)' }}
            >
              A
            </div>
          </div>
        </header>

        <main className="flex-1 p-8 overflow-y-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;
