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

> **Note**: The system dependencies (`gcc`, `postgresql-client`, and `libpq-dev`) are required for building the PostgreSQL adapter packages (`psycopg`). Without these libraries, you might encounter build errors when Docker attempts to install Python dependencies.

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

### 5.1 Create Settings Package

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
ROOT_URLCONF = 'hellobirdie.urls'

# Security settings
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-development-key-for-testing-only')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allow all hosts in local development
ALLOWED_HOSTS = ["*"]

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
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Middleware configuration required for admin
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Database configuration
# Use PostgreSQL for both local development and Docker environments

# Check if we're running in a Docker environment
IN_DOCKER = os.environ.get('IN_DOCKER', False)

# Try to use LOCAL_DATABASE_URL if available
local_db_url = os.environ.get("LOCAL_DATABASE_URL")
if local_db_url:
    DATABASES = {
        "default": dj_database_url.parse(local_db_url)
    }
else:
    # Standard PostgreSQL configuration
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB", "hellobirdie"),
            "USER": os.environ.get("POSTGRES_USER", "hellobirdie_user"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "hellobirdie_password"),
            "HOST": os.environ.get("POSTGRES_HOST", "localhost" if not IN_DOCKER else "db"),
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
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

### 5.4 Set Up PostgreSQL Database and User

Before proceeding, we need to create the PostgreSQL database and user that our application will use:

```bash
# Connect to PostgreSQL as a superuser
sudo -u postgres psql

# Inside the PostgreSQL prompt, create the user and database
CREATE USER hellobirdie_user WITH PASSWORD 'hellobirdie_password';
CREATE DATABASE hellobirdie OWNER hellobirdie_user;

# Grant necessary privileges
GRANT ALL PRIVILEGES ON DATABASE hellobirdie TO hellobirdie_user;

# Exit PostgreSQL prompt
\q
```

> **Note**: If you're using a different PostgreSQL setup (e.g., different superuser name, custom installation), adjust the commands accordingly. The important part is creating a database named `hellobirdie` and a user named `hellobirdie_user` with the password `hellobirdie_password`.

### 5.5 Install Required Dependencies

We need to install a few additional dependencies for our settings configuration:

```bash
# Make sure your virtual environment is activated
pip install dj-database-url python-dotenv

# Add these to requirements/local.txt
echo "dj-database-url==2.3.0" >> requirements/local.txt
echo "python-dotenv==1.0.0" >> requirements/local.txt
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
