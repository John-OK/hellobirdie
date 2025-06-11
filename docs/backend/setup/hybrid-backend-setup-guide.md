# Hybrid Backend Setup Guide

## Purpose of This Guide

This document serves multiple purposes:

1. **For New Team Members**: If you're joining the project, you likely won't need to follow this entire guide. Instead, you should:

   - Clone the existing repository
   - Follow the [Development Environment Setup](../../project/development-environment.md) guide
   - Review this document to understand how the backend was structured and why

2. **For Reference**: This guide documents how the HelloBirdie backend was initially built and structured using a hybrid approach (local development with Docker testing).

3. **For Rebuilding**: If you need to recreate the backend from scratch or understand its architecture in depth, follow the step-by-step process outlined below.

4. **For Learning**: This guide demonstrates Test-Driven Development (TDD) principles applied to a Django project.

## Related Documentation

### Step-by-Step Detailed Guides

- [Step 1: Project Foundation](./details/step1-project-structure-setup.md) - Setting up the initial project structure
- [Step 2: Environment Configuration](./details/step2-environment-configuration.md) - Configuring requirements and Docker
- [Step 3: Django Project Initialization](./details/step3-django-project-initialization.md) - Initializing the Django project
- [Step 4: Implementing First Feature with TDD](./details/step4-implementing-first-feature.md) - Implementing the health check endpoint
- [Step 5: Settings Structure Refactoring](./details/step5-settings-structure-refactoring.md) - Implementing split settings approach
- [Step 6: Database Configuration](./details/step6-database-configuration.md) - Setting up the database and initial migrations

### Additional Resources

- [TDD Testing Strategy](./tdd-testing-strategy.md) - Details our TDD approach and testing practices
- [Feature Setup Guide](./guides/feature-setup-guide.md) - Process for implementing new features following TDD

### Project-Wide Resources

- [Development Environment](../../project/development-environment.md) - Detailed setup for development tools and environment
- [Docker Guide](../../project/docker-guide.md) - Comprehensive Docker usage and configuration

## Setup Process Overview

### 1. Project Foundation

Follow the [Step 1: Project Foundation](./details/step1-project-structure-setup.md) guide to:

- Create backend directory structure within existing project
- Update .gitignore with Python and Django-specific patterns
- Update project README.md with backend setup instructions
- Commit Point: "Backend project structure setup"
  > Why: Establishes backend foundation within existing project

### 2. Environment Configuration

Follow the [Step 2: Environment Configuration](./details/step2-environment-configuration.md) guide to:

- Create requirements files (base.txt, local.txt, test.txt, docker.txt)
- Create sample environment variables file
- Commit Point: "Backend environment configuration"
  > Why: Complete environment setup before adding application code

### 3. Django Project Initialization

Follow the [Step 3: Django Project Initialization](./details/step3-django-project-initialization.md) guide to:

- Set up virtual environment
- Install dependencies
- Create Django project structure
- Create API app with tests directory
- Set up Docker configuration
  - Create Dockerfile for the backend
  - Configure Docker Compose with PostgreSQL
  - Create minimal settings structure for Docker
- Verify Docker setup
- Commit Point: "Django project structure and Docker configuration"
  > Why: Establishes the core Django project structure and containerization

### 4. Implementing First Feature with TDD

Implement a health check endpoint following TDD principles. For detailed implementation steps, refer to the [Step 4: Implementing First Feature with TDD](./details/step4-implementing-first-feature.md) guide.

#### RED Phase

- Write a test for the health check endpoint before implementing it in `backend/api/tests/test_health.py`
- Run the test and verify it fails (expected at this stage):
  ```bash
  python manage.py test api.tests.test_health
  ```

#### GREEN Phase

- Implement minimal code to make the test pass in `backend/api/views.py`
- Configure URL routing in `backend/api/urls.py` and `backend/hellobirdie/urls.py`
- Run the test again to verify it passes:

  ```bash
  python manage.py test api.tests.test_health
  ```

- Commit Point: "Health check endpoint implementation"
  > Why: Completes first feature using TDD workflow

### 5. Settings Structure Refactoring (REFACTOR Phase)

Follow the [Step 5: Settings Structure Refactoring](./details/step5-settings-structure-refactoring.md) guide to properly refactor the minimal settings structure created in Step 2:

- Expand the settings directory structure
  ```
  hellobirdie/
  └── settings/
      ├── __init__.py  # Settings loader (already created in Step 2)
      ├── base.py      # Common settings
      ├── local.py     # Development settings (enhance the minimal version from Step 2)
      └── test.py      # Test-specific settings
  ```
- Move settings from the default settings.py to appropriate files
- Setup environment variables in `.env` file:
  ```
  DJANGO_ENV=local
  DJANGO_SECRET_KEY=your-secret-key-here
  ```
- Run tests to ensure refactoring didn't break functionality:
  ```bash
  python manage.py test api.tests.test_health
  DJANGO_ENV=test python manage.py test api.tests.test_health
  ```
- Commit Point: "Django settings structure refactoring"
  > Why: Improves project organization while maintaining functionality

### 6. Database Configuration and Initial Migrations

Follow the [Step 6: Database Configuration](./details/step6-database-configuration.md) guide to configure the database and create initial migrations:

- Configure database settings in the appropriate settings files
- Create and apply initial migrations
- Test in both local and Docker environments
- Commit Point: "Database configuration and migrations"
  > Why: Completes the basic project setup with working database

## Feature Setup Guide

### 1. API Structure Setup

- Create API app
- Configure DRF
- Setup API test structure
- Create base test classes
- Commit Point: "API foundation setup"
  > Why: Framework for feature development

### 2. Authentication Setup

- Write authentication tests
- Implement authentication
- Configure JWT
- Commit Point: "Authentication implementation"
  > Why: Core security feature complete

### 3. Bird Data Models

- Write model tests
- Create bird-related models
- Setup model validation
- Commit Point: "Bird data models"
  > Why: Core data structure defined

### 4. API Endpoints

- Write endpoint tests
- Implement CRUD endpoints
- Add validation
- Configure serializers
- Commit Point: "API endpoints implementation"
  > Why: Core functionality complete

### 5. Integration Tests

- Write integration tests
- Setup test data fixtures
- Configure API documentation
- Commit Point: "Integration tests and documentation"
  > Why: Ensures system works as a whole

## Development Workflow

### Local Development (Primary)

```bash
# Activate virtual environment
source .venv/bin/activate

# Run Django development server
cd backend
python manage.py runserver

# Run tests
# Always specify the test module path to avoid import errors
python manage.py test api.tests.<test_module>

# Example: Test the health check endpoint
python manage.py test api.tests.test_health
# or with pytest
pytest

# Run tests with coverage
pytest --cov=api
```

### Docker Testing (Secondary)

```bash
# Start services
docker compose up -d

# Run Django tests
# Always specify the test module path to avoid import errors
docker compose exec backend python manage.py test api.tests.<test_module>

# Example: Test the health check endpoint
docker compose exec backend python manage.py test api.tests.test_health

# Run pytest tests
docker compose exec backend pytest

# Run with coverage
docker compose exec backend pytest --cov=api

# Shut down containers
docker compose down

> **Note:** For Docker Compose V1 (older versions), use `docker-compose` instead of `docker compose`. The project requires Docker Compose 2.33.0 or newer, which uses the V2 syntax without the hyphen.
```

## Troubleshooting

### Common Issues

1. **Import Errors After Settings Refactoring**

   - Check that your `BASE_DIR` is correctly defined in `base.py`
   - Verify that `__init__.py` is properly loading the correct settings file

2. **Test Database Issues**

   - Ensure test settings are using the correct PostgreSQL test database
   - Check that the test database exists and is accessible
   - Verify that migrations are applied before running tests

3. **Environment Variable Problems**
   - Verify `.env` file is properly loaded
   - Check that `DJANGO_ENV` is set correctly for the environment you're targeting
