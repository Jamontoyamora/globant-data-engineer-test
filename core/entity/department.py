"""
department.py
Entidad pura de dominio para Department.
"""

class Department:
    def __init__(self, id: int, department: str):
        self.id = id
        self.department = department

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "department": self.department
        }
