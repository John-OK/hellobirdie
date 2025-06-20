# Database Configuration and Initial Migrations

This guide provides detailed instructions for configuring the database and creating initial migrations. This corresponds to **Step 6** in the [Hybrid Backend Setup Guide](../hybrid-backend-setup-guide.md).

## Overview

After refactoring our settings structure, we need to configure the database connections and create initial migrations. This step ensures our application can interact with the PostgreSQL database in both local and Docker environments.

## Database Configuration

The database settings were already configured in the previous step as part of the settings structure refactoring. Let's review the configuration for each environment:

### Local Environment (local.py)

```python
# Database configuration for local development
# Using our hybrid approach with LOCAL_ prefixes for local environment variables

# Check if we're running in a Docker environment - normalize to bool
IN_DOCKER = os.environ.get("IN_DOCKER", "").lower() == "true"

# Database URL handling logic
if IN_DOCKER and os.environ.get("DATABASE_URL"):
    # Docker environment - use DATABASE_URL from backend/.env
    DATABASES = {"default": dj_database_url.parse(os.environ.get("DATABASE_URL"))}
elif not IN_DOCKER and os.environ.get("LOCAL_DATABASE_URL"):
    # Local environment with DATABASE_URL specified in backend/.env
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

### Test Environment (test.py)

```python
# Database configuration for testing
# Using test suffix for the database name

# Check if we're running in a Docker environment
IN_DOCKER = os.environ.get('IN_DOCKER', '').lower() == 'true'

# Function to add test suffix to database URL
def get_test_db_url(url):
    if not url:
        return None
    # Add _test suffix to database name in the URL
    from urllib.parse import urlparse, urlunparse
    parsed = urlparse(url)
    path = parsed.path
    if path.startswith('/'):
        path = f"{path}_test"
    else:
        path = f"/{path}_test"

    # Reconstruct URL with modified path
    parts = list(parsed)
    parts[2] = path  # Update path component
    return urlunparse(parts)

# Prioritize URLs over individual settings
if IN_DOCKER and os.environ.get('DATABASE_URL'):
    # Create test version of Docker database
    test_db_url = get_test_db_url(os.environ.get('DATABASE_URL'))
    DATABASES = {'default': dj_database_url.parse(test_db_url)}
elif not IN_DOCKER and os.environ.get('LOCAL_DATABASE_URL'):
    # Create test version of local database
    test_db_url = get_test_db_url(os.environ.get('LOCAL_DATABASE_URL'))
    DATABASES = {'default': dj_database_url.parse(test_db_url)}
else:
    # Fallback to individual PostgreSQL configuration parameters
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_TEST_DB', 'test_hellobirdie') if IN_DOCKER else os.environ.get('LOCAL_POSTGRES_DB', 'hellobirdie_test'),
            'USER': os.environ.get('LOCAL_POSTGRES_USER', 'hellobirdie_user') if not IN_DOCKER else os.environ.get('POSTGRES_USER', 'postgres'),
            'PASSWORD': os.environ.get('LOCAL_POSTGRES_PASSWORD', 'hellobirdie_password') if not IN_DOCKER else os.environ.get('POSTGRES_PASSWORD', 'postgres'),
            'HOST': os.environ.get('LOCAL_POSTGRES_HOST', 'localhost') if not IN_DOCKER else os.environ.get('POSTGRES_HOST', 'db'),
            'PORT': os.environ.get('LOCAL_POSTGRES_PORT', '5432') if not IN_DOCKER else os.environ.get('POSTGRES_PORT', '5432'),
        }
    }
```

## Creating Initial Migrations

Now that our database configuration is aligned with the dual `.env` strategy developed in steps 2-5, we need to create and apply initial migrations:

```bash
# Make sure you're in the backend directory
cd backend

# Create initial migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

This will create the necessary database tables for Django's built-in apps (auth, admin, sessions, etc.) and any custom models you've defined.

## Testing in Local Environment

Let's verify that our database configuration works correctly in the local environment:

```bash
# Run tests
# Always specify the test module path to avoid import errors
python manage.py test api.tests.<test_module>

# To use test-specific settings
DJANGO_ENV=test python manage.py test api.tests.<test_module>

# Example: Test the health check endpoint
python manage.py test api.tests.test_health

# Start the development server
python manage.py runserver
```

Visit http://127.0.0.1:8000/api/health-check/ to verify that the API is working.

## Testing in Docker Environment

Now let's verify that our database configuration works correctly in the Docker environment:

```bash
# Start Docker containers
docker compose up -d

# Run migrations in Docker
docker compose exec backend python manage.py migrate

# Run tests in Docker
# Always specify the test module path to avoid import errors
docker compose exec backend python manage.py test api.tests.<test_module>

# To use test-specific settings in Docker
docker compose exec backend bash -c "DJANGO_ENV=test python manage.py test api.tests.<test_module>"

# Example: Test the health check endpoint
docker compose exec backend python manage.py test api.tests.test_health

# Stop Docker containers
docker compose down
```

## Troubleshooting Common Issues

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

## Next Steps

After successfully configuring the database and creating initial migrations, you can proceed to implement the core features of the HelloBirdie application following the same TDD principles.
