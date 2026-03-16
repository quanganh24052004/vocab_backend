import os
import sys

# Đảm bảo Python có thể tìm thấy module 'app'
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from sqlalchemy.orm import Session
from app.database import SessionLocal
# QUAN TRỌNG: Import tất cả model để SQLAlchemy nhận diện được Relationships
from app.modules.users.model import User
from app.modules.sync.model import StudyRecord 
from app.modules.courses.model import Course
from app.core import security
from app.core.conf import settings

def create_admin_user():
    db: Session = SessionLocal()
    
    # Lấy thông tin từ .env (đã được nạp vào biến môi trường)
    # Nếu không có trong .env, sẽ lấy từ file settings mặc định
    admin_email = os.getenv("ADMIN_EMAIL", settings.ADMIN_EMAIL)
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123456")
    admin_name = os.getenv("ADMIN_NAME", "Admin Superuser")

    print(f"[*] Đang kiểm tra tài khoản Admin: {admin_email}...")

    try:
        # Kiểm tra xem user đã tồn tại chưa
        user = db.query(User).filter(User.email == admin_email).first()
        
        if user:
            print(f"[-] User {admin_email} đã tồn tại.")
            # Đảm bảo user đó có quyền admin
            if hasattr(user, 'role') and user.role != "admin":
                user.role = "admin"
                db.commit()
                print(f"[+] Đã cập nhật quyền Admin cho {admin_email}.")
            return

        # Tạo user mới nếu chưa tồn tại
        hashed_password = security.get_password_hash(admin_password)
        new_user = User(
            email=admin_email,
            hashed_password=hashed_password,
            name=admin_name,
            role="admin",
            is_premium=True
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"✅ Đã tạo tài khoản Admin thành công từ .env!")
        print(f"    Email: {admin_email}")

    except Exception as e:
        print(f"[!] Lỗi khi khởi tạo Admin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
    