import json
import os

# Thư mục gốc của dự án
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

def get_file_path(filename):
    """Lấy đường dẫn đầy đủ đến tệp tin trong thư mục data."""
    return os.path.join(DATA_DIR, filename)

def load_json(filename, default=[]):
    """Đọc dữ liệu từ tệp JSON."""
    path = get_file_path(filename)
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(filename, data):
    """Ghi dữ liệu vào tệp JSON."""
    path = get_file_path(filename)
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
