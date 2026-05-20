"""Màn hình đăng nhập (Frame trên cửa sổ chính — tránh lỗi Toplevel khi root bị ẩn)."""
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable


class LoginView(ttk.Frame):
    """Form đăng nhập; đặt trực tiếp trong ``tk.Tk()`` để luôn hiển thị trên Windows."""

    def __init__(
        self,
        master: tk.Tk,
        on_success: Callable[[str], None], # Cập nhật: Nhận thêm tham số role (str)
    ) -> None:
        super().__init__(master, padding=16)
        self.on_success = on_success
        self.pack(fill=tk.BOTH, expand=True)

        frm = ttk.Frame(self)
        frm.pack(expand=True)

        ttk.Label(frm, text="Tên đăng nhập").grid(row=0, column=0, sticky=tk.W, pady=(0, 4))
        self.username = ttk.Entry(frm, width=28)
        self.username.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=(0, 10))

        ttk.Label(frm, text="Mật khẩu").grid(row=2, column=0, sticky=tk.W, pady=(0, 4))
        self.password = ttk.Entry(frm, width=28, show="*")
        self.password.grid(row=3, column=0, columnspan=2, sticky=tk.EW, pady=(0, 14))

        btn_frame = ttk.Frame(frm)
        btn_frame.grid(row=4, column=0, columnspan=2, sticky=tk.EW)
        
        # Thêm nút Đăng ký
        ttk.Button(btn_frame, text="Đăng ký (Viewer)", command=self._handle_register).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Đăng nhập", command=self._submit).pack(side=tk.RIGHT)

        frm.columnconfigure(0, weight=1)

        self.username.focus_set()
        self.bind("<Return>", lambda e: self._submit())
        self.password.bind("<Return>", lambda e: self._submit())

    def _submit(self) -> None:
        from controllers.auth_controller import AuthController

        user = self.username.get()
        pwd = self.password.get()
        if not user or not pwd:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đủ tên đăng nhập và mật khẩu.")
            return
            
        # AuthController bây giờ cần trả về role ("admin" hoặc "viewer") thay vì True/False
        role = AuthController().login(user, pwd)
        if role:
            self.on_success(role)
        else:
            messagebox.showerror("Đăng nhập thất bại", "Sai tên đăng nhập hoặc mật khẩu.")

    def _handle_register(self) -> None:
        from controllers.auth_controller import AuthController
        
        user = self.username.get()
        pwd = self.password.get()
        
        if not user or not pwd:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đủ tên đăng nhập và mật khẩu để đăng ký.")
            return
            
        # Gọi hàm register từ controller, gán mặc định role là 'viewer'
        success = AuthController().register(user, pwd, role="viewer")
        if success:
            messagebox.showinfo("Thành công", f"Đã tạo tài khoản '{user}'. Bạn có thể đăng nhập.")
        else:
            messagebox.showerror("Thất bại", "Tên đăng nhập đã tồn tại hoặc có lỗi xảy ra.")
