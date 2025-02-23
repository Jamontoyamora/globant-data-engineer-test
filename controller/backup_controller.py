"""
backup_controller.py
Controlador que maneja endpoints para generación y restauración de backups en AVRO.
"""

from fastapi import APIRouter, UploadFile, HTTPException, status, Response, Depends
from controller.service.backup_service import BackupService
from common.configuration.dependencies import get_backup_service

backup_router = APIRouter()

@backup_router.get("/download")
async def download_backup(
    table: str,
    service: BackupService = Depends(get_backup_service)
):
    """
    Genera un backup en AVRO para la tabla indicada y retorna el archivo.
    table: "departments", "jobs" o "employees"
    """
    try:
        avro_bytes, filename = service.create_backup(table)
        return Response(
            content=avro_bytes,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment;filename={filename}"}
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@backup_router.post("/restore")
async def restore_backup(
    table: str,
    file: UploadFile,
    service: BackupService = Depends(get_backup_service)
):
    """
    Restaura los datos de la tabla indicada a partir de un archivo AVRO subido.
    """
    if file.content_type not in ["application/octet-stream", "application/x-avro-binary"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo debe ser de tipo AVRO (application/octet-stream)."
        )
    try:
        contents = await file.read()
        service.restore_backup(table, contents)
        return {"detail": f"Restauración exitosa para la tabla {table}."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
