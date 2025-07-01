# Database Configuration and Initial Migrations

This guide provides detailed instructions for configuring the database and creating initial migrations. This corresponds to **Step 6** in the [Hybrid Backend Setup Guide](../hybrid-backend-setup-guide.md).

## 6.1 Overview

In this guide, you will:

1. Review the database configuration for different environments
2. Create and apply initial migrations
3. Verify the configuration works correctly in both local and Docker environments
4. Learn troubleshooting techniques for common database issues

## 6.2 Prerequisites

Before proceeding, ensure you have:

- PostgreSQL installed and running on your local machine
- Docker and Docker Compose installed (if using Docker environment)
- Completed the settings structure refactoring (Step 5)
- Access to a terminal with appropriate permissions

After refactoring our settings structure, we need to configure the database connections and create initial migrations. This step ensures our application can interact with the PostgreSQL database in both local and Docker environments.

## 6.3 Database Configuration Review

The database settings were already configured in the previous step as part of the settings structure refactoring. Let's review the configuration for each environment to ensure we understand how the database settings work across environments before proceeding with migrations.

During this review, check that:

- **The correct environment variables are being used**:

  - In Docker: `DATABASE_URL` or `POSTGRES_DB`, `POSTGRES_USER`, etc.
  - In local development: `LOCAL_DATABASE_URL` or `LOCAL_POSTGRES_DB`, `LOCAL_POSTGRES_USER`, etc.

- **The hybrid approach correctly handles both Docker and local development**:

  - Docker uses the `IN_DOCKER=true` environment variable to determine the context
  - Database connection uses `db` as host in Docker but `localhost` in local development

- **The test database naming strategy ensures proper isolation between environments**:
  - Test databases have `_test` suffix (e.g., `hellobirdie_test`)
  - Test databases are separate from development databases to prevent data corruption

### 6.3.1 Local Environment (local.py)

```python
# Database configuration for local development
# Using our hybrid approach with LOCAL_ prefixes for local environment variables
import os
import dj_database_url
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Check if we're running in a Docker environment - normalize to bool
IN_DOCKER = os.environ.get("IN_DOCKER", "").lower() == "true"

# Database configuration with hybrid approach
# 1. In Docker: Use DATABASE_URL
# 2. Local with URL: Use LOCAL_DATABASE_URL
# 3. Fallback: Use individual parameters

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
            "NAME": (
                os.environ.get("LOCAL_POSTGRES_DB", "hellobirdie")
                if not IN_DOCKER
                else os.environ.get("POSTGRES_DB", "hellobirdie")
            ),
            "USER": (
                os.environ.get("LOCAL_POSTGRES_USER", "hellobirdie_user")
                if not IN_DOCKER
                else os.environ.get("POSTGRES_USER", "postgres")
            ),
            "PASSWORD": (
                os.environ.get("LOCAL_POSTGRES_PASSWORD", "hellobirdie_password")
                if not IN_DOCKER
                else os.environ.get("POSTGRES_PASSWORD", "postgres")
            ),
            "HOST": (
                os.environ.get("LOCAL_POSTGRES_HOST", "localhost")
                if not IN_DOCKER
                else os.environ.get("POSTGRES_HOST", "db")
            ),
            "PORT": (
                os.environ.get("LOCAL_POSTGRES_PORT", "5432")
                if not IN_DOCKER
                else os.environ.get("POSTGRES_PORT", "5432")
            ),
        }
    }
```

### 6.3.2 Test Environment (test.py)

```python
import os
import dj_database_url
from .base import *

DEBUG = False

# Normalize IN_DOCKER to bool
IN_DOCKER = os.environ.get("IN_DOCKER", "").lower() == "true"

# Test database configuration with hybrid approach, similar to local.py
# 1. In Docker: Use DATABASE_URL with test suffix
# 2. Local with URL: Use LOCAL_DATABASE_URL with test suffix
# 3. Fallback: Use individual parameters with test database name

# Function to add test suffix to database URL
def get_test_db_url(url):
    if not url:
        return None
    # Add _test suffix to database name in the URL
    from urllib.parse import urlparse, urlunparse, parse_qs

    parsed = urlparse(url)
    path = parsed.path
    if path.startswith("/"):
        path = f"{path}_test"
    else:
        path = f"/{path}_test"

    # Reconstruct URL with modified path
    parts = list(parsed)
    parts[2] = path  # Update path component
    return urlunparse(parts)

# Prioritize URLs over individual settings
if IN_DOCKER and os.environ.get("DATABASE_URL"):
    # Create test version of Docker database
    test_db_url = get_test_db_url(os.environ.get("DATABASE_URL"))
    DATABASES = {"default": dj_database_url.parse(test_db_url)}
elif not IN_DOCKER and os.environ.get("LOCAL_DATABASE_URL"):
    # Create test version of local database
    test_db_url = get_test_db_url(os.environ.get("LOCAL_DATABASE_URL"))
    DATABASES = {"default": dj_database_url.parse(test_db_url)}
else:
    # Fallback to individual PostgreSQL configuration parameters
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": (
                os.environ.get("POSTGRES_TEST_DB", "test_hellobirdie") # Note: uses POSTGRES_TEST_DB in Docker
                if IN_DOCKER
                else os.environ.get("LOCAL_POSTGRES_DB", "hellobirdie_test") # Note: reuses LOCAL_POSTGRES_DB with _test suffix
            ),
            "USER": (
                os.environ.get("LOCAL_POSTGRES_USER", "hellobirdie_user")
                if not IN_DOCKER
                else os.environ.get("POSTGRES_USER", "postgres")
            ),
            "PASSWORD": (
                os.environ.get("LOCAL_POSTGRES_PASSWORD", "hellobirdie_password")
                if not IN_DOCKER
                else os.environ.get("POSTGRES_PASSWORD", "postgres")
            ),
            "HOST": (
                os.environ.get("LOCAL_POSTGRES_HOST", "localhost")
                if not IN_DOCKER
                else os.environ.get("POSTGRES_HOST", "db")
            ),
            "PORT": (
                os.environ.get("LOCAL_POSTGRES_PORT", "5432")
                if not IN_DOCKER
                else os.environ.get("POSTGRES_PORT", "5432")
            ),
        }
    }

# Faster password hashing for tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Disable logging during tests
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
}
```

## 6.4 Creating Initial Migrations

Now that we've reviewed the database configuration for each environment, we can proceed with creating and applying the initial migrations for our Django project.

Here's how to create and apply initial migrations:

```bash
# Create migrations for your Django apps
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Verify that migrations were applied successfully
python manage.py showmigrations
```

> **Note:** `makemigrations` is primarily a development step that creates migration files based on your model changes. These files are stored in the `migrations` directory of each app and should be committed to version control. In contrast, `migrate` is an environment setup step that applies migrations to create/update database tables and should be run in all environments (development, testing, production).

> **Note about Production:** While we focus on local and Docker development environments here, a production environment would typically use similar configuration patterns but with stricter security settings, environment-specific optimizations, and no DEBUG mode.

This will create the necessary database tables for Django's built-in apps (auth, admin, sessions, etc.) and any custom models you've defined.

## 6.5 Verifying Database Configuration

### 6.5.1 Local Environment

Let's verify that our database configuration works correctly in the local environment:

```bash
# Verify database connection by running the health check test
python manage.py test api.tests.test_health

# Start the development server
python manage.py runserver
```

Visit http://127.0.0.1:8000/api/health-check/ to verify that the API is working.

### 6.5.2 Docker Environment

Verify the Docker environment configuration:

```bash
# Verify database connection in Docker
docker compose exec backend python manage.py test api.tests.test_health

# Check the health endpoint in Docker
curl http://localhost:8001/api/health-check/
```

> **Note:** We access the API on port 8001 in the Docker environment (as configured in docker-compose.yml) to avoid conflicts with the local Django server running on port 8000. This allows both environments to run simultaneously.

## 6.6 Additional Testing Information

For running other tests in your project, use these patterns:

```bash
# Local environment with specific test module
python manage.py test api.tests.<test_module>

# Local environment with test settings
DJANGO_ENV=test python manage.py test api.tests.<test_module>

# Docker environment with specific test module
docker compose exec backend python manage.py test api.tests.<test_module>

# Docker environment with test settings
docker compose exec backend bash -c "DJANGO_ENV=test python manage.py test api.tests.<test_module>"

# Stop Docker containers when done
docker compose down
```

## 6.7 Troubleshooting Common Issues

### Understanding Common Error Messages

- **"FATAL: database 'hellobirdie' does not exist"**: The specified database hasn't been created yet. Use the `createdb` command shown below.
- **"FATAL: role 'postgres' does not exist"**: The specified database user doesn't exist. Create it with `createuser`.
- **"FATAL: password authentication failed for user 'postgres'"**: The password in your settings doesn't match the one in PostgreSQL.
- **"could not connect to server: Connection refused"**: PostgreSQL server isn't running or is using a different port.
- **"django.db.utils.OperationalError: FATAL: database 'hellobirdie' is being accessed by other users"**: Other connections are preventing operations. Check for other sessions using the database.

### Connection Refused

If you see a "connection refused" error, check:

1. Is PostgreSQL running?
2. Are the connection parameters (host, port, username, password) correct?
3. Does the database exist?

```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Create the database if it doesn't exist
sudo -u postgres createdb hellobirdie
```

### Permission Denied

If you see a "permission denied" error, check:

1. Does the user have the necessary permissions?
2. Is the password correct?

```bash
# Create a user with the necessary permissions
sudo -u postgres createuser --interactive
```

### Docker-specific Issues

If you encounter issues with Docker:

1. Check if the containers are running:

   ```bash
   docker compose ps
   ```

2. Check the logs:

   ```bash
   docker compose logs
   ```

3. Ensure the environment variables are correctly set in the Docker Compose file.

## 6.8 Next Steps

After successfully configuring the database and creating initial migrations, you can proceed to implement the core features of the HelloBirdie application following the same TDD principles.
