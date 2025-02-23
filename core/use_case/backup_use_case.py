"""
abstract_backup_use_case.py
Clase abstracta para el caso de uso de backup.
"""
from abc import ABC, abstractmethod

class BackupUseCase(ABC):
    @abstractmethod
    def get_data_for_backup(self, table_name: str):
        pass

    @abstractmethod
    def restore_data_from_backup(self, table_name: str, records: list):
        pass
