# Database Configuration and Initial Migrations

This guide provides detailed instructions for configuring the database and creating initial migrations. This corresponds to **Step 6** in the [Hybrid Backend Setup Guide](../hybrid-backend-setup-guide.md).

## Overview

After refactoring our settings structure, we need to configure the database connections and create initial migrations. This step ensures our application can interact with the PostgreSQL database in both local and Docker environments.

## Database Configuration

The database settings were already configured in the previous step as part of the settings structure refactoring. Let's review the configuration for each environment:

### Local Environment (local.py)

```python
# Database configuration for local development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'hellobirdie'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}
```

### Test Environment (test.py)

```python
# Database configuration for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'test_hellobirdie'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}
```

## Creating Initial Migrations

Now that we have configured our database settings, we need to create and apply initial migrations:

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
