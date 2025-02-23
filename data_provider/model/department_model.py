"""
department_model.py
Modelo de departamento para SQLAlchemy.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from data_provider.model.base import Base

class DepartmentModel(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, index=True)
    department = Column(String, nullable=False)

    employees = relationship("EmployeeModel", back_populates="department")
