"""Màn hình chính: danh sách + form."""
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from controllers.employee_controller import EmployeeController
from views.employee_view import EmployeeView


class MainView(ttk.Frame):
    def __init__(self, master: tk.Tk, role: str) -> None: # Thêm biến role
        super().__init__(master, padding=12)
        self.pack(fill=tk.BOTH, expand=True)
        self.role = role

        self.controller = EmployeeController(on_changed=self.refresh_table)

        # Khởi tạo form nhưng CHỈ PACK nó vào màn hình nếu là admin
        self.form = EmployeeView(self, on_add=self._handle_add)
        if self.role == "admin":
            self.form.pack(fill=tk.X, pady=(0, 12))

        table_frame = ttk.LabelFrame(self, text="Danh sách nhân viên", padding=8)
        table_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = self._build_table(table_frame)
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.refresh_table()

    def _build_table(self, parent: tk.Widget) -> ttk.Treeview:
        cols = ("id", "full_name", "department", "base", "allowance", "deduction", "net")
        tree = ttk.Treeview(
            parent,
            columns=cols,
            show="headings",
            height=12,
        )
        headings = {
            "id": "Mã",
            "full_name": "Họ tên",
            "department": "Phòng ban",
            "base": "Lương CB",
            "allowance": "Phụ cấp",
            "deduction": "Khấu trừ",
            "net": "Thực nhận",
        }
        widths = {
            "id": 100,
            "full_name": 140,
            "department": 100,
            "base": 90,
            "allowance": 80,
            "deduction": 80,
            "net": 90,
        }
        for c in cols:
            tree.heading(c, text=headings[c])
            tree.column(c, width=widths[c], anchor=tk.CENTER if c != "full_name" else tk.W)
        return tree

    def refresh_table(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        for e in self.controller.list_employees():
            short_id = e.id[:10] + "…" if len(e.id) > 10 else e.id
            self.tree.insert(
                "",
                tk.END,
                values=(
                    short_id,
                    e.full_name,
                    e.department,
                    f"{e.base_salary:,.0f}",
                    f"{e.allowance:,.0f}",
                    f"{e.deduction:,.0f}",
                    f"{e.net_salary():,.0f}",
                ),
            )

    def _handle_add(
        self,  
        full_name: str,
        department: str,
        base_raw: str,
        allowance_raw: str,
        deduction_raw: str,
    ) -> None:
        if not full_name.strip():
            messagebox.showwarning("Thiếu dữ liệu", "Nhập họ tên.")
            return
        try:
            base = float(base_raw.replace(",", "").strip())
            allowance = float(allowance_raw.replace(",", "").strip() or 0)
            deduction = float(deduction_raw.replace(",", "").strip() or 0)
        except ValueError:
            messagebox.showerror("Số không hợp lệ", "Lương, phụ cấp, khấu trừ phải là số.")
            return
        self.controller.add_employee(full_name, department, base, allowance, deduction)
        self.form.clear_form()
        messagebox.showinfo("Đã lưu", "Đã thêm nhân viên.")
