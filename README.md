# API de Monitoreo de Incendios Forestales (BME280)

Base de datos PostgreSQL en Neon + API REST en FastAPI con arquitectura de 5 capas
(Config, Database, Schemas/Models, Repositories, Routers).

## 1. Base de datos (Neon)

1. Entra a https://neon.tech e inicia sesión.
2. Crea un proyecto nuevo.
3. Abre el **SQL Editor** y ejecuta, en este orden:
   - `sql/01_schema.sql` (crea las 12 tablas)
   - `sql/02_seed_data.sql` (inserta los registros de ejemplo)
4. Ve a la sección de conexión (Connection Details) y copia:
   - Host
   - Database
   - User
   - Password
   - Port

## 2. Configurar el entorno local

```bash
python -m venv myvenv
myvenv\Scripts\activate   # Windows
# source myvenv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```

Copia `.env.example` a `.env` y reemplaza los valores con tus credenciales reales de Neon:

```
DB_HOST=...
DB_NAME=...
DB_USER=...
DB_PASSWORD=...
DB_PORT=5432
```

## 3. Ejecutar la API

```bash
uvicorn main:app --reload
```

Abre `http://127.0.0.1:8000/docs` para ver y probar todos los endpoints CRUD (Swagger UI).

## 4. Estructura del proyecto

```
proyecto_incendios/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
├── sql/
│   ├── 01_schema.sql
│   └── 02_seed_data.sql
└── app/
    ├── core/
    │   └── database.py
    ├── models/          (12 modelos Pydantic)
    ├── repositories/    (12 repositorios con SQL puro)
    └── api/             (12 routers con CRUD)
```

## 5. Entidades disponibles

zonas_forestales, estaciones_monitoreo, sensores, tipos_medicion, mediciones,
niveles_riesgo, umbrales_alerta, alertas, brigadas, personal_brigada,
incidentes, mantenimientos_sensor.

Cada una tiene rutas GET (listar/por id), POST, PUT y DELETE en `/docs`.
