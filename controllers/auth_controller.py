"""Điều phối đăng nhập."""
import json
import os

class AuthController:
    def __init__(self):
        # Đường dẫn tới file users.json. Bạn có thể thay bằng cách dùng file_handler.py của bạn.
        self.users_file = "data/users.json"
        
        # Nếu chưa có file users.json thì tạo 1 cái mặc định chứa tk admin
        if not os.path.exists(self.users_file):
            default_users = {"admin": {"password": "1", "role": "admin"}}
            with open(self.users_file, "w", encoding="utf-8") as f:
                json.dump(default_users, f, indent=4)

    def login(self, username, password):
        try:
            with open(self.users_file, "r", encoding="utf-8") as f:
                users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            users = {}

        user_info = users.get(username)
        # Kiểm tra user có tồn tại và đúng pass không
        if user_info and user_info.get("password") == password:
            # Trả về role (nếu tk cũ không có role thì mặc định là viewer)
            return user_info.get("role", "viewer")
        
        return None # Sai tài khoản hoặc mật khẩu

    def register(self, username, password, role="viewer"):
        try:
            with open(self.users_file, "r", encoding="utf-8") as f:
                users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            users = {}
            
        # Kiểm tra xem tên đăng nhập đã có chưa
        if username in users:
            return False 
            
        # Thêm user mới
        users[username] = {
            "password": password,
            "role": role
        }
        
        # Ghi đè lại vào file JSON
        with open(self.users_file, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4)
            
        return True
