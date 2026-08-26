# Hybrid Development Workflow Guide

This document outlines the recommended workflow for HelloBirdie development using the hybrid approach: local-first for daily development with Docker for verification.

## Core Principles

- **Local Development First**: Use your local environment for daily development tasks
- **Docker for Verification**: Use Docker to verify your code works in a production-like environment before committing
- **Consistent Test Practices**: Use pytest as the primary test runner in both environments

## Local Development Workflow

### Setup (One-Time)

```bash
# Activate your virtual environment
source .venv/bin/activate  # On Linux/Mac

# Install dependencies
pip install -r backend/requirements/local.txt
```

### Daily Development

```bash
# Always make sure your virtual environment is activated
source .venv/bin/activate  # On Linux/Mac

# Run the Django development server
cd backend
python manage.py runserver

# Run all tests with pytest (uses test settings automatically via conftest.py)
python -m pytest

# Run a specific test file
python -m pytest api/tests/test_health.py

# Quick run against local settings (bypasses test settings)
python manage.py test api.tests.<test_module>

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create a new app
python manage.py startapp <app_name>
```

## Docker Verification Workflow

Use Docker in these scenarios:

- Before committing major changes
- When testing database interactions
- For final verification of features
- When simulating production environment

```bash
# Start all services
docker compose up -d

# Run all tests in Docker (uses test settings automatically via conftest.py)
docker compose exec backend pytest

# Run a specific test file in Docker
docker compose exec backend pytest api/tests/test_health.py

# Quick run against local settings in Docker
docker compose exec backend python manage.py test api.tests.<test_module>

# Run migrations in Docker
docker compose exec backend python manage.py migrate

# Stop all services when done
docker compose down
```

## Git Workflow Integration

1. Develop and test features locally
2. Verify with Docker before committing
3. Create a feature branch and commit changes
4. Push branch and create a pull request

## Switching Between Environments

### From Local to Docker

When moving from local development to Docker verification:

1. Ensure you've committed all changes to Git or stashed them
2. Start Docker services: `docker compose up -d`
3. Run the same tests in Docker to verify

### From Docker to Local

When moving from Docker back to local development:

1. Stop Docker services: `docker compose down`
2. Activate your virtual environment: `source .venv/bin/activate`
3. Continue development

## Common Issues and Solutions

### Database Migration Conflicts

If you encounter migration conflicts between environments:

1. In Docker: `docker compose exec backend python manage.py showmigrations`
2. Locally: `python manage.py showmigrations`
3. Compare the outputs and resolve any discrepancies

### Package Version Differences

If you add packages locally:

1. Update the appropriate requirements file
2. Rebuild Docker image: `docker compose build`

## Best Practices

1. **Keep Environments in Sync**: Regularly synchronize your local and Docker environments
2. **Run Tests in Both Environments**: Especially for database-related changes
3. **Use Docker for Final Verification**: Always verify in Docker before pushing changes
4. **Be Consistent with Commands**: Use the same commands in both environments, changing only the prefix
