import secrets
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
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

# Khởi tạo app với docs được tắt mặc định
app = FastAPI(
    title="Vocabulary Sync API - Modular Version",
    docs_url=None, 
    redoc_url=None, 
    openapi_url=None
)

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, settings.DOCS_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, settings.DOCS_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/docs", include_in_schema=False)
async def get_swagger_documentation(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

@app.get("/redoc", include_in_schema=False)
async def get_redoc_documentation(username: str = Depends(get_current_username)):
    return get_redoc_html(openapi_url="/openapi.json", title="redoc")

@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(get_current_username)):
    return get_openapi(title=app.title, version=app.version, routes=app.routes)

origins = [
    "https://admin.amidemy.uk",
    "https://amidemy.uk",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Thay settings.BACKEND_CORS_ORIGINS bằng danh sách này
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
