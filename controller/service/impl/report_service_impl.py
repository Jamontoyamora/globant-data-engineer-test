"""
report_service_impl.py
Implementación del servicio de reportes.
"""
from typing import List
from controller.dto.report_dto import HiredByQuarterResponse, DepartmentAboveMeanResponse
from controller.service.report_service import ReportService
from core.use_case.report_use_case import ReportUseCase
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import tempfile

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

    def generate_report_pdf(self, year: int) -> str:
        hired_by_quarter = self.get_hired_by_quarter(year)
        departments_above_mean = self.get_departments_above_mean(year)

        df_hired_by_quarter = pd.DataFrame([record.dict() for record in hired_by_quarter])
        df_departments_above_mean = pd.DataFrame([record.dict() for record in departments_above_mean])

        sns.set(style="whitegrid")

        fig, axes = plt.subplots(2, 1, figsize=(10, 15))

        sns.barplot(
            x="department", y="Q1", hue="job", data=df_hired_by_quarter, ax=axes[0]
        ).set_title("Contrataciones por Trimestre (Q1)")
        sns.barplot(
            x="department", y="hired", data=df_departments_above_mean, ax=axes[1]
        ).set_title("Departamentos por Encima de la Media de Contrataciones")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
            plt.savefig(tmpfile.name)
            return tmpfile.name
