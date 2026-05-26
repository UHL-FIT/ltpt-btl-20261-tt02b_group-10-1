class Employee:
    def __init__(self, id, full_name, department, base_salary, allowance, deduction, working_days=0, overtime_hours=0.0):
        self.id = str(id)
        self.full_name = str(full_name)
        self.department = str(department)
        self.base_salary = float(base_salary)
        self.allowance = float(allowance)
        self.deduction = float(deduction)
        self.working_days = int(working_days)
        self.overtime_hours = float(overtime_hours)

    def net_salary(self):
        """Lương thực nhận = Lương cơ bản + Phụ cấp - Khấu trừ"""
        return self.base_salary + self.allowance - self.deduction

    def to_dict(self):
        """Chuyển thông tin nhân viên thành dictionary để lưu vào JSON."""
        return {
            "id": self.id,
            "full_name": self.full_name,
            "department": self.department,
            "base_salary": self.base_salary,
            "allowance": self.allowance,
            "deduction": self.deduction,
            "working_days": self.working_days,
            "overtime_hours": self.overtime_hours,
            "net_salary": round(self.net_salary(), 2)
        }

    @staticmethod
    def from_dict(data):
        """Tạo đối tượng Employee từ dữ liệu dictionary đọc từ JSON."""
        return Employee(
            id=data.get("id"),
            full_name=data.get("full_name"),
            department=data.get("department", ""),
            base_salary=data.get("base_salary", 0.0),
            allowance=data.get("allowance", 0.0),
            deduction=data.get("deduction", 0.0),
            working_days=data.get("working_days", 0),
            overtime_hours=data.get("overtime_hours", 0.0)
        )
