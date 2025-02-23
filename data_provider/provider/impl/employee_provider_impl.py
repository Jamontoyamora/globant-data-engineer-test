"""
employee_provider_impl.py
Implementación concreta de EmployeeProvider usando SQLAlchemy.
"""
from typing import List
from data_provider.provider.employee_provider import EmployeeProvider
from data_provider.model.employee_model import EmployeeModel
from core.entity.employee import Employee
from common.configuration.database_config import SessionLocal

class EmployeeProviderImpl(EmployeeProvider):
    def get_all_employees(self) -> List[Employee]:
        session = SessionLocal()
        try:
            results = session.query(EmployeeModel).all()
            return [
                Employee(r.id, r.name, r.datetime, r.department_id, r.job_id)
                for r in results
            ]
        finally:
            session.close()

    def insert_employees(self, employees: List[Employee]) -> None:
        session = SessionLocal()
        try:
            for e in employees:
                model = EmployeeModel(
                    id=e.id,
                    name=e.name,
                    datetime=e.datetime,
                    department_id=e.department_id,
                    job_id=e.job_id
                )
                session.merge(model)  # upsert
            session.commit()
        finally:
            session.close()

    def delete_all(self) -> None:
        session = SessionLocal()
        try:
            session.query(EmployeeModel).delete()
            session.commit()
        finally:
            session.close()
