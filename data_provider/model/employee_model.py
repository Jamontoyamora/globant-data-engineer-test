"""
employee_model.py
Modelo de empleado para SQLAlchemy.
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from data_provider.model.base import Base

class EmployeeModel(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    datetime = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'))
    job_id = Column(Integer, ForeignKey('jobs.id'))

    department = relationship("DepartmentModel", back_populates="employees")
    job = relationship("JobModel", back_populates="employees")
