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

        self.form = EmployeeView(self, on_add=self._handle_add)
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
        ttk.Button(search_frame, text="Xóa tìm kiếm", command=lambda: self.search_var.set("")).pack(side=tk.LEFT)

        table_frame = ttk.LabelFrame(self, text="Danh sách lương nhân viên", padding=8)
        table_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = self._build_table(table_frame)
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=(8, 0))
        
        # Nút xem thống kê cho mọi người dùng
        ttk.Button(btn_frame, text="Xem Thống Kê", command=self._handle_stats).pack(side=tk.LEFT)
        
        # Chỉ hiển thị nút xóa cho admin
        if self.role == "admin":
            ttk.Button(btn_frame, text="Xóa nhân viên", command=self._handle_delete).pack(side=tk.RIGHT)
            
        ttk.Button(btn_frame, text="Xuất Excel (CSV)", command=self._handle_export).pack(side=tk.RIGHT, padx=(0, 8))

        self.refresh_table()

    def _build_table(self, parent):
        cols = ("id", "full_name", "department", "base", "allowance", "deduction", "working", "overtime", "net")
        tree = ttk.Treeview(parent, columns=cols, show="headings", height=12)
        
        headings = {
            "id": "Mã NV", "full_name": "Họ tên", "department": "Phòng ban",
            "base": "Lương CB", "allowance": "Phụ cấp", "deduction": "Khấu trừ",
            "working": "Ngày công", "overtime": "Giờ LT", "net": "Thực nhận"
        }
        widths = {
            "id": 80, "full_name": 140, "department": 100, "base": 90,
            "allowance": 80, "deduction": 80, "working": 70, "overtime": 60, "net": 90
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
                    e.working_days,
                    e.overtime_hours,
                    f"{e.net_salary():,.0f}"
                )
            )

    def _handle_add(self, full_name, department, base_raw, allowance_raw, deduction_raw, working_days_raw, overtime_hours_raw):
        """Xử lý sự kiện nhấn nút thêm nhân viên."""
        if not full_name.strip():
            messagebox.showwarning("Thiếu dữ liệu", "Họ tên không được để trống!")
            return
        try:
            base = float(base_raw.replace(",", "").strip())
            allowance = float(allowance_raw.replace(",", "").strip() or 0)
            deduction = float(deduction_raw.replace(",", "").strip() or 0)
            working_days = int(working_days_raw.strip() or 0)
            overtime_hours = float(overtime_hours_raw.strip() or 0)
        except ValueError:
            messagebox.showerror("Số không hợp lệ", "Vui lòng nhập đúng định dạng số cho lương, phụ cấp, khấu trừ, ngày công, giờ làm thêm.")
            return
            
        self.controller.add_employee(full_name, department, base, allowance, deduction, working_days, overtime_hours)
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
                writer.writerow(["Mã NV", "Họ tên", "Phòng ban", "Lương CB", "Phụ cấp", "Khấu trừ", "Ngày công", "Giờ làm thêm", "Thực nhận"])
                for e in self.controller.list_employees():
                    writer.writerow([
                        e.id, e.full_name, e.department, e.base_salary,
                        e.allowance, e.deduction, e.working_days, e.overtime_hours, e.net_salary()
                    ])
            messagebox.showinfo("Thành công", f"Đã xuất file bảng lương thành công:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất file:\n{str(e)}")

    def _handle_stats(self):
        """Hiển thị hộp thoại thống kê thông tin lương và làm thêm."""
        total_hours = self.controller.get_total_overtime_hours()
        growth_rate = self.controller.get_salary_growth_rate()
        msg = (
            f"Tỷ lệ tăng trưởng lương trung bình: {growth_rate}%\n\n"
            f"Tổng số giờ làm thêm: {total_hours} giờ"
        )
        messagebox.showinfo("Thống kê", msg)
