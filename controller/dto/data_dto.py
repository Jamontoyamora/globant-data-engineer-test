from pydantic import BaseModel, Field
from typing import List

class DepartmentInput(BaseModel):
    id: int = Field(..., gt=0, description="ID del departamento")
    department: str = Field(..., min_length=1, max_length=100, description="Nombre del departamento")

class JobInput(BaseModel):
    id: int = Field(..., gt=0, description="ID del trabajo")
    job: str = Field(..., min_length=1, max_length=100, description="Nombre del trabajo")

class EmployeeInput(BaseModel):
    id: int = Field(..., gt=0, description="ID del empleado")
    name: str = Field(..., min_length=1, max_length=100, description="Nombre del empleado")
    # Mejor usar datetime en vez de str, p.ej. "2021-07-27T16:02:08Z"
    datetime: str = Field(..., description="Fecha y hora en formato ISO")
    department_id: int = Field(..., gt=0, description="ID del departamento")
    job_id: int = Field(..., gt=0, description="ID del trabajo")

class BatchDataRequest(BaseModel):
    departments: List[DepartmentInput] = Field(default_factory=list, max_items=1000)
    jobs: List[JobInput] = Field(default_factory=list, max_items=1000)
    employees: List[EmployeeInput] = Field(default_factory=list, max_items=1000)

class CsvUploadResponse(BaseModel):
    detail: str = Field(..., description="Detalle de la respuesta")
    invalid_records: int = Field(..., description="Número de registros inválidos")
