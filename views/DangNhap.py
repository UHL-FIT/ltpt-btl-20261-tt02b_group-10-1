import tkinter as tk

class LoginView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Đăng nhập hệ thống")
        self.geometry("350x250")
        self.configure(padx=20, pady=20)

        # Tiêu đề
        tk.Label(self, text="ĐĂNG NHẬP", font=("Arial", 14, "bold")).pack(pady=10)

        # Ô nhập Tài khoản
        tk.Label(self, text="Tên tài khoản:").pack(anchor="w")
        self.ent_user = tk.Entry(self, width=30)
        self.ent_user.pack(pady=5)

        # Ô nhập Mật khẩu (show="*" để ẩn mật khẩu)
        tk.Label(self, text="Mật khẩu (Chỉ dùng số):").pack(anchor="w")
        self.ent_pass = tk.Entry(self, width=30, show="*")
        self.ent_pass.pack(pady=5)

        # Nút đăng nhập màu đỏ
        self.btn_login = tk.Button(self, text="Đăng Nhập", bg="red", fg="white", 
                                   font=("TimeNewRoman", 10, "bold"), width=15)
        self.btn_login.pack(pady=20)

    def get_credentials(self):
        return self.ent_user.get(), self.ent_pass.get()

# ==========================================
# CHẠY THỬ NGHIỆM ĐỘC LẬP FILE LOGIN_VIEW
# ==========================================
if __name__ == "__main__":
    print("--- ĐANG TEST GIAO DIỆN ĐĂNG NHẬP ---")
    test_login = LoginView()
    
    def test_nut_bam():
        tk_user, mk = test_login.get_credentials()
        print(f"-> Bạn vừa gõ Tài khoản: '{tk_user}' và Mật khẩu: '{mk}'")

    test_login.btn_login.config(command=test_nut_bam)
    test_login.mainloop()
