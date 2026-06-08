import tkinter as tk
from tkinter import messagebox, ttk

class LoginView(ttk.Frame):
    def __init__(self, master, on_success):
        super().__init__(master, padding=16)
        self.on_success = on_success
        self.pack(fill=tk.BOTH, expand=True)

        frm = ttk.Frame(self)
        frm.pack(expand=True)

        ttk.Label(frm, text="Tên đăng nhập:").grid(row=0, column=0, sticky=tk.W, pady=(0, 4))
        self.username = ttk.Entry(frm, width=28)
        self.username.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=(0, 10))

        ttk.Label(frm, text="Mật khẩu (Chỉ nhập số):").grid(row=2, column=0, sticky=tk.W, pady=(0, 4))
        self.password = ttk.Entry(frm, width=28, show="*")
        self.password.grid(row=3, column=0, columnspan=2, sticky=tk.EW, pady=(0, 14))

        btn_frame = ttk.Frame(frm)
        btn_frame.grid(row=4, column=0, columnspan=2, sticky=tk.EW)
        
        tk.Button(btn_frame, text="Đăng ký tài khoản", command=self._open_register, bg="#95A5A6", fg="white", activebackground="#7F8C8D", activeforeground="white", relief="flat", bd=0, padx=10, pady=5).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Đăng nhập", command=self._submit, bg="#3498DB", fg="white", activebackground="#2980B9", activeforeground="white", relief="flat", bd=0, padx=15, pady=5).pack(side=tk.RIGHT)

        self.username.focus_set()
        self.username.bind("<Return>", lambda e: self._submit())
        self.password.bind("<Return>", lambda e: self._submit())

    def _submit(self):
        """Xử lý sự kiện đăng nhập."""
        from controllers.auth_controller import AuthController

        user = self.username.get().strip()
        pwd = self.password.get()
        if not user or not pwd:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đủ tên đăng nhập và mật khẩu.")
            return

        if not pwd.isdigit():
            messagebox.showerror("Lỗi", "Mật khẩu chỉ được điền số!")
            return
            
        role = AuthController().login(user, pwd)
        if role:
            self.on_success(role)
        else:
            messagebox.showerror("Đăng nhập thất bại", "Sai tên đăng nhập hoặc mật khẩu.")

    def _open_register(self):
        """Mở cửa sổ phụ tạo tài khoản mới."""
        reg_win = tk.Toplevel(self)
        reg_win.title("Tạo tài khoản")
        reg_win.geometry("300x200")
        reg_win.transient(self.master)
        reg_win.grab_set()

        frm = ttk.Frame(reg_win, padding=16)
        frm.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frm, text="Tên đăng nhập mới:").grid(row=0, column=0, sticky=tk.W, pady=(0, 4))
        reg_user = ttk.Entry(frm, width=25)
        reg_user.grid(row=1, column=0, sticky=tk.EW, pady=(0, 10))

        ttk.Label(frm, text="Mật khẩu mới (Chỉ chứa số):").grid(row=2, column=0, sticky=tk.W, pady=(0, 4))
        reg_pwd = ttk.Entry(frm, width=25, show="*")
        reg_pwd.grid(row=3, column=0, sticky=tk.EW, pady=(0, 14))

        def _do_register():
            u = reg_user.get().strip()
            p = reg_pwd.get()
            if not u or not p:
                messagebox.showwarning("Lỗi", "Vui lòng nhập đủ thông tin.", parent=reg_win)
                return

            if not p.isdigit():
                messagebox.showerror("Lỗi", "Mật khẩu chỉ được chứa số!", parent=reg_win)
                return
                
            from controllers.auth_controller import AuthController
            if AuthController().register(u, p):
                messagebox.showinfo("Thành công", f"Đã đăng ký tài khoản '{u}' (Quyền: Chỉ xem).", parent=reg_win)
                reg_win.destroy()
            else:
                messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại!", parent=reg_win)

        tk.Button(frm, text="Đăng ký", command=_do_register, bg="#2ECC71", fg="white", activebackground="#27AE60", activeforeground="white", relief="flat", bd=0, padx=15, pady=5).grid(row=4, column=0, pady=(10, 0))
