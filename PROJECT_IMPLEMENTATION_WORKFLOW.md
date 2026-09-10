# Shipment API: Current Implementation and Workflow

## Current implementation

This project is a small FastAPI application that exposes a user CRUD example.
The runtime database is selected with `DATABASE_URL`. When it is set, Neon
PostgreSQL is used through Psycopg 3; otherwise SQLite remains the local
fallback in `user.db`.

The project dependencies are managed by `uv` and declared in `pyproject.toml`.
SQLAlchemy provides database access, Pydantic validates request and response
data, and Scalar provides interactive API documentation.

## Application startup workflow

1. FastAPI creates the application object.
2. `database.py` reads `DATABASE_URL` and creates the database engine.
3. `models.py` registers the `User` table with SQLAlchemy metadata.
4. `main.py` creates the `users` table if it does not already exist.
5. FastAPI registers the route handlers.
6. Uvicorn starts serving the application.

Run against Neon PostgreSQL from the project root:

```bash
export DATABASE_URL='postgresql://USERNAME:PASSWORD@HOST/DATABASE?sslmode=require&channel_binding=require'
uv run uvicorn shipment_api.main:app --reload
```

The `export` command sets `DATABASE_URL` for the current terminal session.
`database.py` reads this variable with `os.getenv("DATABASE_URL")`. When it is
present, the application connects to Neon PostgreSQL; when it is absent, the
application uses the SQLite fallback.

The `uv run uvicorn shipment_api.main:app --reload` command uses the project's
managed environment, starts Uvicorn as the ASGI server, loads the `app` object
from `shipment_api.main`, and automatically restarts the server when Python
files change.

Together, these commands configure PostgreSQL for the terminal session and
start the FastAPI application using that database.

Do not commit the real Neon URL because it contains database credentials.
`database.py` automatically changes `postgresql://` to
`postgresql+psycopg://` so SQLAlchemy selects Psycopg 3.

## Request workflow

Each database-backed request follows this flow:

1. FastAPI validates path, query, and JSON body values.
2. `Depends(get_db)` creates a SQLAlchemy session.
3. The endpoint queries or changes the `users` table.
4. The endpoint returns an ORM object or a list of ORM objects.
5. Pydantic serializes the result using `UserResponse`.
6. The dependency closes the database session.

## Available endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/` | Confirms that the API is running |
| `POST` | `/users` | Creates a user |
| `GET` | `/users/{user_id}` | Retrieves one user |
| `GET` | `/users?skip=0&limit=10` | Lists users with pagination |
| `GET` | `/scalar` | Opens Scalar API documentation |

## Database model

The `users` table currently contains:

- `id`: integer primary key
- `name`: required string
- `email`: required and unique string

## Switching databases

`psycopg[binary]` is already declared for PostgreSQL support. Set
`DATABASE_URL` to the supplied Neon connection string to use PostgreSQL.
If `DATABASE_URL` is absent, the preserved SQLite fallback is used.

The existing sessions, models, schemas, and routers work with both databases.
For production, use environment configuration and Alembic migrations rather
than hard-coded credentials and `create_all`.
