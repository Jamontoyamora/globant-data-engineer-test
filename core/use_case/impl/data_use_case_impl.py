"""
data_use_case.py
Caso de uso para insertar datos (batch o CSV).
No interactúa con modelos de infraestructura directamente, solo con entidades.
Valida reglas de negocio y llama a los providers.
"""

from core.use_case.data_use_case import DataUseCase
from common.lib.logging import logger
from core.entity.department import Department
from core.entity.job import Job
from core.entity.employee import Employee
from data_provider.provider.department_provider import DepartmentProvider
from data_provider.provider.job_provider import JobProvider
from data_provider.provider.employee_provider import EmployeeProvider


class DataUseCaseImpl(DataUseCase):
    def __init__(
        self,
        department_provider: DepartmentProvider,
        job_provider: JobProvider,
        employee_provider: EmployeeProvider,
    ):
        self.department_provider = department_provider
        self.job_provider = job_provider
        self.employee_provider = employee_provider

    def insert_data(self, departments: list, jobs: list, employees: list) -> int:
        """
        Inserta datos, validando campos y registrando en log los inválidos.
        Retorna la cantidad de registros inválidos.
        """
        invalid_count = 0

        # Insertar departments
        department_entities = []
        for d in departments:
            if self._validate_department(d):
                department_entities.append(Department(d["id"], d["department"]))
            else:
                invalid_count += 1
                logger.error(f"Registro inválido en departments: {d}")

        # Insertar jobs
        job_entities = []
        for j in jobs:
            if self._validate_job(j):
                job_entities.append(Job(j["id"], j["job"]))
            else:
                invalid_count += 1
                logger.error(f"Registro inválido en jobs: {j}")

        # Insertar employees
        employee_entities = []
        for e in employees:
            if self._validate_employee(e):
                employee_entities.append(
                    Employee(
                        e["id"],
                        e["name"],
                        e["datetime"],
                        e["department_id"],
                        e["job_id"],
                    )
                )
            else:
                invalid_count += 1
                logger.error(f"Registro inválido en employees: {e}")

        # Finalmente, insertar en DB
        if department_entities:
            self.department_provider.insert_departments(department_entities)
        if job_entities:
            self.job_provider.insert_jobs(job_entities)
        if employee_entities:
            self.employee_provider.insert_employees(employee_entities)

        return invalid_count

    def _validate_department(self, d: dict) -> bool:
        return (
            d.get("id") is not None
            and d.get("department") is not None
            and isinstance(d["id"], int)
            and isinstance(d["department"], str)
            and len(d["department"].strip()) > 0
        )

    def _validate_job(self, j: dict) -> bool:
        return (
            j.get("id") is not None
            and j.get("job") is not None
            and isinstance(j["id"], int)
            and isinstance(j["job"], str)
            and len(j["job"].strip()) > 0
        )

    def _validate_employee(self, e: dict) -> bool:
        if any(
            k not in e for k in ["id", "name", "datetime", "department_id", "job_id"]
        ):
            return False
        if not all(
            e[k] is not None
            for k in ["id", "name", "datetime", "department_id", "job_id"]
        ):
            return False
        # Validar tipos
        if not isinstance(e["id"], int):
            return False
        if not isinstance(e["name"], str):
            return False
        if not isinstance(e["datetime"], str):
            return False
        if not isinstance(e["department_id"], int):
            return False
        if not isinstance(e["job_id"], int):
            return False
        # Podrías validar formato de fecha/hora (ISO 8601)
        return True
