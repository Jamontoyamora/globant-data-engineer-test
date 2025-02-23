"""
report_service_impl.py
Implementación del servicio de reportes.
"""
from typing import List
from controller.dto.report_dto import HiredByQuarterResponse, DepartmentAboveMeanResponse
from controller.service.report_service import ReportService
from core.use_case.report_use_case import ReportUseCase

class ReportServiceImpl(ReportService):
    def __init__(self, report_use_case: ReportUseCase):
        self.use_case = report_use_case

    def get_hired_by_quarter(self, year: int) -> List[HiredByQuarterResponse]:
        data = self.use_case.get_hired_by_quarter(year)
        return [
            HiredByQuarterResponse(**record) for record in data
        ]

    def get_departments_above_mean(self, year: int) -> List[DepartmentAboveMeanResponse]:
        data = self.use_case.get_departments_above_mean(year)
        return [
            DepartmentAboveMeanResponse(**record) for record in data
        ]
