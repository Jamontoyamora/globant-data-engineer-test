# FastAPI Microservice - Data Migration & Reporting

Este proyecto es un microservicio desarrollado con FastAPI para la migración y reporte de datos. Utiliza una arquitectura limpia y se conecta a una base de datos PostgreSQL.

## Requisitos

- Docker
- Docker Compose

## Configuración

Asegúrate de tener Docker y Docker Compose instalados en tu máquina.

## Levantar el Proyecto

1. Clona el repositorio:

    ```sh
    git clone https://github.com/Jamontoyamora/globant-data-engineer-test
    cd globant-data-engineer-test
    ```

2. Construye y levanta los servicios con Docker Compose:

    ```sh
    docker-compose up --build
    ```

    Esto levantará dos servicios:
    - `db`: Un contenedor con PostgreSQL.
    - `web`: Un contenedor con la aplicación FastAPI.

3. Accede a la aplicación:

    La aplicación estará disponible en `http://localhost:8000`.

## Endpoints

La aplicación expone los siguientes endpoints:

- **Data Ingestion**
  - `POST /data/batch`: Inserta datos en batch para [departments](http://_vscodecontentref_/0), [jobs](http://_vscodecontentref_/1) y [employees](http://_vscodecontentref_/2).
    ```sh
    curl --location 'http://localhost:8000/data/batch' \
    --header 'Content-Type: application/json' \
    --data '{
      "departments": [
        { "id": 1, "department": "Supply Chain" },
        { "id": 2, "department": "Maintenance" }
      ],
      "jobs": [
        { "id": 1, "job": "Recruiter" },
        { "id": 2, "job": "Manager" }
      ],
      "employees": [
        { "id": 4535, "name": "Marcelo Gonzalez", "datetime": "2021-07-27T16:02:08Z", "department_id": 1, "job_id": 2 },
        { "id": 4572, "name": "Lida Guerrero", "datetime": "2021-07-27T19:04:09Z", "department_id": 1, "job_id": 2 }
      ]
    }'
    ```
  - `POST /data/upload-csv`: Sube archivos CSV para [employees](http://_vscodecontentref_/3), [departments](http://_vscodecontentref_/4) y [jobs](http://_vscodecontentref_/5) e inserta los datos en la base de datos.
    ```sh
    curl --location 'http://localhost:8000/data/upload-csv' \
    --form 'employees_file=@"/path/to/hired_employees.csv"' \
    --form 'departments_file=@"/path/to/departments.csv"' \
    --form 'jobs_file=@"/path/to/jobs.csv"'
    ```

- **Backup & Restore**
  - `GET /backup/download`: Genera un backup en AVRO para la tabla indicada y retorna el archivo.
    ```sh
    curl --location 'http://localhost:8000/backup/download?table=employees'
    curl --location 'http://localhost:8000/backup/download?table=jobs'
    curl --location 'http://localhost:8000/backup/download?table=departments'
    ```
  - `POST /backup/restore`: Restaura los datos de la tabla indicada a partir de un archivo AVRO subido.
    ```sh
    curl --location 'http://localhost:8000/backup/restore?table=employees' \
    --form 'file=@"/path/to/employees_backup.avro"'
    curl --location 'http://localhost:8000/backup/restore?table=jobs' \
    --form 'file=@"/path/to/jobs_backup.avro"'
    curl --location 'http://localhost:8000/backup/restore?table=departments' \
    --form 'file=@"/path/to/departments_backup.avro"'
    ```

- **Reporting**
  - `GET /report/hired-by-quarter`: Retorna el número de empleados contratados por trimestre para un año dado.
    ```sh
    curl --location 'http://localhost:8000/report/hired-by-quarter?year=2021'
    ```
  - `GET /report/departments-above-mean`: Lista los departamentos que superan la media de empleados contratados en un año dado.

## Variables de Entorno

Las siguientes variables de entorno pueden ser configuradas en el archivo [docker-compose.yml](http://_vscodecontentref_/6):

- [POSTGRES_USER](http://_vscodecontentref_/7): Usuario de PostgreSQL (por defecto: `postgres`)
- [POSTGRES_PASSWORD](http://_vscodecontentref_/8): Contraseña de PostgreSQL (por defecto: `postgres`)
- [POSTGRES_DB](http://_vscodecontentref_/9): Nombre de la base de datos (por defecto: `my_fastapi_db`)
- [POSTGRES_HOST](http://_vscodecontentref_/10): Host de PostgreSQL (por defecto: `db`)
- [POSTGRES_PORT](http://_vscodecontentref_/11): Puerto de PostgreSQL (por defecto: `5432`)

## Notas

- Puedes modificar el archivo [docker-compose.yml](http://_vscodecontentref_/12) para cambiar la configuración de los servicios.
- Asegúrate de que los puertos `5432` y `8000` estén disponibles en tu máquina.

## Documentación

Puedes acceder a la documentación interactiva de la API en los siguientes enlaces:
- [Swagger](http://localhost:8000/docs)
- [ReDoc](http://localhost:8000/redoc)

## Licencia

Este proyecto está licenciado bajo la Licencia MIT.