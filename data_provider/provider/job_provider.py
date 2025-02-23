"""
job_provider.py
Interfaz para acceso a la tabla jobs.
"""
from abc import ABC, abstractmethod
from typing import List
from core.entity.job import Job

class JobProvider(ABC):
    @abstractmethod
    def get_all_jobs(self) -> List[Job]:
        pass

    @abstractmethod
    def insert_jobs(self, jobs: List[Job]) -> None:
        pass

    @abstractmethod
    def delete_all(self) -> None:
        pass
