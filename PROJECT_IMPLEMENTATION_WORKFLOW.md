# Shipment API: Current Implementation and Workflow

## Current implementation

This project is a small FastAPI application that exposes a user CRUD example.
The current runtime database is SQLite, stored in `user.db`.

The project dependencies are managed by `uv` and declared in
`pyproject.toml`. SQLAlchemy provides database access, Pydantic validates
request and response data, and Scalar provides interactive API documentation.

## Application startup workflow

1. FastAPI creates the application object.
2. SQLAlchemy creates an engine for `sqlite:///user.db`.
3. A session factory and declarative model base are configured.
4. The `users` table is created if it does not already exist.
5. FastAPI registers the route handlers.
6. Uvicorn starts serving the application.

Run the application from the project root:

```bash
uv run uvicorn shipment_api.main:app --reload
```

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

The generated OpenAPI specification is also available at `/docs` and
`/openapi.json` through FastAPI's default documentation routes.

## Database model

The `users` table currently contains:

- `id`: integer primary key
- `name`: required string
- `email`: required and unique string

## Production considerations

This is a development-friendly implementation. Before production use, the
project should move the database URL to environment configuration, use Alembic
migrations instead of `create_all`, add update/delete operations, validate
pagination bounds, and add transaction/error handling for duplicate emails.

Although `psycopg[binary]` is already declared for PostgreSQL support, the
current code does not use PostgreSQL because its engine URL is SQLite. To use
the installed Psycopg 3 driver later, the URL must use the
`postgresql+psycopg://` dialect.
