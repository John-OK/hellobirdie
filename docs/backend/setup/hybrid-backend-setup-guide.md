# Hybrid Backend Setup Guide

This guide outlines the process for setting up and extending the HelloBirdie backend using a hybrid approach (local development with Docker testing), following Test-Driven Development (TDD) principles.

## Related Documentation

- [Project Structure Setup](./details/project-structure-setup.md) - Setting up the initial project structure
- [Environment Configuration](./details/environment-configuration.md) - Configuring requirements and Docker
- [Django Project Initialization](./details/django-project-initialization.md) - Initializing the Django project
- [Django Settings Structure](./details/django-settings-structure.md) - Implementing split settings approach
- [TDD Testing Strategy](./tdd-testing-strategy.md) - Details our TDD approach and testing practices

## Setup Process Overview

### 1. Project Foundation

Follow the [Project Structure Setup](./details/project-structure-setup.md) guide to:

- Create backend directory structure within existing project
- Update .gitignore with Python and Django-specific patterns
- Update project README.md with backend setup instructions
- Commit Point: "Backend project structure setup"
  > Why: Establishes backend foundation within existing project

### 2. Environment Configuration

Follow the [Environment Configuration](./details/environment-configuration.md) guide to:

- Create requirements files (base.txt, local.txt, test.txt, docker.txt)
- Set up Dockerfile for the backend
- Configure docker-compose.yml with PostgreSQL
- Create sample environment variables file
- Commit Point: "Backend environment configuration"
  > Why: Complete environment setup before adding application code

### 3. Django Project Initialization

Follow the [Django Project Initialization](./details/django-project-initialization.md) guide to:

- Set up virtual environment
- Install dependencies
- Create Django project structure
- Create API app with tests directory
- Commit Point: "Django project structure initialization"
  > Why: Establishes the core Django project structure

### 4. Implementing First Feature with TDD

Implement a health check endpoint following TDD principles:

#### RED Phase

- Write a test for the health check endpoint before implementing it:

  ```python
  # backend/api/tests/test_health.py
  from django.test import TestCase
  from django.urls import reverse

  class HealthCheckTestCase(TestCase):
      def test_health_check_returns_ok_status(self):
          response = self.client.get(reverse('health-check'))
          self.assertEqual(response.status_code, 200)
          self.assertEqual(response["Content-Type"], "application/json")
          data = response.json()
          self.assertEqual(data, {"status": "ok"})
  ```

- Run the test and verify it fails (expected at this stage):
  ```bash
  python manage.py test api.tests.test_health
  ```

#### GREEN Phase

- Implement minimal code to make the test pass:

  ```python
  # backend/api/views.py
  from django.http import JsonResponse

  def health_check(request):
      return JsonResponse({"status": "ok"})
  ```

- Configure URL routing:

  ```python
  # backend/api/urls.py
  from django.urls import path
  from . import views

  urlpatterns = [
      path('health-check/', views.health_check, name='health-check'),
  ]
  ```

  ```python
  # backend/hellobirdie/urls.py
  from django.contrib import admin
  from django.urls import path, include

  urlpatterns = [
      path('admin/', admin.site.urls),
      path('api/', include('api.urls')),
  ]
  ```

- Run the test again to verify it passes:

  ```bash
  python manage.py test api.tests.test_health
  ```

- Commit Point: "Health check endpoint implementation"
  > Why: Completes first feature using TDD workflow

### 5. Settings Structure Refactoring (REFACTOR Phase)

Follow the [Django Settings Structure](./details/django-settings-structure.md) guide to:

- Create settings directory structure
  ```
  hellobirdie/
  └── settings/
      ├── __init__.py  # Settings loader
      ├── base.py      # Common settings
      ├── local.py     # Development settings
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

- Configure database settings in the appropriate settings files:
  - PostgreSQL for all environments (local.py, test.py, production.py)
  - Use environment variables to configure database connections
- Create initial migrations
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```
- Run and verify tests in both environments

  ```bash
  # Local environment
  python manage.py test

  # Docker environment
  docker-compose up -d
  docker-compose exec backend python manage.py test
  docker-compose down
  ```

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
python manage.py test
# or with pytest
pytest

# Run tests with coverage
pytest --cov=api
```

### Docker Testing (Secondary)

```bash
# Start services
docker-compose up -d

# Run tests in container
docker-compose exec backend python manage.py test
# or with pytest
docker-compose exec backend pytest

# Run tests with coverage
docker-compose exec backend pytest --cov=api

# Stop services
docker-compose down
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
