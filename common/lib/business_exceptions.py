"""
business_exceptions.py
Excepciones de negocio personalizadas.
"""

class BusinessValidationError(Exception):
    """
    Se lanza cuando una validación de negocio o de datos no se cumple.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class DataNotInsertedError(Exception):
    """
    Se lanza cuando un conjunto de datos no puede insertarse (por validaciones fallidas, etc.).
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
