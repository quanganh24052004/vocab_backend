from fastapi import FastAPI
from .database import engine, Base

from .api import auth, sync

# Tự động tạo bảng PostgreSQL nếu chưa có
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vocabulary Sync API")

@app.get("/")
def read_root():
    return {"message": "Server đang chạy ngon lành!", "status": "OK"}

# Đăng ký các route API
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(sync.router, prefix="/api/v1/sync", tags=["Sync"])