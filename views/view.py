import tkinter as tk
from tkinter import ttk

class QuanLyLuongView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hệ thống Quản Lý Lương Nhân Viên")
        self.geometry("900x550")
        self.configure(padx=10, pady=10)

        # --- PHẦN 1: KHUNG NHẬP LIỆU ---
        frame_nhap = tk.LabelFrame(self, text="Nhập Thông Tin Lương", font=("Arial", 10, "bold"))
        frame_nhap.pack(fill="x", pady=10)

        self.ma_nv = tk.StringVar()
        self.ten_nv = tk.StringVar()
        self.luong_cb = tk.StringVar()
        self.thuong = tk.StringVar()
        self.phat = tk.StringVar()
        self.ngay_cong = tk.StringVar()
        self.gio_lam = tk.StringVar()

        tk.Label(frame_nhap, text="Mã NV:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        tk.Entry(frame_nhap, textvariable=self.ma_nv).grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(frame_nhap, text="Tên NV:").grid(row=0, column=2, padx=10, pady=5, sticky="e")
        tk.Entry(frame_nhap, textvariable=self.ten_nv).grid(row=0, column=3, padx=10, pady=5)
        
        tk.Label(frame_nhap, text="Lương CB:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        tk.Entry(frame_nhap, textvariable=self.luong_cb).grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(frame_nhap, text="Thưởng:").grid(row=1, column=2, padx=10, pady=5, sticky="e")
        tk.Entry(frame_nhap, textvariable=self.thuong).grid(row=1, column=3, padx=10, pady=5)
        
        tk.Label(frame_nhap, text="Phạt:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        tk.Entry(frame_nhap, textvariable=self.phat).grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(frame_nhap, text="Ngày công:").grid(row=2, column=2, padx=10, pady=5, sticky="e")
        tk.Entry(frame_nhap, textvariable=self.ngay_cong).grid(row=2, column=3, padx=10, pady=5)
        
        tk.Label(frame_nhap, text="Giờ làm thêm:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        tk.Entry(frame_nhap, textvariable=self.gio_lam).grid(row=3, column=1, padx=10, pady=5)

        # --- PHẦN 2: CÁC NÚT BẤM ---
        frame_btn = tk.Frame(self)
        frame_btn.pack(pady=5)
        
        self.btn_them = tk.Button(frame_btn, text=" Thêm & Tính Lương", width=20, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.btn_them.pack(side="left", padx=10)
        
        self.btn_thong_ke = tk.Button(frame_btn, text=" Xem Thống Kê", width=20, bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
        self.btn_thong_ke.pack(side="left", padx=10)

        # --- PHẦN 3: BẢNG HIỂN THỊ DỮ LIỆU ---
        frame_bang = tk.LabelFrame(self, text="Bảng Lương Chi Tiết", font=("Arial", 10, "bold"))
        frame_bang.pack(fill="both", expand=True, pady=10)
        
        cols = ("Mã NV", "Tên NV", "Lương CB", "Thưởng", "Phạt", "Ngày", "Giờ LT", "Thực Nhận")
        self.tree = ttk.Treeview(frame_bang, columns=cols, show="headings")
        
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
