"""Điểm vào ứng dụng Quản lý lương (Tkinter + MVC)."""
from __future__ import annotations

import tkinter as tk

from views.login_view import LoginView
from views.main_view import MainView


def main() -> None:
    root = tk.Tk()
    root.title("Đăng nhập — Quản lý lương")
    root.geometry("400x260")
    root.minsize(320, 220)

    def open_main(role: str) -> None:  # 1. Thêm tham số role ở đây
        for w in root.winfo_children():
            w.destroy()
        root.title("Quản lý lương nhân viên")
        root.geometry("900x620")
        root.minsize(720, 480)
        MainView(root, role=role)      # 2. Truyền tham số role vào MainView

    LoginView(root, on_success=open_main)
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()


if __name__ == "__main__":
    main()
