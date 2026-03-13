# 🛡️ Vocab Admin Panel

Giao diện quản trị (Admin Dashboard) cho hệ thống học từ vựng.  
Được xây dựng bằng **React 18 + TypeScript + Vite + Tailwind CSS v4**.

---

## ✨ Tính năng

- 🔐 **Đăng nhập bảo mật** — Riêng biệt hoàn toàn với tài khoản người dùng app
- 📊 **Dashboard tổng quan** — Thống kê học viên, khóa học, trạng thái hệ thống
- 👥 **Quản lý người dùng** — Xem danh sách, tìm kiếm và xóa tài khoản học viên
- 📚 **Quản lý khóa học** *(sắp ra mắt)* — Thêm/sửa/xóa khóa học và từ vựng
- 🌙 **Dark mode** — Giao diện tối chuyên nghiệp, tối ưu cho công việc dài

---

## 🛠️ Stack công nghệ

| Công nghệ | Phiên bản | Mục đích |
|-----------|-----------|----------|
| React | 18 | UI framework |
| TypeScript | 5 | Type safety |
| Vite | 7 | Build tool & dev server |
| Tailwind CSS | 4 | Styling |
| React Router DOM | 6 | Client-side routing |
| Axios | latest | HTTP client + JWT interceptor |
| Lucide React | latest | Icon library |

---

## 📋 Yêu cầu

- **Node.js** 18+ và npm 9+
- **Backend API** đang chạy tại `http://localhost:8000` *(xem README gốc để setup)*

---

## 🚀 Khởi động

### 1. Cài đặt dependencies

```bash
cd admin-panel
npm install
```

### 2. Chạy môi trường phát triển

```bash
npm run dev
```

Truy cập tại: **[http://localhost:5173](http://localhost:5173)**

### 3. Đăng nhập

Dùng tài khoản Admin đã tạo qua script:
```bash
# Chạy từ thư mục gốc dự án
docker compose exec api python -m app.create_admin admin@example.com MatKhau123 "Tên Admin"
```

---

## 📦 Scripts

| Lệnh | Mô tả |
|------|-------|
| `npm run dev` | Khởi động dev server (hot reload) |
| `npm run build` | Build production vào thư mục `dist/` |
| `npm run preview` | Preview bản build production |
| `npm run lint` | Kiểm tra lỗi ESLint |

---

## 📁 Cấu trúc source code

```
src/
├── api/
│   └── axios.ts          # HTTP client, JWT interceptor tự động
├── components/
│   └── Layout.tsx         # Sidebar + Top bar layout
├── context/
│   └── AuthContext.tsx    # Quản lý trạng thái đăng nhập (localStorage)
├── pages/
│   ├── LoginPage.tsx      # Màn hình đăng nhập
│   ├── DashboardPage.tsx  # Tổng quan hệ thống
│   └── UsersPage.tsx      # Quản lý người dùng
├── App.tsx                # Routing + ProtectedRoute
├── main.tsx               # Entry point
└── index.css              # Tailwind v4 theme + custom utilities
```

---

## 🔐 Cách xác thực hoạt động

1. Admin POST `{username, password}` dạng `x-www-form-urlencoded` tới `/api/v1/admin/auth/login`
2. Server trả về **JWT Token** chứa `"role": "admin"`
3. Token được lưu vào `localStorage` qua `AuthContext`
4. `axios.ts` tự động đính kèm `Authorization: Bearer <token>` vào mọi request
5. Nếu nhận `401`, Axios xóa token và điều hướng về `/login`

---

## 🤖 Agent Skills

Dự án có tích hợp **Tailwind CSS v4 Agent Skill** để AI Code Assistant làm việc chính xác hơn:

```
.agents/skills/tailwind-4-docs/
├── SKILL.md              # Hướng dẫn cho AI agent
└── references/
    ├── gotchas.md        # Các lỗi phổ biến Tailwind v4
    ├── docs/             # Snapshot docs Tailwind v4 (local)
    └── docs-index.tsx    # Index tra cứu nhanh
```

Để cập nhật tài liệu Tailwind:
```bash
python .agents/skills/tailwind-4-docs/scripts/sync_tailwind_docs.py --accept-docs-license
```

---

## 🌐 Cấu hình API URL

Mặc định, admin panel gọi API tại `http://localhost:8000`.  
Để thay đổi (ví dụ khi deploy lên server), sửa `baseURL` trong `src/api/axios.ts`:

```ts
const api = axios.create({
  baseURL: 'https://your-api-domain.com/api/v1',
});
```
