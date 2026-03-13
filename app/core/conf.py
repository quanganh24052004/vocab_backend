import os
from dotenv import load_dotenv

# Tìm và load giá trị từ file .env ở thư mục gốc dự án
load_dotenv()

class Settings:
    # Database
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "postgres")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    
    # URL mặc định cho Local Testing (khi chạy python trực tiếp ngoài docker)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "fallback_secret_key_please_change")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:5173",  # Vite default
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "*", # Cho phép tất cả trong lúc dev, có thể siết lại sau
    ]

    # Admin config
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "admin@vocab.com")

settings = Settings()
