from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.core.conf import settings
from app.modules.auth.api import router as auth_router
from app.modules.users.api import router as user_router
from app.modules.courses.api import router as course_router
from app.modules.sync.api import router as sync_router

# Tự động tạo bảng (Nên dùng Alembic trong production, nhưng giữ nguyên prototype cho user)
# Lưu ý: Vì Base được dùng chung, nó sẽ quét tất cả các model đã được import
from app.modules.users.model import User
from app.modules.courses.model import Course, Lesson, Word, Meaning
from app.modules.sync.model import StudyRecord, LessonRecord

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vocabulary Sync API - Modular Version")

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Server Modular đang chạy ngon lành!", "status": "OK"}

# Đăng ký các module router
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(user_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(course_router, prefix="/api/v1/courses", tags=["Courses"])
app.include_router(sync_router, prefix="/api/v1/sync", tags=["Sync"])