"""
backup_dto.py
DTOs relacionados con la operación de backup/restore si se requirieran.
Aquí solo un ejemplo de Query param.
"""
from pydantic import BaseModel

class BackupTableQuery(BaseModel):
    table: str
