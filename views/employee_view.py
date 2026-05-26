import tkinter as tk
from tkinter import ttk

class EmployeeView(ttk.LabelFrame):
    def __init__(self, master, on_add):
        super().__init__(master, text="Thêm nhân viên mới", padding=10)
        self._on_add = on_add

        # Các nhãn và ô nhập dữ liệu
        row = 0
        ttk.Label(self, text="Họ tên:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.full_name = ttk.Entry(self, width=30)
        self.full_name.grid(row=row, column=1, sticky=tk.EW, pady=2)
        row += 1

        ttk.Label(self, text="Phòng ban:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.department = ttk.Entry(self, width=30)
        self.department.grid(row=row, column=1, sticky=tk.EW, pady=2)
        row += 1

        ttk.Label(self, text="Lương cơ bản:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.base_salary = ttk.Entry(self, width=30)
        self.base_salary.grid(row=row, column=1, sticky=tk.EW, pady=2)
        row += 1

        ttk.Label(self, text="Phụ cấp:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.allowance = ttk.Entry(self, width=30)
        self.allowance.insert(0, "0")
        self.allowance.grid(row=row, column=1, sticky=tk.EW, pady=2)
        row += 1

        ttk.Label(self, text="Khấu trừ:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.deduction = ttk.Entry(self, width=30)
        self.deduction.insert(0, "0")
        self.deduction.grid(row=row, column=1, sticky=tk.EW, pady=2)
        row += 1

        ttk.Label(self, text="Ngày công:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.working_days = ttk.Entry(self, width=30)
        self.working_days.insert(0, "26")
        self.working_days.grid(row=row, column=1, sticky=tk.EW, pady=2)
        row += 1

        ttk.Label(self, text="Giờ làm thêm:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.overtime_hours = ttk.Entry(self, width=30)
        self.overtime_hours.insert(0, "0")
        self.overtime_hours.grid(row=row, column=1, sticky=tk.EW, pady=2)
        row += 1

        # Nút xác nhận thêm
        ttk.Button(self, text="Thêm nhân viên", command=self._submit).grid(
            row=row, column=1, sticky=tk.E, pady=(8, 0)
        )

        self.columnconfigure(1, weight=1)

    def _submit(self):
        """Gửi các thông tin đã nhập về hàm xử lý (on_add)."""
        self._on_add(
            self.full_name.get(),
            self.department.get(),
            self.base_salary.get(),
            self.allowance.get(),
            self.deduction.get(),
            self.working_days.get(),
            self.overtime_hours.get()
        )

    def clear_form(self):
        """Xóa trắng toàn bộ dữ liệu trên form và thiết lập giá trị mặc định."""
        self.full_name.delete(0, tk.END)
        self.department.delete(0, tk.END)
        self.base_salary.delete(0, tk.END)
        
        self.allowance.delete(0, tk.END)
        self.allowance.insert(0, "0")
        
        self.deduction.delete(0, tk.END)
        self.deduction.insert(0, "0")
        
        self.working_days.delete(0, tk.END)
        self.working_days.insert(0, "26")
        
        self.overtime_hours.delete(0, tk.END)
        self.overtime_hours.insert(0, "0")
