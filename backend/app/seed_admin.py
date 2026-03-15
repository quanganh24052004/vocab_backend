import os
import sys
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.modules.users.model import User
from app.core import security
from app.core.conf import settings

def create_admin_user(email: str, password: str, name: str = "Admin"):
    db: Session = SessionLocal()
    try:
        # Kiểm tra xem user đã tồn tại chưa
        user = db.query(User).filter(User.email == email).first()
        if user:
            print(f"[-] User với email {email} đã tồn tại.")
            # Cập nhật quyền admin nếu chưa có
            if user.role != "admin":
                user.role = "admin"
                db.commit()
                print(f"[+] Đã cập nhật quyền Admin cho user {email}.")
            return

        # Tạo user mới
        hashed_password = security.get_password_hash(password)
        new_user = User(
            email=email,
            hashed_password=hashed_password,
            name=name,
            role="admin",
            is_premium=True
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"[+] Đã tạo tài khoản Admin thành công!")
        print(f"    Email: {email}")
        print(f"    Name: {name}")
    except Exception as e:
        print(f"[!] Lỗi khi tạo user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Ưu tiên lấy từ biến môi trường, nếu không có thì dùng mặc định
    admin_email = os.getenv("ADMIN_EMAIL", settings.ADMIN_EMAIL)
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123456") # Mật khẩu mặc định nếu không có trong env

    print(f"[*] Đang khởi tạo tài khoản Admin cho hệ thống...")
    create_admin_user(email=admin_email, password=admin_password)
