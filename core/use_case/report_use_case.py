"""
abstract_report_use_case.py
Clase abstracta para el caso de uso de reportes.
"""
from abc import ABC, abstractmethod

class ReportUseCase(ABC):
    @abstractmethod
    def get_hired_by_quarter(self, year: int):
        pass

    @abstractmethod
    def get_departments_above_mean(self, year: int):
        pass
