# Shipment API

FastAPI shipment service organized by feature.

## Current structure

```text
src/shipment_api/
├── core/
│   └── database.py
├── features/
│   └── users/
│       ├── model.py
│       ├── repository.py
│       ├── router.py
│       ├── schema.py
│       └── service.py
├── main.py
└── __init__.py
```

## Production-readiness roadmap

The project is currently suitable for development and learning. Before deploying
to production, implement and verify the following items.

### 1. Security and access control

- Add authentication (for example, OAuth2/JWT).
- Add authorization and role/permission checks.
- Hash passwords with a proven password-hashing library.
- Validate and sanitize all user-controlled input.
- Configure CORS explicitly for trusted origins.
- Add rate limiting and request-size limits.
- Keep secrets in environment variables or a secret manager; never commit them.
- Review dependencies for known vulnerabilities.

### 2. Database reliability

- Use Alembic migrations instead of `Base.metadata.create_all()` in the app.
- Configure production connection pooling and pool health checks.
- Add indexes and constraints based on real query patterns.
- Add transaction rollback handling for failed writes.
- Define backup, restore, and disaster-recovery procedures.
- Use separate databases/configuration for development, testing, and production.

### 3. API correctness

- Define a versioned API such as `/api/v1`.
- Add consistent error-response formats and exception handlers.
- Enforce safe pagination limits and validate `skip`/`limit`.
- Add request correlation IDs and idempotency where needed.
- Define OpenAPI documentation, compatibility, and deprecation policies.

### 4. Testing and quality

- Add unit tests for services and repositories.
- Add API integration tests using an isolated test database.
- Add migration tests and tests for validation, conflicts, and not-found cases.
- Add coverage thresholds and run formatting, linting, and type checking.
- Add contract or end-to-end tests for important workflows.

### 5. Observability and operations

- Use structured, JSON-compatible logs.
- Add health and readiness endpoints that check required dependencies.
- Add metrics for latency, errors, throughput, and database connections.
- Add distributed tracing if the service calls other services.
- Configure alerting, dashboards, and log retention.
- Ensure sensitive values are never written to logs.

### 6. Deployment and resilience

- Add a production ASGI server/process configuration.
- Containerize the service and define resource limits.
- Add CI/CD with automated checks, migrations, and deployment approval.
- Provide environment-specific configuration and a documented rollback plan.
- Add timeouts, retries, graceful shutdown, and dependency failure handling.
- Run load, stress, and security testing before launch.

### 7. Documentation and maintenance

- Document setup, environment variables, migrations, and deployment.
- Document API usage and authentication flows.
- Define ownership, support contacts, and incident procedures.
- Pin and regularly update dependencies.
- Track each roadmap item as a task before calling the project production-ready.

## Definition of done for production

Do not consider the service production-ready until the roadmap items have been
implemented, tested in a production-like environment, reviewed, and documented.