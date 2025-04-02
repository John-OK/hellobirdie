# Development Approaches: Local vs. Docker

## Hybrid Development Approach

For the HelloBirdie project, we're using a hybrid development approach that combines:

1. Local development with virtual environments
2. Docker-based testing and deployment

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

## Docker Environment (Secondary)

### Benefits

- **Production Similarity**: Environment matches production more closely
- **Dependency Isolation**: Avoids "works on my machine" problems
- **Service Integration**: Easy to add services like PostgreSQL
- **Team Consistency**: Everyone has the same environment

### When to Use Docker

- Before committing major changes
- When testing database interactions
- For final verification of features
- When simulating production environment

### Docker Commands

```bash
# Start all services
docker-compose up

# Run a command in the container
docker-compose exec backend python manage.py test

# Rebuild after dependency changes
docker-compose build
```

## TDD Workflow in Hybrid Environment

1. Write tests in local environment
2. Implement features locally
3. Run tests locally for quick feedback
4. Verify in Docker before committing
5. CI/CD pipeline runs tests in Docker

## Recommended IDE Extensions

- Python extension with virtual environment support
- Docker extension for container management
- Database client for connecting to PostgreSQL
