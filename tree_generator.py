import os
from pathlib import Path

# Các thư mục hoặc file không muốn in ra (để tránh cây quá dài)
IGNORE_ITEMS = {
    '.git', '__pycache__', 'node_modules', 'venv', '.venv', 
    '.build', '.DS_Store', '.idea', 'DerivedData'
}

def print_tree(directory, prefix=""):
    """
    Hàm đệ quy để in cây cấu trúc thư mục.
    """
    try:
        # Lấy danh sách file/folder và sắp xếp (folder trước, file sau)
        items = os.listdir(directory)
        items = [item for item in items if item not in IGNORE_ITEMS]
        items.sort(key=lambda x: (not os.path.isdir(os.path.join(directory, x)), x))
    except PermissionError:
        # Bỏ qua nếu không có quyền truy cập
        return

    count = len(items)
    for index, item in enumerate(items):
        path = os.path.join(directory, item)
        is_last = (index == count - 1)
        
        # Chọn ký tự rẽ nhánh phù hợp
        connector = "└── " if is_last else "├── "
        
        # In ra màn hình
        print(f"{prefix}{connector}{item}")
        
        # Nếu là thư mục thì gọi đệ quy đi sâu vào trong
        if os.path.isdir(path):
            extension = "    " if is_last else "│   "
            print_tree(path, prefix + extension)

if __name__ == "__main__":
    # Thay đổi đường dẫn này nếu muốn quét thư mục khác
    # "." nghĩa là quét thư mục hiện tại (nơi chứa file python này)
    target_dir = "." 
    
    # In tên thư mục gốc
    project_name = os.path.basename(os.path.abspath(target_dir))
    print(f"📁 {project_name}/")
    
    # Bắt đầu quét
    print_tree(target_dir)