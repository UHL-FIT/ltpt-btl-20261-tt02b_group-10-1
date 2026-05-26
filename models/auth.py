from utils.file_handler import load_json, save_json

def verify(username, password):
    """Kiểm tra tên đăng nhập và mật khẩu. Trả về vai trò (role) nếu đúng, ngược lại trả về None."""
    users = load_json("users.json", default=[])
    for u in users:
        if u.get("username") == username and u.get("password") == password:
            return u.get("role", "viewer")
    return None

def register_user(username, password):
    """Đăng ký tài khoản mới với quyền mặc định là 'viewer'."""
    users = load_json("users.json", default=[])
    
    # Kiểm tra xem tài khoản đã tồn tại chưa
    for u in users:
        if u.get("username") == username:
            return False # Tài khoản đã tồn tại
            
    # Thêm tài khoản mới
    users.append({
        "username": username,
        "password": password,
        "role": "viewer"
    })
    save_json("users.json", users)
    return True
