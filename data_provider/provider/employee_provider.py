"""
employee_provider.py
Interfaz para acceso a la tabla employees.
"""
from abc import ABC, abstractmethod
from typing import List
from core.entity.employee import Employee

class EmployeeProvider(ABC):
    @abstractmethod
    def get_all_employees(self) -> List[Employee]:
        pass

    @abstractmethod
    def insert_employees(self, employees: List[Employee]) -> None:
        pass

    @abstractmethod
    def delete_all(self) -> None:
        pass
