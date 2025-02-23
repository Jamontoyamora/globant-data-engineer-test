"""
data_service.py
Interfaz de servicio para la inserción de datos.
"""
from abc import ABC, abstractmethod
from controller.dto.data_dto import BatchDataRequest

class DataService(ABC):
    @abstractmethod
    def insert_data_batch(self, request: BatchDataRequest) -> None:
        pass

    @abstractmethod
    def insert_data_from_csv(self, employees_csv: bytes, departments_csv: bytes, jobs_csv: bytes) -> int:
        """
        Procesa el contenido de 3 CSV y los inserta en la base de datos.
        Retorna la cantidad de registros inválidos.
        """
