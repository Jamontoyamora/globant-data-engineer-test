"""
data_controller.py
Controlador para la inserción de datos (departments, jobs, employees) por lotes, validando las reglas.
"""
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Depends
from controller.dto.data_dto import BatchDataRequest, CsvUploadResponse
from controller.service.data_service import DataService
from common.configuration.dependencies import get_data_service

data_router = APIRouter()

@data_router.post("/batch", summary="Inserta datos de departments, jobs y employees en batch")
def insert_batch_data(
    request: BatchDataRequest,
    service: DataService = Depends(get_data_service)
):
    """
    Inserta datos en batch para 3 tablas: departments, jobs y employees.
    Requiere validación de campos y rechaza registros inválidos (los registra en logs).
    Permite hasta 1000 filas por tabla en la misma petición.
    """
    try:
        service.insert_data_batch(request)
        return {"detail": "Datos insertados exitosamente."}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@data_router.post("/upload-csv", response_model=CsvUploadResponse)
async def upload_csv_data(
    employees_file: UploadFile = File(...),
    departments_file: UploadFile = File(...),
    jobs_file: UploadFile = File(...),
    service: DataService = Depends(get_data_service)
):
    """
    Sube 3 archivos CSV (employees, departments, jobs) y los inserta en la DB.
    Los archivos deben venir en formato CSV (comma-separated).
    Se registran en log los registros inválidos.
    """
    try:
        invalid_count = service.insert_data_from_csv(
            employees_csv=await employees_file.read(),
            departments_csv=await departments_file.read(),
            jobs_csv=await jobs_file.read(),
        )
        return CsvUploadResponse(
            detail="Archivos procesados",
            invalid_records=invalid_count
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
