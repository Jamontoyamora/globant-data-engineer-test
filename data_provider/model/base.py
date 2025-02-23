"""
base.py
Declarative Base para SQLAlchemy.
"""
from sqlalchemy.ext.declarative import declarative_base
from common.configuration.database_config import engine

Base = declarative_base()

def create_all_tables():
    # Importar los modelos para que se registren en el metadata de Base
    from data_provider.model.department_model import DepartmentModel
    from data_provider.model.job_model import JobModel
    from data_provider.model.employee_model import EmployeeModel
    Base.metadata.create_all(bind=engine)
