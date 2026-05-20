"""Điều phối thao tác nhân viên và lưu JSON."""
from __future__ import annotations

import uuid
from typing import Callable

from models.employee import Employee
from utils.file_handler import load_json, save_json


class EmployeeController:
    def __init__(self, on_changed: Callable[[], None] | None = None) -> None:
        self._on_changed = on_changed

    def _notify(self) -> None:
        if self._on_changed:
            self._on_changed()

    def list_employees(self) -> list[Employee]:
        raw = load_json("employees.json", default=[])
        if not isinstance(raw, list):
            return []
        out: list[Employee] = []
        for item in raw:
            if isinstance(item, dict):
                try:
                    out.append(Employee.from_dict(item))
                except (KeyError, TypeError, ValueError):
                    continue
        return out

    def add_employee(
        self,
        full_name: str,
        department: str,
        base_salary: float,
        allowance: float,
        deduction: float,
    ) -> Employee:
        employees = self.list_employees()
        emp = Employee(
            full_name=full_name.strip(),
            department=department.strip(),
            base_salary=base_salary,
            allowance=allowance,
            deduction=deduction,
        )
        employees.append(emp)
        save_json(
            "employees.json",
            [e.to_dict() for e in employees],
        )
        self._notify()
        return emp
