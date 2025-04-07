# Django Project Initialization

This guide walks through initializing the Django project for HelloBirdie, following our Test-Driven Development (TDD) approach. This document corresponds to **Step 3** in the [Hybrid Backend Setup Guide](../hybrid-backend-setup-guide.md) and provides detailed steps for setting up the Django project structure.

## 1. Set Up Virtual Environment

Start by creating and activating a virtual environment for local development:

```bash
# Create virtual environment in project root
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Linux/Mac
# or
.venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r backend/requirements/local.txt
```

## 2. Create Django Project

Set up the basic Django project structure:

```bash
# Navigate to backend directory
cd backend

# Create Django project
python -m django startproject hellobirdie .
```

> **Note**: Using `python -m django` instead of `django-admin` ensures you're using the Django version installed in your virtual environment rather than a system-wide installation.

## 3. Create API App

While still in the `backend/` directory, create the API app where we'll implement our endpoints:

```bash
# Ensure you're in the backend directory
cd backend  # If you're not already there

# Create the API app
python manage.py startapp api

# Create tests directory structure
mkdir -p api/tests
touch api/tests/__init__.py
```

## 4. Docker Configuration

Now that we have the Django project structure in place, let's set up Docker for containerized development and testing.

### Dockerfile

Create a file named `Dockerfile` in the `backend/` directory with the following content:

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

> **Note**: The system dependencies (`gcc`, `postgresql-client`, and `libpq-dev`) are required for building the `psycopg2` package, which is the PostgreSQL adapter for Python. Without these libraries, you might encounter build errors when Docker attempts to install Python dependencies.

### docker-compose.yml

Create a file named `docker-compose.yml` in the project root directory with the following content:

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
    ports:
      - "5433:5432" # Using port 5433 on host to avoid conflicts with local PostgreSQL

volumes:
  postgres_data:
```

> **Note**: This configuration uses Docker Compose V2 format, which no longer requires the `version` field that was used in earlier versions. Docker Compose V2 is the current standard and simplifies the configuration syntax.
>
> **Note on Port Conflicts**: The PostgreSQL container is configured to use port 5433 on the host to avoid conflicts with any existing PostgreSQL installation (which typically uses port 5432). If you encounter the error `address already in use`, you may need to modify the port mapping further. For example, change `"5433:5432"` to `"5434:5432"` or another available port.
>
> **Updating Connection Settings**: If you change the port mapping, you'll need to update your connection settings in three places:
>
> 1. In your `.env` file: Update `POSTGRES_PORT=5433` to match your new port
> 2. In `local.py`: Update the default port in `os.environ.get("POSTGRES_PORT", "5433")` to match your new port
> 3. For direct database access: Use `psql -h localhost -p 5433 -U postgres -d hellobirdie` (adjusting the port as needed)

## 5. Minimal Settings Structure

Before testing Docker, we need to create a minimal settings structure. This is a temporary setup that will be properly refactored in Step 5 (Settings Structure Refactoring).

Ensure you're in the `backend/` directory:

```bash
# Ensure you're in the backend directory
cd backend  # If you're not already there

# Create the settings package directory
mkdir -p hellobirdie/settings

# Create an empty __init__.py file to make it a proper package
touch hellobirdie/settings/__init__.py
```

Create a file named `local.py` in the `backend/hellobirdie/settings/` directory with the following content:

```python
"""
Temporary local development settings for hellobirdie project.
This will be properly refactored in Step 5 (Settings Structure Refactoring).
"""

from hellobirdie.settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allow all hosts in local development
ALLOWED_HOSTS = ["*"]

# Database
import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "hellobirdie"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.environ.get(
            "POSTGRES_HOST", "db"
        ),  # Use 'db' for Docker communication, 'localhost' for direct access
        "PORT": os.environ.get(
            "POSTGRES_PORT", "5433"
        ),  # Match the host port we mapped in docker-compose.yml
    }
}
```

## 6. Verify Docker Setup

Now that you have the Django project structure and Docker configuration in place, you can verify the Docker setup:

```bash
# From project root
docker compose build
docker compose up -d
docker compose ps  # Should show both services running
docker compose logs backend  # Check for any errors
```

> **Note**: Depending on your system configuration, you might need to use `sudo` before the Docker commands (e.g., `sudo docker compose build`). This is required if your user is not part of the Docker group. To avoid using `sudo`, you can add your user to the Docker group with: `sudo usermod -aG docker $USER` and then log out and back in.

To run tests in the Docker environment (once you've written tests in Step 4):

```bash
docker compose exec backend python manage.py test
```

When you're done, stop the Docker containers:

```bash
docker compose down
```

### Troubleshooting Docker Setup

If you encounter issues with the Docker setup, here are some common problems and solutions:

1. **ALLOWED_HOSTS Error**: If you see `CommandError: You must set settings.ALLOWED_HOSTS if DEBUG is False`, check that:

   - Your `docker-compose.yml` includes the `ALLOWED_HOSTS` environment variable
   - Your `docker-compose.yml` explicitly sets `DJANGO_SETTINGS_MODULE=hellobirdie.settings.local`
   - Your `Dockerfile` sets `ENV DJANGO_ENV=development`
   - Your Django settings properly read these environment variables

2. **Database Connection Issues**: If the backend can't connect to the database:

   - Ensure the database container is running (`docker compose ps`)
   - Check that port mappings are correct and not conflicting with local services
   - Verify the database connection settings in `local.py` match your Docker configuration
   - For Docker-to-Docker communication, use the service name (`db`) as the host

3. **Permission Denied Errors**: If you see permission errors with Docker commands:

   - Use `sudo` before Docker commands
   - Or add your user to the Docker group: `sudo usermod -aG docker $USER` and log out/in

4. **Django Import Errors**: If you see `ImportError: Couldn't import Django` or similar errors:
   - Check that your `requirements/docker.txt` file is properly set up and not empty
   - Ensure it includes `-r base.txt` to inherit the base requirements
   - Rebuild the Docker image with `docker compose build` after fixing the requirements

## Next Steps

After completing the Django project initialization and verifying the Docker setup, you can:

1. Proceed to [Step 4: Implementing First Feature with TDD](./step4-implementing-first-feature.md) to implement the health check endpoint following TDD principles
2. Begin implementing additional API endpoints following the same TDD process
3. Set up authentication if required

Always remember to follow the TDD cycle: RED (write failing test) → GREEN (make it pass) → REFACTOR (improve the code).
