"""
data_service_impl.py
Implementación del servicio para inserción de datos (batch y CSV).
"""

import csv
import io
from typing import List
from controller.service.data_service import DataService
from controller.dto.data_dto import BatchDataRequest
from core.use_case.data_use_case import DataUseCase


class DataServiceImpl(DataService):
    def __init__(self, use_case: DataUseCase):
        self.use_case = use_case

    def insert_data_batch(self, request: BatchDataRequest) -> None:
        """
        Valida e inserta datos en batch.
        """
        # Transformar DTOs a entidades
        # Departments
        departments = []
        for dept in request.departments:
            departments.append({"id": dept.id, "department": dept.department})

        # Jobs
        jobs = []
        for job in request.jobs:
            jobs.append({"id": job.id, "job": job.job})

        # Employees
        employees = []
        for emp in request.employees:
            employees.append(
                {
                    "id": emp.id,
                    "name": emp.name,
                    "datetime": emp.datetime,
                    "department_id": emp.department_id,
                    "job_id": emp.job_id,
                }
            )

        self.use_case.insert_data(departments, jobs, employees)

    def insert_data_from_csv(
        self, employees_csv: bytes, departments_csv: bytes, jobs_csv: bytes
    ) -> int:
        """
        Lee 3 CSV, valida e inserta sus datos. Retorna la cantidad de registros inválidos.
        """
        # Decodificar los bytes y parsear CSV
        invalid_count = 0

        employees_list = self._parse_csv(
            employees_csv, ["id", "name", "datetime", "department_id", "job_id"]
        )
        departments_list = self._parse_csv(departments_csv, ["id", "department"])
        jobs_list = self._parse_csv(jobs_csv, ["id", "job"])

        # Llamar al caso de uso
        invalid_count += self.use_case.insert_data(
            departments_list, jobs_list, employees_list
        )

        return invalid_count

    def _parse_csv(self, file_bytes: bytes, expected_headers: List[str]) -> List[dict]:
        """
        Parsea el contenido CSV (en bytes) y retorna una lista de diccionarios
        con tipos de datos apropiados (ejemplo: id -> int).
        """
        text = file_bytes.decode("utf-8")
        reader = csv.DictReader(io.StringIO(text), fieldnames=expected_headers)
        rows = []

        # Mapear nombres de campo a funciones de conversión
        # Si un campo no aparece aquí, quedará como string por defecto
        conversions = {
            "id": int,
            "department_id": int,
            "job_id": int,
            # Puedes añadir más si lo deseas, p.ej.:
            # "some_float_field": float
        }

        for idx, row in enumerate(reader):
            # Quitar espacios en blanco
            clean_row = {k: v.strip() if v else v for k, v in row.items()}

            # Aplicar conversiones
            for field, convert_func in conversions.items():
                # Si el campo existe y no está vacío, conviértelo
                if field in clean_row and clean_row[field] not in (None, ""):
                    try:
                        clean_row[field] = convert_func(clean_row[field])
                    except ValueError:
                        # Manejar error si no se puede convertir
                        # Podrías registrar un log o dejarlo como None
                        clean_row[field] = None

            rows.append(clean_row)

        # Regresar la lista con los tipos adecuados
        return rows
