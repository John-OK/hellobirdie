# Django Project Initialization

This guide walks through initializing the Django project for HelloBirdie, following our Test-Driven Development (TDD) approach. This document corresponds to **Step 3** in the [Hybrid Backend Setup Guide](../hybrid-backend-setup-guide.md) and provides detailed steps for setting up the Django project structure.

## Prerequisites: Install PostgreSQL Client Libraries

Before setting up the virtual environment, install the PostgreSQL client libraries required by psycopg (the PostgreSQL adapter for Python):

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y gcc postgresql-client libpq-dev

# macOS (using Homebrew)
brew install postgresql libpq
# You may need to add libpq to your path:
export PATH="/usr/local/opt/libpq/bin:$PATH"

# Windows
# Install PostgreSQL from the installer which includes the required client libraries
# https://www.postgresql.org/download/windows/
```

> **Note**: These system-level dependencies are required for psycopg to compile and connect to PostgreSQL databases. Without them, pip installation of psycopg will fail.

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

> **Note**: The system dependencies (`gcc`, `postgresql-client`, and `libpq-dev`) are required for building the PostgreSQL adapter packages (`psycopg`). Without these libraries, you might encounter build errors when Docker attempts to install Python dependencies. Check with: `gcc --version`, `psql --V`, and `dpkg -s libpq-dev`. To install: `sudo apt update && sudo apt install gcc postgresql-client libpq-dev`.

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
      - DJANGO_ENV=local # Must match the environment name used in settings/__init__.py
      # Do not set DJANGO_SETTINGS_MODULE here - allow __init__.py to handle it based on DJANGO_ENV
      - IN_DOCKER=True # Helps settings determine correct database host
    env_file:
      - ./backend/.env # Load backend-specific environment variables
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

> **Note**: This configuration uses Docker Compose V2 format, which no longer requires the `version` field that was used in earlier versions. Docker Compose V2 is the current standard and simplifies the configuration syntax.
>
> **Note on Port Conflicts**: The PostgreSQL container is configured to use port 5433 on the host to avoid conflicts with any existing PostgreSQL installation (which typically uses port 5432). If you encounter the error `address already in use`, you may need to modify the port mapping further. For example, change `"5433:5432"` to `"5434:5432"` or another available port.
>
> **Updating Connection Settings**: If you change the port mapping, you'll need to update your connection settings in three places:
>
> 1. In your root `.env` file: Update `POSTGRES_PORT=5433` to match your new port
> 2. In your backend `.env` file: Update the `LOCAL_DATABASE_URL` to use the new port
> 3. For direct database access: Use `psql -h localhost -p 5433 -U postgres -d hellobirdie` (adjusting the port as needed)

## 5. Minimal Settings Structure

Before testing Docker, we need to create a minimal settings structure. This is a temporary setup that will be properly refactored in Step 5 (Settings Structure Refactoring).

### 5.1 Create Settings Package

Ensure you're in the `backend/` directory:

```bash
# Ensure you're in the backend directory
cd backend  # If you're not already there

# Create the settings package directory
mkdir -p hellobirdie/settings

# Create an empty __init__.py file to make it a proper package
touch hellobirdie/settings/__init__.py

> **Note on Python Packages**: The `__init__.py` file (even if empty) is what makes a directory a Python package. Without it, Python cannot import modules from that directory. This is a fundamental concept in Python's module system that applies to all package directories in your project.
```

### 5.2 Create Local Settings File

Create a file named `local.py` in the `backend/hellobirdie/settings/` directory with the following content:

```python
"""
Temporary local development settings for hellobirdie project.
This will be properly refactored in Step 5 (Settings Structure Refactoring).
"""

import os
import sys
import dj_database_url
from pathlib import Path

# Get the parent directory to access the main settings file
parent_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(parent_dir.parent))

# Define BASE_DIR for database path
BASE_DIR = parent_dir.parent

# Import all settings from the main settings file
from hellobirdie.settings import *

# Root URL configuration
ROOT_URLCONF = "hellobirdie.urls"

# Security settings
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY", "django-insecure-development-key-for-testing-only"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allow all hosts in local development
ALLOWED_HOSTS = ["*"]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Time zone settings
TIME_ZONE = 'UTC'
USE_TZ = True

# Add the api app to INSTALLED_APPS
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "api",
]

# Templates configuration required for admin
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Middleware configuration required for admin
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Database configuration
# Use PostgreSQL for both local development and Docker environments

# Check if we're running in a Docker environment - normalize to bool
IN_DOCKER = os.environ.get("IN_DOCKER", "").lower() == "true"

# Database URL handling logic
# 1. If in Docker, use DATABASE_URL from backend/.env
# 2. If not in Docker but LOCAL_DATABASE_URL exists, use that from backend/.env
# 3. Otherwise fallback to individual environment variables

if IN_DOCKER and os.environ.get("DATABASE_URL"):
    # Docker environment - use DATABASE_URL
    DATABASES = {"default": dj_database_url.parse(os.environ.get("DATABASE_URL"))}
elif not IN_DOCKER and os.environ.get("LOCAL_DATABASE_URL"):
    # Local environment with DATABASE_URL specified
    DATABASES = {"default": dj_database_url.parse(os.environ.get("LOCAL_DATABASE_URL"))}
else:
    # Fallback to individual PostgreSQL configuration parameters
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("LOCAL_POSTGRES_DB", "hellobirdie") if not IN_DOCKER else os.environ.get("POSTGRES_DB", "hellobirdie"),
            "USER": os.environ.get("LOCAL_POSTGRES_USER", "hellobirdie_user") if not IN_DOCKER else os.environ.get("POSTGRES_USER", "postgres"),
            "PASSWORD": os.environ.get("LOCAL_POSTGRES_PASSWORD", "hellobirdie_password") if not IN_DOCKER else os.environ.get("POSTGRES_PASSWORD", "postgres"),
            "HOST": os.environ.get("LOCAL_POSTGRES_HOST", "localhost") if not IN_DOCKER else os.environ.get("POSTGRES_HOST", "db"),
            "PORT": os.environ.get("LOCAL_POSTGRES_PORT", "5432") if not IN_DOCKER else os.environ.get("POSTGRES_PORT", "5432"),
        }
    }
```

### 5.3 Update manage.py

Now we need to update the `manage.py` file to use our new settings module. Open the `backend/manage.py` file and modify the `os.environ.setdefault` line to point to our local settings:

```python
# Find this line in manage.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hellobirdie.settings")

# Change it to:
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hellobirdie.settings.local")
```

### 5.4 PostgreSQL Setup for Local Development

This section sets up the **local development database** as explained in the dual database configuration in [Step 2, Section 4.1](./step2-environment-configuration.md#41-understanding-the-dual-database-configuration).

> **Note**: In our hybrid workflow approach, configuring the local PostgreSQL database is essential as we primarily use local development for daily work. The Docker configuration handles database setup for verification purposes only.

```bash
# Connect to PostgreSQL as a superuser
# You will be prompted to enter a password. Use the password for your account on the current machine.
sudo -u postgres psql

# Inside the PostgreSQL prompt, create the user and database
CREATE USER hellobirdie_user WITH PASSWORD 'hellobirdie_password';
CREATE DATABASE hellobirdie OWNER hellobirdie_user;

# Grant necessary privileges
GRANT ALL PRIVILEGES ON DATABASE hellobirdie TO hellobirdie_user;

# Exit PostgreSQL prompt
\q
```

> **Important**: These credentials (`hellobirdie_user`/`hellobirdie_password`) match the `LOCAL_DATABASE_URL` in your `.env` file. They are different from the Docker database credentials (`postgres`/`postgres`) which are configured in `docker-compose.yml`.
>
> If you're using a different PostgreSQL setup (e.g., different superuser name, custom installation), adjust the commands accordingly, but make sure to update your `LOCAL_DATABASE_URL` environment variable to match.

## 6. Verify Docker Setup

Now that you have the Django project structure and Docker configuration in place, let's verify the Docker setup:

> **Note**: Depending on your system configuration, you might need to use `sudo` before the Docker commands (e.g., `sudo docker compose build`). This is required if your user is not part of the Docker group. To avoid using `sudo`, you can add your user to the Docker group with: `sudo usermod -aG docker $USER` and then log out and back in.

```bash
# From project root
docker compose build
docker compose up -d
docker compose ps
```

### Expected Docker Services

After running the commands above, you should see two services running when you execute `docker compose ps`:

```
NAME                                 IMAGE                        SERVICE   STATUS
hellobirdie-backend-rebuild_2-db-1   postgres:17.4                db        Up
hellobirdie-backend-rebuild_2-1      hellobirdie-backend-rebuild  backend   Up
```

If both services are running, your Docker setup is working correctly. You can proceed to the next step.

If only the database service is running, there may be an issue with the backend service. Check the logs with:

```bash
docker compose logs backend
```

Once you've verified that both services are running correctly, stop the containers before proceeding to the next step:

```bash
docker compose down
```

### Common Docker Setup Issues

1. **Missing Dependencies**: If you see errors like `ModuleNotFoundError: No module named 'package_name'`, ensure:

   - The package is included in the appropriate requirements file
   - Core dependencies used by settings files should be in `base.txt`
   - The Dockerfile is correctly installing requirements with `RUN pip install -r requirements/docker.txt`

2. **Settings Module Not Found**: If you see `ModuleNotFoundError: No module named 'hellobirdie.settings.local'`:

   - Check that your `DJANGO_SETTINGS_MODULE` environment variable in `docker-compose.yml` matches your actual settings path
   - Verify the settings directory structure is correctly set up

3. **Database Connection Issues**: If you see database connection errors:
   - Ensure the database service is running (`docker compose ps`)
   - Check that the database environment variables in `docker-compose.yml` match your settings
   - The `depends_on` directive ensures the database starts before the backend, but doesn't guarantee it's ready to accept connections

### Docker Commands Reference

Here are some useful Docker commands for working with your environment:

```bash
# View logs of the backend service
docker compose logs backend

# Run Django management commands in the container
docker compose exec backend python manage.py [command]

# Run tests (you'll implement these in Step 4)
# Always specify the test module path to avoid import errors
docker compose exec backend python manage.py test api.tests.<test_module>

# Example: Test the health check endpoint
docker compose exec backend python manage.py test api.tests.test_health

# Stop all containers when you're done
docker compose down
```

### Troubleshooting Docker Setup

If you encounter issues with the Docker setup, here are some common problems and solutions:

1. **ALLOWED_HOSTS Error**: If you see `CommandError: You must set settings.ALLOWED_HOSTS if DEBUG is False`, check that:
   - Your `docker-compose.yml` includes the `ALLOWED_HOSTS` environment variable
   - Your `docker-compose.yml` explicitly sets `DJANGO_SETTINGS_MODULE=hellobirdie.settings.local`
   - Your `Dockerfile` sets `ENV DJANGO_ENV=development`

### Troubleshooting Local Development

Here are some common issues you might encounter during local development:

1. **PostgreSQL Connection Issues**: If you see database connection errors:

   - Ensure PostgreSQL is installed and running on your system
   - Verify that the database user and database exist
   - Check that the credentials in your `.env` file match your PostgreSQL setup
   - Make sure the PostgreSQL port is correct (default is 5432)
   - Try connecting directly with `psql -U hellobirdie_user -d hellobirdie` to test credentials

2. **Settings Import Issues**: If you see `NameError: name 'INSTALLED_APPS' is not defined` or similar errors, check that:

   - Your settings import path is correct
   - The `manage.py` file is pointing to the correct settings module
   - All required settings are defined in your settings file

3. **Missing SECRET_KEY Error**: If you see `django.core.exceptions.ImproperlyConfigured: The SECRET_KEY setting must not be empty`, make sure you've defined a SECRET_KEY in your settings file.

   - Your `docker-compose.yml` includes the `ALLOWED_HOSTS` environment variable
   - Your `docker-compose.yml` explicitly sets `DJANGO_SETTINGS_MODULE=hellobirdie.settings.local`
   - Your `Dockerfile` sets `ENV DJANGO_ENV=development`
   - Your Django settings properly read these environment variables

4. **Database Connection Issues**: If the backend can't connect to the database:

   - Ensure the database container is running (`docker compose ps`)
   - Check that port mappings are correct and not conflicting with local services
   - Verify the database connection settings in `local.py` match your Docker configuration
   - For Docker-to-Docker communication, use the service name (`db`) as the host

5. **Permission Denied Errors**: If you see permission errors with Docker commands:

   - Use `sudo` before Docker commands
   - Or add your user to the Docker group: `sudo usermod -aG docker $USER` and log out/in

6. **Django Import Errors**: If you see `ImportError: Couldn't import Django` or similar errors:
   - Check that your `requirements/docker.txt` file is properly set up and not empty
   - Ensure it includes `-r base.txt` to inherit the base requirements
   - Rebuild the Docker image with `docker compose build` after fixing the requirements

## Next Steps

After completing the Django project initialization and verifying the Docker setup, you can:

1. Proceed to [Step 4: Implementing First Feature with TDD](./step4-implementing-first-feature.md) to implement the health check endpoint following TDD principles
2. Begin implementing additional API endpoints following the same TDD process
3. Set up authentication if required

Always remember to follow the TDD cycle: RED (write failing test) → GREEN (make it pass) → REFACTOR (improve the code).
