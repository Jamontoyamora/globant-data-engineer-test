"""
report_use_case.py
Caso de uso para generar reportes de contrataciones (Challenge #2).
Usa los providers para obtener datos.
"""

from core.use_case.report_use_case import ReportUseCase
from data_provider.provider.employee_provider import EmployeeProvider
from data_provider.provider.department_provider import DepartmentProvider
from data_provider.provider.job_provider import JobProvider
import datetime


class ReportUseCaseImpl(ReportUseCase):
    def __init__(
        self,
        employee_provider: EmployeeProvider,
        department_provider: DepartmentProvider,
        job_provider: JobProvider,
    ):
        self.employee_provider = employee_provider
        self.department_provider = department_provider
        self.job_provider = job_provider

    def get_hired_by_quarter(self, year: int):
        """
        Retorna una lista de diccionarios con:
        {
          "department": str,
          "job": str,
          "Q1": int,
          "Q2": int,
          "Q3": int,
          "Q4": int
        }
        Ordenado alfabéticamente por department y job.
        """
        # 1. Obtener todos los empleados
        employees = self.employee_provider.get_all_employees()
        # 2. Filtrar por año
        filtered = [emp for emp in employees if emp.datetime.startswith(str(year))]

        # 3. Agrupar por department_id, job_id y por trimestre
        #   Convertir emp.datetime a datetime real para sacar trimestre
        #   Ej: 2021-07-27T16:02:08Z -> date.month = 7 => Q3
        # 4. Mapear department_id -> department_name, job_id -> job_name
        departments_map = {
            d.id: d.department for d in self.department_provider.get_all_departments()
        }
        jobs_map = {j.id: j.job for j in self.job_provider.get_all_jobs()}

        # Estructura: {(dept, job): [countQ1, countQ2, countQ3, countQ4]}
        aggregator = {}

        for emp in filtered:
            dept_name = departments_map.get(emp.department_id, "Unknown")
            job_name = jobs_map.get(emp.job_id, "Unknown")

            # Parse mes
            try:
                dt = datetime.datetime.fromisoformat(
                    emp.datetime.replace("Z", "+00:00")
                )
                month = dt.month
            except:
                # Si no es parseable, ignorar o loguear
                continue
            quarter = (month - 1) // 3 + 1  # 1..4

            key = (dept_name, job_name)
            if key not in aggregator:
                aggregator[key] = [0, 0, 0, 0]
            aggregator[key][quarter - 1] += 1

        # 5. Convertir aggregator a lista
        result_list = []
        for (dept_name, job_name), quarters in aggregator.items():
            result_list.append(
                {
                    "department": dept_name,
                    "job": job_name,
                    "Q1": quarters[0],
                    "Q2": quarters[1],
                    "Q3": quarters[2],
                    "Q4": quarters[3],
                }
            )

        # Ordenar alfabéticamente por department, luego job
        result_list.sort(key=lambda x: (x["department"], x["job"]))

        return result_list

    def get_departments_above_mean(self, year: int):
        """
        Retorna [{
          "id": int,
          "department": str,
          "hired": int
        }] para los departamentos con contrataciones > promedio.
        """
        employees = self.employee_provider.get_all_employees()
        filtered = [emp for emp in employees if emp.datetime.startswith(str(year))]

        # Contar contrataciones por departamento
        dept_counts = {}
        for emp in filtered:
            dept_counts[emp.department_id] = dept_counts.get(emp.department_id, 0) + 1

        if not dept_counts:
            return []

        # Calcular promedio
        total_hired = sum(dept_counts.values())
        dept_count = len(dept_counts)
        mean_value = total_hired / dept_count if dept_count else 0

        # Mapear id -> nombre
        departments_map = {
            d.id: d.department for d in self.department_provider.get_all_departments()
        }

        # Filtrar los que superan la media
        above = []
        for dept_id, hired in dept_counts.items():
            if hired > mean_value:
                above.append(
                    {
                        "id": dept_id,
                        "department": departments_map.get(dept_id, "Unknown"),
                        "hired": hired,
                    }
                )

        # Ordenar desc por hired
        above.sort(key=lambda x: x["hired"], reverse=True)
        return above
