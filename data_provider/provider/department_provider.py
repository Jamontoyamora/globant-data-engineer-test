"""
department_provider.py
Interfaz de acceso a la tabla departments (patrón Repository/Provider).
"""
from abc import ABC, abstractmethod
from typing import List
from core.entity.department import Department

class DepartmentProvider(ABC):
    @abstractmethod
    def get_all_departments(self) -> List[Department]:
        pass

    @abstractmethod
    def insert_departments(self, departments: List[Department]) -> None:
        pass

    @abstractmethod
    def delete_all(self) -> None:
        pass
