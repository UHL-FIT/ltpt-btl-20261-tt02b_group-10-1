from models.auth import verify, register_user

class AuthController:
    def login(self, username, password):
        """Xử lý đăng nhập, trả về quyền hoặc None."""
        return verify(username.strip(), password)

    def register(self, username, password):
        """Xử lý đăng ký tài khoản mới."""
        return register_user(username.strip(), password)
