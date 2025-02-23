"""
backup_service.py
Interfaz del servicio de backup.
"""
from abc import ABC, abstractmethod

class BackupService(ABC):
    @abstractmethod
    def create_backup(self, table_name: str) -> (bytes, str):
        """
        Genera un archivo AVRO (en bytes) para la tabla indicada.
        Retorna (avro_bytes, filename).
        """

    @abstractmethod
    def restore_backup(self, table_name: str, avro_bytes: bytes):
        """
        Restaura la tabla indicada desde los bytes de un archivo AVRO.
        """
