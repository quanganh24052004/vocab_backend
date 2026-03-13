import React, { useEffect, useState } from 'react';
import { Trash2, Search, UserPlus, Loader2, ShieldOff } from 'lucide-react';
import api from '../api/axios';

interface User {
  id: string;
  email: string;
  name: string | null;
  phone: string | null;
  is_premium: boolean;
  created_at: string;
}

const UsersPage: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [deletingId, setDeletingId] = useState<string | null>(null);

  useEffect(() => {
    api.get('/users/')
      .then(r => setUsers(r.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const handleDelete = async (id: string) => {
    if (!confirm('Xóa tài khoản này? Toàn bộ dữ liệu học tập sẽ bị xóa vĩnh viễn.')) return;
    setDeletingId(id);
    try {
      await api.delete(`/users/${id}`);
      setUsers(prev => prev.filter(u => u.id !== id));
    } catch {
      alert('Xóa thất bại.');
    } finally {
      setDeletingId(null);
    }
  };

  const filtered = users.filter(u =>
    u.email.toLowerCase().includes(search.toLowerCase()) ||
    (u.name?.toLowerCase().includes(search.toLowerCase()))
  );

  return (
    <div className="space-y-6 animate-fade-up">
      {/* Header */}
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <h1 className="text-3xl font-black text-white tracking-tight">Người dùng</h1>
          <p className="text-sm mt-1" style={{ color: '#475569' }}>
            {users.length} tài khoản trong hệ thống
          </p>
        </div>
        <button
          className="btn-primary flex items-center gap-2 px-4 py-2.5 text-sm"
          disabled
          title="Tính năng sắp ra mắt"
        >
          <UserPlus size={16} /> Thêm người dùng
        </button>
      </div>

      {/* Table card */}
      <div
        className="rounded-2xl overflow-hidden"
        style={{ background: 'var(--color-surface-800)', border: '1px solid rgba(255,255,255,0.05)' }}
      >
        {/* Search bar */}
        <div
          className="flex items-center gap-4 px-5 py-4"
          style={{ borderBottom: '1px solid rgba(255,255,255,0.04)' }}
        >
          <div className="relative flex-1">
            <Search
              size={15}
              className="absolute left-3.5 top-1/2 -translate-y-1/2"
              style={{ color: '#334155' }}
            />
            <input
              type="text"
              placeholder="Tìm kiếm theo email hoặc tên..."
              value={search}
              onChange={e => setSearch(e.target.value)}
              className="input-dark w-full pl-10 pr-4 py-2.5 text-sm"
              style={{ background: 'var(--color-surface-900)' }}
            />
          </div>
          <span className="text-xs shrink-0" style={{ color: '#334155' }}>
            {filtered.length} kết quả
          </span>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.04)' }}>
                {['ID', 'Người dùng', 'Số điện thoại', 'Gói', 'Ngày tham gia', ''].map(h => (
                  <th
                    key={h}
                    className="px-5 py-3 text-left text-xs font-semibold uppercase tracking-wider"
                    style={{ color: '#334155', background: 'var(--color-surface-900)' }}
                  >
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan={6} className="py-16 text-center">
                    <Loader2 className="animate-spin mx-auto mb-2" size={24} style={{ color: '#3b82f6' }} />
                    <div className="text-sm" style={{ color: '#334155' }}>Đang tải dữ liệu...</div>
                  </td>
                </tr>
              ) : filtered.length === 0 ? (
                <tr>
                  <td colSpan={6} className="py-16 text-center">
                    <ShieldOff className="mx-auto mb-2" size={24} style={{ color: '#334155' }} />
                    <div className="text-sm" style={{ color: '#334155' }}>Không tìm thấy người dùng nào.</div>
                  </td>
                </tr>
              ) : (
                filtered.map(user => (
                  <tr
                    key={user.id}
                    className="group transition-colors duration-100"
                    style={{ borderBottom: '1px solid rgba(255,255,255,0.025)' }}
                    onMouseEnter={e => (e.currentTarget as HTMLElement).style.background = 'rgba(255,255,255,0.02)'}
                    onMouseLeave={e => (e.currentTarget as HTMLElement).style.background = ''}
                  >
                    <td className="px-5 py-4">
                      <code
                        className="text-xs px-2 py-1 rounded-lg font-mono"
                        style={{ background: 'rgba(59,130,246,0.1)', color: '#60a5fa' }}
                      >
                        {user.id}
                      </code>
                    </td>
                    <td className="px-5 py-4">
                      <div className="flex items-center gap-3">
                        <div
                          className="w-8 h-8 rounded-xl flex items-center justify-center text-xs font-bold shrink-0 uppercase"
                          style={{ background: 'linear-gradient(135deg, #3b82f6, #6366f1)', color: 'white' }}
                        >
                          {(user.name || user.email)[0]}
                        </div>
                        <div>
                          <div className="font-medium text-white leading-tight">{user.name || '—'}</div>
                          <div className="text-xs mt-0.5" style={{ color: '#475569' }}>{user.email}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-5 py-4" style={{ color: '#64748b' }}>
                      {user.phone || '—'}
                    </td>
                    <td className="px-5 py-4">
                      {user.is_premium ? (
                        <span
                          className="px-2.5 py-1 rounded-lg text-xs font-bold uppercase"
                          style={{ background: 'rgba(245,158,11,0.12)', color: '#f59e0b', border: '1px solid rgba(245,158,11,0.2)' }}
                        >
                          Premium
                        </span>
                      ) : (
                        <span
                          className="px-2.5 py-1 rounded-lg text-xs font-bold uppercase"
                          style={{ background: 'rgba(255,255,255,0.04)', color: '#475569', border: '1px solid rgba(255,255,255,0.06)' }}
                        >
                          Free
                        </span>
                      )}
                    </td>
                    <td className="px-5 py-4 text-xs" style={{ color: '#475569' }}>
                      {new Date(user.created_at).toLocaleDateString('vi-VN', {
                        year: 'numeric', month: 'short', day: 'numeric'
                      })}
                    </td>
                    <td className="px-5 py-4">
                      <button
                        onClick={() => handleDelete(user.id)}
                        disabled={deletingId === user.id}
                        className="opacity-0 group-hover:opacity-100 transition-all duration-150 w-8 h-8 rounded-lg flex items-center justify-center"
                        style={{ background: 'rgba(244,63,94,0.1)', color: '#f43f5e' }}
                        onMouseEnter={e => {
                          (e.currentTarget as HTMLElement).style.background = 'rgba(244,63,94,0.2)';
                        }}
                        onMouseLeave={e => {
                          (e.currentTarget as HTMLElement).style.background = 'rgba(244,63,94,0.1)';
                        }}
                      >
                        {deletingId === user.id ? (
                          <Loader2 size={14} className="animate-spin" />
                        ) : (
                          <Trash2 size={14} />
                        )}
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default UsersPage;
