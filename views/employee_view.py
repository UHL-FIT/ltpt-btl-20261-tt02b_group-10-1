import tkinter as tk
from tkinter import ttk

class EmployeeView(ttk.LabelFrame):
    def __init__(self, master, on_add, on_edit=None, on_cancel=None):
        super().__init__(master, text="Thêm nhân viên mới", padding=10)
        self._on_add = on_add
        self._on_edit = on_edit
        self._on_cancel = on_cancel
        self.is_edit_mode = False
        self.editing_id = None

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

        # Hàng chữ thuế mặc định 10% dưới khấu trừ
        tax_lbl = tk.Label(self, text="* Thuế là 10% (tự động trừ vào thực nhận)", fg="#E74C3C", font=("Helvetica", 9, "italic"))
        tax_lbl.grid(row=row, column=1, sticky=tk.W, pady=(2, 6))
        row += 1

        # Nút xác nhận thêm / sửa và nút hủy
        self.btn_container = ttk.Frame(self)
        self.btn_container.grid(row=row, column=1, sticky=tk.E, pady=(12, 0))

        self.cancel_btn = tk.Button(self.btn_container, text="Hủy", command=self._cancel, bg="#95A5A6", fg="white", activebackground="#7F8C8D", activeforeground="white", relief="flat", bd=0, padx=15, pady=6)

        self.submit_btn = tk.Button(self.btn_container, text="Thêm nhân viên", command=self._submit, bg="#2ECC71", fg="white", activebackground="#27AE60", activeforeground="white", relief="flat", bd=0, padx=15, pady=6)
        self.submit_btn.pack(side=tk.RIGHT)

        self.columnconfigure(1, weight=1)

    def _submit(self):
        """Gửi các thông tin đã nhập về hàm xử lý."""
        if self.is_edit_mode:
            if self._on_edit:
                self._on_edit(
                    self.editing_id,
                    self.full_name.get(),
                    self.department.get(),
                    self.base_salary.get(),
                    self.allowance.get(),
                    self.deduction.get()
                )
        else:
            self._on_add(
                self.full_name.get(),
                self.department.get(),
                self.base_salary.get(),
                self.allowance.get(),
                self.deduction.get()
            )

    def _cancel(self):
        if self._on_cancel:
            self._on_cancel()

    def set_edit_mode(self, is_edit, employee=None):
        self.is_edit_mode = is_edit
        if is_edit and employee:
            self.editing_id = employee.id
            self.configure(text=f"Sửa thông tin nhân viên (Mã NV: {employee.id})")
            self.submit_btn.configure(text="Lưu thay đổi", bg="#3498DB", activebackground="#2980B9")
            
            # Hiển thị nút hủy
            self.cancel_btn.pack(side=tk.RIGHT, padx=(0, 8))
            
            # Điền dữ liệu của nhân viên được chọn
            self.full_name.delete(0, tk.END)
            self.full_name.insert(0, employee.full_name)
            self.department.delete(0, tk.END)
            self.department.insert(0, employee.department)
            
            def fmt(val):
                return f"{int(val)}" if val.is_integer() else f"{val}"
            
            self.base_salary.delete(0, tk.END)
            self.base_salary.insert(0, fmt(employee.base_salary))
            self.allowance.delete(0, tk.END)
            self.allowance.insert(0, fmt(employee.allowance))
            self.deduction.delete(0, tk.END)
            self.deduction.insert(0, fmt(employee.deduction))
        else:
            self.editing_id = None
            self.configure(text="Thêm nhân viên mới")
            self.submit_btn.configure(text="Thêm nhân viên", bg="#2ECC71", activebackground="#27AE60")
            self.cancel_btn.pack_forget()
            self.clear_form()

    def clear_form(self):
        """Xóa trắng toàn bộ dữ liệu trên form và thiết lập giá trị mặc định."""
        self.full_name.delete(0, tk.END)
        self.department.delete(0, tk.END)
        self.base_salary.delete(0, tk.END)
        
        self.allowance.delete(0, tk.END)
        self.allowance.insert(0, "0")
        
        self.deduction.delete(0, tk.END)
        self.deduction.insert(0, "0")
