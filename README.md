# 📘 Vocabulary Learning System — Backend & Admin Panel

> Một hệ thống học từ vựng với Backend FastAPI, Admin Dashboard React, và App iOS.  
> Tài liệu này hướng dẫn cách khởi tạo và chạy toàn bộ hệ thống trên máy local.

---

## 📁 Cấu trúc dự án

```
vocab_backend/
├── app/                    # FastAPI backend source code
│   ├── api/                # API routers (auth, sync, admin_*)
│   ├── core/               # Config, security utilities
│   ├── models.py           # SQLAlchemy database models
│   ├── schemas.py          # Pydantic request/response schemas
│   ├── database.py         # Database engine & session
│   ├── seed.py             # Data seeder script
│   └── create_admin.py     # Script tạo tài khoản Admin
├── admin-panel/            # React + Vite Admin Dashboard
│   └── src/
│       ├── pages/          # Login, Dashboard, Users, Courses
│       ├── components/     # Layout, sidebar
│       ├── api/            # Axios HTTP client
│       └── context/        # AuthContext (JWT state)
├── docker-compose.yml      # Dịch vụ: api + db (PostgreSQL)
├── Dockerfile              # Container cho FastAPI
├── requirements.txt        # Python dependencies
├── .env.example            # Template biến môi trường
└── .env                    # ⚠️ Cấu hình thực (KHÔNG commit!)
```

---

## ⚙️ Yêu cầu hệ thống

| Công cụ | Phiên bản tối thiểu |
|---------|---------------------|
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | 4.x |
| [Node.js](https://nodejs.org/) | 18.x LTS |
| npm | 9.x |
| Python | 3.11+ *(chỉ dùng để chạy script local)* |

---

## 🚀 PHẦN 1 — Khởi động Backend

### Bước 1: Clone dự án

```bash
git clone <repository_url>
cd vocab_backend
```

### Bước 2: Tạo file cấu hình môi trường

```bash
cp .env.example .env
```

Sau đó mở file `.env` và điền các giá trị phù hợp:

```dotenv
# Thông tin PostgreSQL
POSTGRES_USER=admin
POSTGRES_PASSWORD=your_secure_password_here
POSTGRES_DB=vocab_db
POSTGRES_HOST=db
POSTGRES_PORT=5432

# SQLAlchemy connection string (thay thế theo user/pass/db ở trên)
DATABASE_URL=postgresql://admin:your_secure_password_here@db:5432/vocab_db

# JWT Secret — Tạo bằng lệnh: openssl rand -hex 32
SECRET_KEY=your_generated_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

> **Tạo SECRET_KEY mạnh:**
> ```bash
> openssl rand -hex 32
> ```

### Bước 3: Build và chạy Docker

```bash
docker compose up --build -d
```

Kiểm tra các container đang chạy:

```bash
docker compose ps
```

Bạn sẽ thấy 2 service: `vocab_backend-api-1` và `vocab_backend-db-1`.

### Bước 4: Kiểm tra API đang hoạt động

```bash
curl http://localhost:8000/
# Kết quả mong đợi: {"message":"Server đang chạy ngon lành!","status":"OK"}
```

Hoặc truy cập Swagger UI tại: **http://localhost:8000/docs**

### Bước 5: Nạp dữ liệu mẫu (Tùy chọn)

Nếu bạn có file dữ liệu `app/courses_data.json`:

```bash
docker compose exec api python -m app.seed
```

---

## 🛡️ PHẦN 2 — Tạo tài khoản Admin

Tài khoản Admin **hoàn toàn tách biệt** với tài khoản người dùng app. Chạy lệnh sau để tạo admin đầu tiên:

```bash
docker compose exec api python -m app.create_admin <email> <password> "<tên hiển thị>"
```

**Ví dụ:**

```bash
docker compose exec api python -m app.create_admin admin@example.com MySecurePass123 "Nguyen Quang Anh"
```

Kết quả khi thành công:
```
Thành công! Đã tạo tài khoản Admin:
- Email: admin@example.com
- Tên: Nguyen Quang Anh
```

---

## 🖥️ PHẦN 3 — Khởi động Admin Dashboard (Frontend)

### Bước 1: Cài đặt dependencies

```bash
cd admin-panel
npm install
```

### Bước 2: Chạy server phát triển

```bash
npm run dev
```

Truy cập tại: **http://localhost:5173**

### Bước 3: Đăng nhập

Sử dụng email và password đã tạo ở Phần 2.

---

## 📋 Tổng hợp lệnh thường dùng

### Backend (Docker)

| Mục đích | Lệnh |
|----------|------|
| Khởi động toàn bộ | `docker compose up -d` |
| Dừng toàn bộ | `docker compose down` |
| Xem logs API | `docker compose logs -f api` |
| Restart API | `docker compose restart api` |
| Tạo Admin | `docker compose exec api python -m app.create_admin <email> <pass> "<name>"` |
| Nạp dữ liệu | `docker compose exec api python -m app.seed` |
| Truy cập DB shell | `docker compose exec db psql -U $POSTGRES_USER -d $POSTGRES_DB` |

### Frontend (Admin Panel)

| Mục đích | Lệnh |
|----------|------|
| Cài dependencies | `cd admin-panel && npm install` |
| Chạy dev server | `cd admin-panel && npm run dev` |
| Build production | `cd admin-panel && npm run build` |
| Sync Tailwind docs | `python admin-panel/.agents/skills/tailwind-4-docs/scripts/sync_tailwind_docs.py --accept-docs-license` |

---

## 🌐 API Endpoints chính

| Endpoint | Phương thức | Mô tả |
|----------|------------|-------|
| `/api/v1/auth/register` | POST | Đăng ký người dùng mới |
| `/api/v1/auth/login` | POST | Đăng nhập người dùng, lấy JWT |
| `/api/v1/sync/pull_courses` | POST | Tải dữ liệu khóa học (delta sync) |
| `/api/v1/admin/auth/login` | POST | Đăng nhập Admin (riêng biệt) |
| `/api/v1/admin/users/` | GET | Lấy danh sách toàn bộ người dùng |
| `/api/v1/admin/users/{id}` | DELETE | Xóa người dùng (cascade) |
| `/api/v1/admin/courses/` | POST | Tạo khóa học mới |
| `/api/v1/admin/courses/{id}` | DELETE | Xóa mềm khóa học |

> 📖 Xem chi tiết tất cả API tại: **http://localhost:8000/docs**

---

## 🔒 Bảo mật

- File `.env` đã được thêm vào `.gitignore` — **KHÔNG BAO GIỜ commit file này**.
- Tài khoản Admin và User dùng **bảng database riêng biệt** (`admins` vs `users`).
- JWT Token của Admin chứa `"role": "admin"` — các API admin từ chối token của user thường và ngược lại.
- Mật khẩu được hash bằng **bcrypt** trước khi lưu vào database.

---

## 🏗️ Kiến trúc hệ thống

```
iOS App (SwiftUI)
      ↕ JWT Token (Keychain)
      ↕ /api/v1/auth/** + /api/v1/sync/**
      ↕
FastAPI (Docker :8000)
      ↕ SQLAlchemy ORM
      ↕
PostgreSQL (Docker :5432)
      ↑
Admin Dashboard (React :5173)
      ↕ Admin JWT (/api/v1/admin/**)
```

---

## 🐛 Xử lý sự cố

**Lỗi: `connection refused` khi gọi API từ browser**
→ Kiểm tra Docker đang chạy: `docker compose ps`

**Lỗi: `401 Unauthorized` khi đăng nhập Admin**
→ Kiểm tra đã tạo tài khoản admin chưa (Phần 2) và đang gọi đúng endpoint `/admin/auth/login`.

**Lỗi: `ModuleNotFoundError: No module named 'sqlalchemy'`**
→ Chạy script qua Docker (không phải Python local): `docker compose exec api python -m app.create_admin ...`

**Lỗi: CORS blocked trên browser**
→ Đảm bảo backend đang chạy trên port 8000 và `main.py` đã có `CORSMiddleware`.
