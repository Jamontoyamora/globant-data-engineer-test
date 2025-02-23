"""
employee.py
Entidad pura de dominio para Employee.
"""

class Employee:
    def __init__(self, id: int, name: str, datetime: str, department_id: int, job_id: int):
        self.id = id
        self.name = name
        self.datetime = datetime
        self.department_id = department_id
        self.job_id = job_id

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "datetime": self.datetime,
            "department_id": self.department_id,
            "job_id": self.job_id
        }
