"""
report_dto.py
DTOs para las respuestas de los endpoints de reporte.
"""
from pydantic import BaseModel
from typing import Optional

class HiredByQuarterResponse(BaseModel):
    department: str
    job: str
    Q1: int
    Q2: int
    Q3: int
    Q4: int

class DepartmentAboveMeanResponse(BaseModel):
    id: int
    department: str
    hired: int
