"""Xác thực đăng nhập (đọc từ users.json)."""
from __future__ import annotations

from utils.file_handler import load_json


def verify(username: str, password: str) -> bool:
    users = load_json("users.json", default=[])
    if not isinstance(users, list):
        return False
    for u in users:
        if not isinstance(u, dict):
            continue
        if u.get("username") == username and u.get("password") == password:
            return True
    return False
