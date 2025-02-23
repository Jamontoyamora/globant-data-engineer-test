"""
app.py
Punto de entrada principal de la aplicación FastAPI.
"""

from fastapi import FastAPI
from controller.backup_controller import backup_router
from controller.data_controller import data_router
from controller.report_controller import report_router
from data_provider.model.base import create_all_tables

def create_application() -> FastAPI:
    application = FastAPI(
        title="FastAPI Microservice - Data Migration & Reporting",
        description="Prueba Técnica para migración y reporte de datos con Arquitectura Limpia.",
        version="1.0.0",
    )

    # Crear tablas (puedes usar Alembic si prefieres migraciones más formales)
    create_all_tables()

    # Incluir los routers de los controladores
    application.include_router(data_router, prefix="/data", tags=["Data Ingestion"])
    application.include_router(backup_router, prefix="/backup", tags=["Backup & Restore"])
    application.include_router(report_router, prefix="/report", tags=["Reporting"])

    return application

app = create_application()
