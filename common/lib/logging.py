"""
logging.py
Ejemplo de configuración de logging global.
Puedes reemplazar con loguru, structlog, etc.
"""
import logging

# Configuración básica
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger("fastapi_microservice")
