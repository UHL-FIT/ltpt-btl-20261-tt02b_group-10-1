class Employee:
    def __init__(self, id, full_name, department, base_salary, allowance, deduction):
        self.id = str(id)
        self.full_name = str(full_name)
        self.department = str(department)
        self.base_salary = float(base_salary)
        self.allowance = float(allowance)
        self.deduction = float(deduction)

    def net_salary(self):
        """Lương thực nhận = (Lương cơ bản + Phụ cấp - Khấu trừ) * 0.9 (Trừ đi 10% thuế mặc định)"""
        pre_tax = (self.base_salary + self.allowance) - self.deduction
        return pre_tax * 0.9

    def to_dict(self):
        """Chuyển thông tin nhân viên thành dictionary để lưu vào JSON."""
        return {
            "id": self.id,
            "full_name": self.full_name,
            "department": self.department,
            "base_salary": self.base_salary,
            "allowance": self.allowance,
            "deduction": self.deduction,
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
            deduction=data.get("deduction", 0.0)
        )
