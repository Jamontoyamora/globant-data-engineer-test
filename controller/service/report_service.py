"""
report_service.py
Interfaz del servicio para reportes.
"""
from abc import ABC, abstractmethod
from typing import List
from controller.dto.report_dto import HiredByQuarterResponse, DepartmentAboveMeanResponse

class ReportService(ABC):
    @abstractmethod
    def get_hired_by_quarter(self, year: int) -> List[HiredByQuarterResponse]:
        pass

    @abstractmethod
    def get_departments_above_mean(self, year: int) -> List[DepartmentAboveMeanResponse]:
        pass

    @abstractmethod
    def generate_report_pdf(self, year: int) -> str:
        pass
