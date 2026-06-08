import csv
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from controllers.employee_controller import EmployeeController
from views.employee_view import EmployeeView

class MainView(ttk.Frame):
    def __init__(self, master, role="viewer"):
        super().__init__(master, padding=12)
        self.pack(fill=tk.BOTH, expand=True)
        
        self.role = role
        self.controller = EmployeeController(on_changed=self.refresh_table)

        self.form = EmployeeView(
            self,
            on_add=self._handle_add,
            on_edit=self._handle_edit_submit,
            on_cancel=self._handle_edit_cancel
        )
        # Chỉ hiển thị form nhập nếu là admin
        if self.role == "admin":
            self.form.pack(fill=tk.X, pady=(0, 12))

        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X, pady=(0, 8))
        
        ttk.Label(search_frame, text="Tìm kiếm theo mã NV:").pack(side=tk.LEFT, padx=(0, 8))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.refresh_table)
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 8))
        tk.Button(search_frame, text="Xóa tìm kiếm", command=lambda: self.search_var.set(""), bg="#BDC3C7", fg="black", activebackground="#95A5A6", activeforeground="black", relief="flat", bd=0, padx=8, pady=2).pack(side=tk.LEFT)

        # Khung chứa các nút chức năng (Đặt ở phía dưới cùng để không bị che khuất khi thu nhỏ)
        btn_frame = ttk.Frame(self)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(8, 0))
        
        # Nút xem thống kê cho mọi người dùng (Màu cam/vàng)
        tk.Button(btn_frame, text="Xem Thống Kê", command=self._handle_stats, bg="#F39C12", fg="white", activebackground="#D35400", activeforeground="white", relief="flat", bd=0, padx=12, pady=5).pack(side=tk.LEFT)
        
        # Chỉ hiển thị nút xóa và nút sửa cho admin
        if self.role == "admin":
            tk.Button(btn_frame, text="Xóa nhân viên", command=self._handle_delete, bg="#E74C3C", fg="white", activebackground="#C0392B", activeforeground="white", relief="flat", bd=0, padx=12, pady=5).pack(side=tk.RIGHT)
            tk.Button(btn_frame, text="Sửa nhân viên", command=self._handle_edit, bg="#3498DB", fg="white", activebackground="#2980B9", activeforeground="white", relief="flat", bd=0, padx=12, pady=5).pack(side=tk.RIGHT, padx=(0, 8))
            
        # Nút xuất Excel (Màu xanh ngọc lam)
        tk.Button(btn_frame, text="Xuất Excel (CSV)", command=self._handle_export, bg="#1ABC9C", fg="white", activebackground="#16A085", activeforeground="white", relief="flat", bd=0, padx=12, pady=5).pack(side=tk.RIGHT, padx=(0, 8))

        # Bảng danh sách lương (Đặt ở giữa và tự động co giãn)
        table_frame = ttk.LabelFrame(self, text="Danh sách lương nhân viên", padding=8)
        table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.tree = self._build_table(table_frame)
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.refresh_table()

    def _build_table(self, parent):
        cols = ("id", "full_name", "department", "base", "allowance", "deduction", "net")
        tree = ttk.Treeview(parent, columns=cols, show="headings", height=12)
        
        headings = {
            "id": "Mã NV", "full_name": "Họ tên", "department": "Phòng ban",
            "base": "Lương CB", "allowance": "Phụ cấp", "deduction": "Khấu trừ",
            "net": "Thực nhận"
        }
        widths = {
            "id": 80, "full_name": 140, "department": 100, "base": 90,
            "allowance": 80, "deduction": 80, "net": 90
        }
        for c in cols:
            tree.heading(c, text=headings[c])
            tree.column(c, width=widths[c], anchor=tk.CENTER if c not in ("full_name", "department") else tk.W)
        return tree

    def refresh_table(self, *args):
        """Xóa bảng cũ và load danh sách nhân viên mới có lọc theo tìm kiếm."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        search_query = self.search_var.get().strip().lower() if hasattr(self, "search_var") else ""
            
        for e in self.controller.list_employees():
            if search_query and search_query not in e.id.lower():
                continue
                
            self.tree.insert(
                "", tk.END, iid=e.id,
                values=(
                    e.id,
                    e.full_name,
                    e.department,
                    f"{e.base_salary:,.0f}",
                    f"{e.allowance:,.0f}",
                    f"{e.deduction:,.0f}",
                    f"{e.net_salary():,.0f}"
                )
            )

    def _handle_add(self, full_name, department, base_raw, allowance_raw, deduction_raw):
        """Xử lý sự kiện nhấn nút thêm nhân viên."""
        if not full_name.strip():
            messagebox.showwarning("Thiếu dữ liệu", "Họ tên không được để trống!")
            return
        try:
            base = float(base_raw.replace(",", "").strip())
            allowance = float(allowance_raw.replace(",", "").strip() or 0)
            deduction = float(deduction_raw.replace(",", "").strip() or 0)
        except ValueError:
            messagebox.showerror("Số không hợp lệ", "Vui lòng nhập đúng định dạng số cho lương, phụ cấp, khấu trừ.")
            return
            
        self.controller.add_employee(full_name, department, base, allowance, deduction)
        self.form.clear_form()
        messagebox.showinfo("Thành công", "Đã thêm nhân viên thành công.")

    def _handle_delete(self):
        """Xử lý sự kiện nhấn nút xóa nhân viên."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn nhân viên cần xóa khỏi bảng.")
            return
        
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa nhân viên đã chọn?"):
            for item in selected:
                self.controller.delete_employee(item)
            messagebox.showinfo("Thành công", "Đã xóa nhân viên thành công.")

    def _handle_export(self):
        """Xuất danh sách bảng lương ra tệp CSV."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV (Excel)", "*.csv"), ("All files", "*.*")],
            title="Lưu bảng lương"
        )
        if not file_path:
            return
            
        try:
            with open(file_path, mode="w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(["Mã NV", "Họ tên", "Phòng ban", "Lương CB", "Phụ cấp", "Khấu trừ", "Thực nhận"])
                for e in self.controller.list_employees():
                    writer.writerow([
                        e.id, e.full_name, e.department, e.base_salary,
                        e.allowance, e.deduction, e.net_salary()
                    ])
            messagebox.showinfo("Thành công", f"Đã xuất file bảng lương thành công:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất file:\n{str(e)}")

    def _handle_stats(self):
        """Hiển thị hộp thoại thống kê thông tin lương."""
        growth_rate = self.controller.get_salary_growth_rate()
        msg = f"Tỷ lệ tăng trưởng lương trung bình: {growth_rate}%"
        messagebox.showinfo("Thống kê", msg)

    def _handle_edit(self):
        """Xử lý khi nhấn nút Sửa nhân viên ở bảng điều khiển."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn nhân viên cần sửa từ danh sách.")
            return
        
        emp_id = selected[0]
        emp = None
        for e in self.controller.list_employees():
            if e.id == emp_id:
                emp = e
                break
        
        if emp:
            self.form.set_edit_mode(True, emp)
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy thông tin nhân viên.")

    def _handle_edit_submit(self, emp_id, full_name, department, base_raw, allowance_raw, deduction_raw):
        """Xử lý cập nhật thông tin nhân viên sau khi người dùng sửa và lưu."""
        if not full_name.strip():
            messagebox.showwarning("Thiếu dữ liệu", "Họ tên không được để trống!")
            return
        try:
            base = float(base_raw.replace(",", "").strip())
            allowance = float(allowance_raw.replace(",", "").strip() or 0)
            deduction = float(deduction_raw.replace(",", "").strip() or 0)
        except ValueError:
            messagebox.showerror("Số không hợp lệ", "Vui lòng nhập đúng định dạng số cho lương, phụ cấp, khấu trừ.")
            return
            
        success = self.controller.update_employee(emp_id, full_name, department, base, allowance, deduction)
        if success:
            self.form.set_edit_mode(False)
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin nhân viên thành công.")
        else:
            messagebox.showerror("Lỗi", "Cập nhật thất bại. Nhân viên không tồn tại.")

    def _handle_edit_cancel(self):
        """Hủy bỏ chế độ sửa và quay lại chế độ thêm nhân viên mới."""
        self.form.set_edit_mode(False)
