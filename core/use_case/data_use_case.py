"""
abstract_data_use_case.py
Clase abstracta para el caso de uso de inserción de datos.
"""
from abc import ABC, abstractmethod

class DataUseCase(ABC):
    @abstractmethod
    def insert_data(self, departments: list, jobs: list, employees: list) -> int:
        pass
