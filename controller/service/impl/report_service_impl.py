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
from matplotlib.backends.backend_pdf import PdfPages

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

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
            pdf_pages = PdfPages(tmpfile.name)

            # Crear una tabla con múltiples páginas si es necesario
            max_rows_per_page = 25  # Ajusta según sea necesario
            total_rows = len(df_hired_by_quarter)
            num_pages = (total_rows // max_rows_per_page) + (1 if total_rows % max_rows_per_page != 0 else 0)

            for page in range(num_pages):
                fig, ax = plt.subplots(figsize=(10, 6))  # Ajusta tamaño de la página
                ax.axis("off")

                start_row = page * max_rows_per_page
                end_row = min((page + 1) * max_rows_per_page, total_rows)

                table_data = [df_hired_by_quarter.columns.tolist()] + df_hired_by_quarter.iloc[start_row:end_row].values.tolist()
                table = ax.table(cellText=table_data, colLabels=None, cellLoc='center', loc='center')

                table.auto_set_font_size(False)
                table.set_fontsize(8)
                table.auto_set_column_width([i for i in range(len(df_hired_by_quarter.columns))])  
                
                ax.set_title(f"Contrataciones por Trimestre - Página {page + 1}")
                pdf_pages.savefig(fig)
                plt.close(fig)

            # Agregar gráfico de barras
            fig, ax = plt.subplots(figsize=(10, 6))
            df_departments_above_mean["department"] = df_departments_above_mean["department"].str.replace(" ", "\n")
            sns.barplot(x="department", y="hired", data=df_departments_above_mean, ax=ax, color="steelblue")
            ax.set_title("Departamentos por Encima de la Media de Contrataciones")
            ax.set_xticklabels(ax.get_xticklabels(), ha="center")

            pdf_pages.savefig(fig)
            plt.close(fig)

            pdf_pages.close()
            return tmpfile.name
