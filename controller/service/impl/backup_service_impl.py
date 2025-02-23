"""
backup_service_impl.py
Implementación del servicio de backup y restore en AVRO.
Usa un bloque 'with' para evitar el error "I/O operation on closed file".
"""

import io
import avro.schema
from avro.datafile import DataFileWriter, DataFileReader
from avro.io import DatumWriter, DatumReader
from datetime import datetime

from controller.service.backup_service import BackupService
from core.use_case.backup_use_case import BackupUseCase
from common.utils.enums.table_enums import TableEnum


class BackupServiceImpl(BackupService):
    def __init__(self, use_case: BackupUseCase):
        self.use_case = use_case

    def create_backup(self, table_name: str) -> (bytes, str):
        """
        Genera un archivo AVRO desde la tabla y lo retorna en bytes.
        """
        # Validar la tabla
        if table_name not in [
            TableEnum.DEPARTMENTS,
            TableEnum.JOBS,
            TableEnum.EMPLOYEES,
        ]:
            raise ValueError(f"Tabla '{table_name}' no soportada.")

        # Obtener datos de dominio (lista de entidades)
        entities = self.use_case.get_data_for_backup(table_name)

        # Construir el esquema Avro según la tabla
        if table_name == TableEnum.DEPARTMENTS:
            schema = avro.schema.parse(
                """
            {
              "type": "record",
              "name": "Department",
              "fields": [
                {"name": "id", "type": "int"},
                {"name": "department", "type": "string"}
              ]
            }
            """
            )
        elif table_name == TableEnum.JOBS:
            schema = avro.schema.parse(
                """
            {
              "type": "record",
              "name": "Job",
              "fields": [
                {"name": "id", "type": "int"},
                {"name": "job", "type": "string"}
              ]
            }
            """
            )
        else:  # EMPLOYEES
            schema = avro.schema.parse(
                """
            {
              "type": "record",
              "name": "Employee",
              "fields": [
                {"name": "id", "type": "int"},
                {"name": "name", "type": "string"},
                {"name": "datetime", "type": "string"},
                {"name": "department_id", "type": "int"},
                {"name": "job_id", "type": "int"}
              ]
            }
            """
            )

        # Preparar un stream en memoria
        bytes_writer = io.BytesIO()
        datum_writer = DatumWriter(schema)

        # Usar with para que el writer se cierre automáticamente
        with DataFileWriter(bytes_writer, datum_writer, schema) as avro_writer:
            for entity in entities:
                data_dict = entity.to_dict()
                avro_writer.append(data_dict)
            # Extraer los bytes Avro generados
            avro_bytes = bytes_writer.getvalue()

        filename = (
            f"{table_name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.avro"
        )

        # Retornar (contenido en bytes, nombre sugerido de archivo)
        return avro_bytes, filename

    def restore_backup(self, table_name: str, avro_bytes: bytes):
        """
        Restaura la tabla desde los bytes de un archivo AVRO.
        """
        # Validar la tabla
        if table_name not in [
            TableEnum.DEPARTMENTS,
            TableEnum.JOBS,
            TableEnum.EMPLOYEES,
        ]:
            raise ValueError(f"Tabla '{table_name}' no soportada.")

        # Usar with para que el reader se cierre automáticamente
        with io.BytesIO(avro_bytes) as bytes_reader:
            with DataFileReader(bytes_reader, DatumReader()) as avro_reader:
                # Leer todos los registros
                records = [record for record in avro_reader]

        # Llamar al use case con la lista de registros
        self.use_case.restore_data_from_backup(table_name, records)
