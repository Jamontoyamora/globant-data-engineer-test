"""
backup_use_case.py
Casos de uso para generar y restaurar datos desde un backup en AVRO.
No conoce ni de DTOs ni de infraestructura directamente; se apoya en interfaces.
"""
from core.use_case.backup_use_case import BackupUseCase
from common.utils.enums.table_enums import TableEnum
from core.entity.department import Department
from core.entity.job import Job
from core.entity.employee import Employee
from data_provider.provider.department_provider import DepartmentProvider
from data_provider.provider.job_provider import JobProvider
from data_provider.provider.employee_provider import EmployeeProvider

class BackupUseCaseImpl(BackupUseCase):
    def __init__(
        self,
        department_provider: DepartmentProvider,
        job_provider: JobProvider,
        employee_provider: EmployeeProvider,
    ):
        self.department_provider = department_provider
        self.job_provider = job_provider
        self.employee_provider = employee_provider

    def get_data_for_backup(self, table_name: str):
        """
        Retorna la lista de entidades para la tabla especificada.
        """
        if table_name == TableEnum.DEPARTMENTS:
            return self.department_provider.get_all_departments()
        elif table_name == TableEnum.JOBS:
            return self.job_provider.get_all_jobs()
        else:
            return self.employee_provider.get_all_employees()

    def restore_data_from_backup(self, table_name: str, records: list):
        """
        Inserta los datos de la tabla a partir de la lista de diccionarios extraídos del AVRO.
        """
        if table_name == TableEnum.DEPARTMENTS:
            entities = [Department(**r) for r in records]
            # Limpieza previa (opcional) e inserción
            self.department_provider.delete_all()
            self.department_provider.insert_departments(entities)
        elif table_name == TableEnum.JOBS:
            entities = [Job(**r) for r in records]
            self.job_provider.delete_all()
            self.job_provider.insert_jobs(entities)
        else:
            entities = [Employee(**r) for r in records]
            self.employee_provider.delete_all()
            self.employee_provider.insert_employees(entities)
