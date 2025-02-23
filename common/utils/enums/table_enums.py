"""
table_enums.py
Enumeración para identificar tablas para backup/restore.
"""
from enum import Enum

class TableEnum(str, Enum):
    DEPARTMENTS = "departments"
    JOBS = "jobs"
    EMPLOYEES = "employees"
