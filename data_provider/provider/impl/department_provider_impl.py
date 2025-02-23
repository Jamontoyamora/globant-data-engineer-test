"""
department_provider_impl.py
Implementación concreta de DepartmentProvider usando SQLAlchemy.
"""
from typing import List
from data_provider.provider.department_provider import DepartmentProvider
from data_provider.model.department_model import DepartmentModel
from core.entity.department import Department
from common.configuration.database_config import SessionLocal

class DepartmentProviderImpl(DepartmentProvider):
    def get_all_departments(self) -> List[Department]:
        session = SessionLocal()
        try:
            results = session.query(DepartmentModel).all()
            return [Department(r.id, r.department) for r in results]
        finally:
            session.close()

    def insert_departments(self, departments: List[Department]) -> None:
        session = SessionLocal()
        try:
            for d in departments:
                model = DepartmentModel(id=d.id, department=d.department)
                session.merge(model)  # merge -> upsert
            session.commit()
        finally:
            session.close()

    def delete_all(self) -> None:
        session = SessionLocal()
        try:
            session.query(DepartmentModel).delete()
            session.commit()
        finally:
            session.close()
