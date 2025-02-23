"""
job_model.py
Modelo SQLAlchemy para Job.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from data_provider.model.base import Base

class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job = Column(String, nullable=False)

    employees = relationship("EmployeeModel", back_populates="job")
