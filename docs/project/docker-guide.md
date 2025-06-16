# Docker Guide for HelloBirdie

This guide explains how Docker is used in HelloBirdie and provides a detailed look at our containerization strategy.

## What is Docker?

Docker is a platform that packages applications and their dependencies into isolated containers. Think of a container as a lightweight, standalone package that includes everything needed to run a piece of software:

- Code
- Runtime environment
- System tools
- System libraries
- Settings

## Required Versions

You'll need either:

1. Docker Desktop (recommended for development):
   - Version: 4.38.0
   - Includes Docker Engine and Docker Compose
   - Provides GUI and better development experience

OR

2. Standalone Installation:
   - Docker Engine 28.0.0
   - Docker Compose 2.33.0

Additional Requirements:

- Node.js 22.14.0 (LTS)

> Note: Version numbers are explicit to ensure consistent behavior across development environments. These versions provide features we rely on, such as BuildKit and enhanced compose file syntax.

## Docker's Role in the HelloBirdie Hybrid Workflow

Help establish a hybrid development workflow, where:

1. **Local Development (Primary)**

   - Day-to-day development happens in a local Python virtual environment
   - Faster iteration and simplified debugging
   - Direct access to Django commands

2. **Docker Verification (Secondary)**
   - Verifies changes work in a standardized environment before commits
   - Ensures code runs consistently across different machines
   - Simulates production-like conditions for integration testing

> Note: While previously HelloBirdie used a Docker-first approach, we've transitioned to a hybrid model to improve development speed and learning outcomes.

3. **Isolated Components**
   - Backend, database, and frontend run independently
   - Easy to update or replace individual parts
   - Problems in one container don't affect others

## Container Architecture

### Primary Development Environment (Local)

```text
┌─────────────────┐     ┌─────────────────┐
│    Frontend     │     │     Backend     │
│   (Local Dev)   │────▶│   (Local Dev)   │
│  localhost:5173 │     │  localhost:8000 │
└─────────────────┘     └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │    Database     │
                        │ (Local Postgres)│
                        │  localhost:5432 │
                        └─────────────────┘
```

> Note: Both frontend and backend run locally during daily development for the best developer experience with hot reloading, fast feedback cycles, and straightforward debugging.

### Docker Verification Environment (Secondary)

```text
┌─────────────────┐     ┌─────────────────┐
│    Frontend     │     │     Backend     │
│   (Local Dev)   │────▶│    Container    │
│  localhost:5173 │     │  localhost:8000 │
└─────────────────┘     └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │    Database     │
                        │    Container    │
                        │  localhost:5433 │
                        └─────────────────┘
```

> Note: Backend and database run in Docker containers for verification before commits, while frontend remains local for all development. The Docker PostgreSQL instance runs on port 5433 to avoid conflicts with local PostgreSQL.

### Production Environment

```text
┌─────────────────┐     ┌─────────────────┐
│    Frontend     │     │     Backend     │
│    Container    │────▶│    Container    │
│   (Nginx/Node)  │     │     (Django)    │
└─────────────────┘     └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │    Database     │
                        │    Container    │
                        │   (PostgreSQL)  │
                        └─────────────────┘
```

## Key Files and Their Purposes

### 1. Docker Compose Configuration

```yaml
# Docker Compose V2 configuration
services:
  backend:
    build: ./backend
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    environment:
      - DJANGO_ENV=development
      - DJANGO_SETTINGS_MODULE=hellobirdie.settings.local
      - ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
      - DATABASE_URL=postgres://postgres:postgres@db:5432/hellobirdie
      - IN_DOCKER=True
      - TZ=UTC
    depends_on:
      - db

  db:
    image: postgres:17.4
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=hellobirdie
      - TZ=UTC
    ports:
      - "5433:5432" # Using port 5433 on host to avoid conflicts with local PostgreSQL

volumes:
  postgres_data:
```

> Note: Port 5433 is used on the host to avoid conflicts with your local PostgreSQL installation.

### 2. Backend Dockerfile

```dockerfile
FROM python:3.13.1-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_ENV=development

# Set work directory
WORKDIR /app

# Install system dependencies including PostgreSQL client libraries
RUN apt-get update && apt-get install -y \
  gcc \
  postgresql-client \
  libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements /app/requirements
RUN pip install --no-cache-dir -r requirements/docker.txt

# Copy project
COPY . /app/

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "hellobirdie.wsgi:application"]
```

> Note: While the Docker container is configured to use gunicorn, the docker-compose configuration overrides this command to use Django's runserver for development.

## Common Docker Commands

### Starting the Environment

```bash
# Build and start all containers
docker compose up --build -d

# View container logs
docker compose logs -f

# Stop all containers
docker compose down
```

> **Note:** For Docker Compose V1 (older versions), use `docker-compose` instead of `docker compose`. The project requires Docker Compose 2.33.0 or newer, which uses the V2 syntax without the hyphen.

### Working with Containers

```bash
# Run Django management commands
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser

# Access PostgreSQL
docker compose exec db psql -U user -d hellobirdie

# View container status
docker compose ps
```

### Development Workflow

```bash
# Start backend services
docker compose up -d

# Start frontend development server (locally)
cd frontend
npm run dev

# Run backend tests
# Always specify the test module path to avoid import errors
docker compose exec backend python manage.py test api.tests.<test_module>

# Examples:
# Test a specific module
docker compose exec backend python manage.py test api.tests.test_health

# Test a specific test class
docker compose exec backend python manage.py test api.tests.test_health:HealthCheckTestCase

# Test a specific test method
docker compose exec backend python manage.py test api.tests.test_health:HealthCheckTestCase.test_health_check_returns_ok_status

# Format backend code
docker compose exec backend black .
```

## Data Persistence

Docker uses volumes to persist data:

- `postgres_data`: Stores database files
- Backend code directory is mounted as a volume for live development

## Environment Variables

We use `.env` files for configuration:

```plaintext
# Development (.env)
COMPOSE_PROJECT_NAME=hellobirdie
DATABASE_URL=postgresql://user:password@db:5432/hellobirdie
DJANGO_SETTINGS_MODULE=hellobirdie.settings.local
DEBUG=True
```

## Common Issues and Solutions

### 1. Port Conflicts

If you see "port is already allocated" errors:

```bash
# Check what's using the port
sudo lsof -i :8000  # For backend port
sudo lsof -i :5432  # For database port

# Stop the conflicting process or change the port in Docker Compose configuration
```

### 2. Database Connection Issues

If the backend can't connect to the database:

```bash
# Ensure database container is running
docker compose ps

# Check database logs
docker compose logs db

# Verify environment variables
docker compose exec backend env | grep DATABASE
```

### 3. Volume Permission Issues

If you encounter permission errors:

```bash
# Fix ownership of mounted volumes
sudo chown -R $USER:$USER .

# Or run Docker commands with sudo
sudo docker compose up
```

## Best Practices

1. **Always use docker compose up -d**

   - Starts containers in detached mode
   - Keeps your terminal free for other commands

2. **Check logs when troubleshooting**

   - Use `docker compose logs -f [service]`
   - Helps identify issues quickly

3. **Clean up regularly**

   - Remove unused containers: `docker compose down`
   - Clean volumes when needed: `docker compose down -v`

4. **Use volume mounts for development**
   - Enables live code changes
   - Preserves development experience

## Next Steps

1. Review the [Development Environment Setup](development-environment.md) guide
2. Explore the [Backend Setup Guide](../hybrid-backend-setup-guide.md)
3. Set up your local environment following these guides

## Additional Resources

- [Official Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
- [Python Docker Image](https://hub.docker.com/_/python)
