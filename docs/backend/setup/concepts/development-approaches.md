# Development Approaches: Local vs. Docker

## Hybrid Development Approach

For the HelloBirdie project, we're using a hybrid development approach that combines:

1. Local development and testing with virtual environments (primary workflow)
2. Docker-based verification before commits and deployment (secondary workflow)

## Local Development (Primary)

### Benefits for Learning

- **Direct Interaction**: Immediate feedback when working with Django commands and code
- **Simplified Debugging**: Easier to trace issues without container abstraction
- **Faster Iterations**: Quicker reload times and development cycles
- **Focus on Django**: Learn Django concepts without Docker complexity

### Setup

```bash
# Create a virtual environment
python -m venv .venv

# Activate it
source .venv/bin/activate  # On Linux/Mac
# or
.venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r backend/requirements/local.txt

# Run Django commands directly
cd backend
python manage.py runserver
```

## Docker Environment (Secondary - Verification)

### Benefits

- **Production Similarity**: Environment matches production more closely
- **Dependency Isolation**: Avoids "works on my machine" problems
- **Service Integration**: Easy to add services like PostgreSQL
- **Team Consistency**: Everyone has the same environment

### When to Use Docker

- For final verification before committing changes
- When integration testing across multiple services
- When simulating production environment
- For CI/CD pipeline consistency

### Docker Commands

```bash
# Start all services
docker compose up

# Run a command in the container
# Run tests with specific module path to avoid import errors
docker compose exec backend python manage.py test api.tests.<test_module>

# Example: Test the health check endpoint
docker compose exec backend python manage.py test api.tests.test_health

# Rebuild after dependency changes
docker compose build
```

> **Note:** For Docker Compose V1 (older versions), use `docker-compose` instead of `docker compose`. The project requires Docker Compose 2.33.0 or newer, which uses the V2 syntax without the hyphen.

## TDD Workflow in Hybrid Environment

1. Write tests in local environment
2. Run tests locally using `python manage.py test api.tests.<test_module>`
3. Implement features locally
4. Run tests locally again for rapid feedback cycles
5. Verify in Docker before committing:
   ```bash
   docker compose up -d
   docker compose exec backend python manage.py test api.tests.<test_module>
   ```
6. Create pull request with all tests passing in both environments
7. CI/CD pipeline runs tests in Docker

## Recommended IDE Extensions

- Python extension with virtual environment support
- Docker extension for container management
- Database client for connecting to PostgreSQL
