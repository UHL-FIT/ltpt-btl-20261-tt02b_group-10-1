"""Model nhân viên và công thức tính lương thực nhận."""
from __future__ import annotations
import uuid                                    
from dataclasses import dataclass, field, asdict
from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class Employee:
    
    full_name: str
    department: str
    base_salary: float
    allowance: float
    deduction: float
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def net_salary(self) -> float:
        """Lương thực nhận = lương cơ bản + phụ cấp - khấu trừ."""
        return self.base_salary + self.allowance - self.deduction

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["net_salary"] = round(self.net_salary(), 2)
        return d

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "Employee":
        return Employee(
            id=str(data["id"]),
            full_name=str(data["full_name"]),
            department=str(data.get("department", "")),
            base_salary=float(data["base_salary"]),
            allowance=float(data.get("allowance", 0)),
            deduction=float(data.get("deduction", 0)),
        )
