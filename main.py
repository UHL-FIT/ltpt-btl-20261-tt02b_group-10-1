import tkinter as tk
from views.login_view import LoginView
from views.main_view import MainView

def main():
    root = tk.Tk()
    root.title("Đăng nhập — Quản lý lương")
    root.geometry("400x260")
    root.minsize(320, 220)

    def open_main(role):
        # Xóa giao diện đăng nhập cũ
        for w in root.winfo_children():
            w.destroy()
        
        # Thiết lập cửa sổ làm việc chính dựa vào quyền truy cập
        role_title = "Quản trị viên" if role == "admin" else "Nhân viên (Chỉ xem)"
        root.title(f"Quản lý lương nhân viên - {role_title}")
        root.geometry("900x620")
        root.minsize(720, 480)
        
        # Mở màn hình làm việc chính
        MainView(root, role=role)

    # Hiển thị màn hình đăng nhập đầu tiên
    LoginView(root, on_success=open_main)
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()

if __name__ == "__main__":
    main()
