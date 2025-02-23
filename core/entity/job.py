"""
job.py
Entidad pura de dominio para Job.
"""

class Job:
    def __init__(self, id: int, job: str):
        self.id = id
        self.job = job

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "job": self.job
        }
