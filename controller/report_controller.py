"""
report_controller.py
Controlador que maneja endpoints de reporting.
"""

from fastapi import APIRouter, Query, Depends
from typing import List
from controller.dto.report_dto import HiredByQuarterResponse, DepartmentAboveMeanResponse
from controller.service.report_service import ReportService
from common.configuration.dependencies import get_report_service

report_router = APIRouter()

@report_router.get("/hired-by-quarter", response_model=List[HiredByQuarterResponse])
def hired_by_quarter(
    year: int = Query(..., description="Año para filtrar (ej: 2021)"),
    service: ReportService = Depends(get_report_service)
):
    """
    Retorna el número de empleados contratados para cada job y departamento
    durante un año dado, dividido por trimestre.
    Ordenado alfabéticamente por department y job.
    """
    result = service.get_hired_by_quarter(year)
    return result

@report_router.get("/departments-above-mean", response_model=List[DepartmentAboveMeanResponse])
def departments_above_mean(
    year: int = Query(..., description="Año para filtrar (ej: 2021)"),
    service: ReportService = Depends(get_report_service)
):
    """
    Lista los departamentos (id, nombre y número de contrataciones) que superan
    la media de empleados contratados en un año dado, ordenado descendentemente
    por número de contrataciones.
    """
    result = service.get_departments_above_mean(year)
    return result
