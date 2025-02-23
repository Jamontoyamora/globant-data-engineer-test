"""
job_provider_impl.py
Implementación concreta de JobProvider usando SQLAlchemy.
"""
from typing import List
from data_provider.provider.job_provider import JobProvider
from data_provider.model.job_model import JobModel
from core.entity.job import Job
from common.configuration.database_config import SessionLocal

class JobProviderImpl(JobProvider):
    def get_all_jobs(self) -> List[Job]:
        session = SessionLocal()
        try:
            results = session.query(JobModel).all()
            return [Job(r.id, r.job) for r in results]
        finally:
            session.close()

    def insert_jobs(self, jobs: List[Job]) -> None:
        session = SessionLocal()
        try:
            for j in jobs:
                model = JobModel(id=j.id, job=j.job)
                session.merge(model)  # upsert
            session.commit()
        finally:
            session.close()

    def delete_all(self) -> None:
        session = SessionLocal()
        try:
            session.query(JobModel).delete()
            session.commit()
        finally:
            session.close()
