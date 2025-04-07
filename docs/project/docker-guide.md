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

## Why HelloBirdie Uses Docker

We use Docker to ensure:

1. **Consistent Environments**

   - Every developer works with identical setups
   - Development matches production environment
   - No "it works on my machine" problems

2. **Easy Setup**

   - New developers need only Docker installed
   - One command to start the entire backend stack
   - Automated dependency management

3. **Isolated Components**
   - Backend, database, and frontend run independently
   - Easy to update or replace individual parts
   - Problems in one container don't affect others

## Container Architecture

### Development Environment

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
                        │  localhost:5432 │
                        └─────────────────┘
```

> Note: Frontend runs locally during development for the best developer experience with hot reloading and fast feedback cycles. It is only containerized for production deployment.

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
version: "3.8"

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/hellobirdie

  db:
    image: postgres:17
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=hellobirdie
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password

volumes:
  postgres_data:
```

### 2. Backend Dockerfile

```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

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
docker compose exec backend pytest

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
