# Django Project Initialization

This guide walks through initializing the Django project for HelloBirdie, following our Test-Driven Development (TDD) approach. This document is referenced from the [Hybrid Backend Setup Guide](../hybrid-backend-setup-guide.md) and provides detailed steps for setting up the Django project structure.

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
django-admin startproject hellobirdie .
```

## 3. Create API App

Create the API app where we'll implement our endpoints:

```bash
# Create the API app
python manage.py startapp api

# Create tests directory structure
mkdir -p api/tests
touch api/tests/__init__.py
```

## 4. Write First Test (RED Phase)

Following TDD principles, write a test for the health check endpoint before implementing it:

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

## 5. Run the Test and Watch it Fail (RED Phase)

Run the test to verify it fails (this is expected and part of TDD):

```bash
python manage.py test api.tests.test_health
```

You should see an error about 'health-check' not being a valid view or pattern name.

## 6. Implement Health Check View (GREEN Phase)

Now implement the minimal code to make the test pass:

```python
# backend/api/views.py
from django.http import JsonResponse

def health_check(request):
    data = {"status": "ok"}
    return JsonResponse(data)
```

## 7. Configure URLs

Set up the URL routing for the health check endpoint:

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

## 8. Run Tests Again (GREEN Phase)

Run the test again to verify it now passes:

```bash
python manage.py test api.tests.test_health
```

You should see that the test passes successfully.

## 9. Refactor (REFACTOR Phase)

This is where you would refactor your code if needed, while ensuring tests continue to pass. For our simple health check, there might not be much to refactor yet.

## 10. Settings Structure Refactoring

Once you have a working endpoint with passing tests, you can refactor your settings structure. This is part of the REFACTOR phase of TDD.

```bash
# Create settings directory
mkdir -p hellobirdie/settings
touch hellobirdie/settings/__init__.py
```

For detailed instructions on implementing the split settings approach, refer to the [Django Settings Structure](./django-settings-structure.md) guide, which covers:

- Creating base.py for common settings
- Creating local.py for development settings
- Creating test.py for test-specific settings
- Setting up the settings loader in **init**.py

## 11. Run Development Server

After completing the implementation and refactoring, start the development server to manually verify the endpoint:

```bash
python manage.py runserver
```

Test the endpoint using one of these methods:

1. Visit http://127.0.0.1:8000/api/health-check/ in your browser
2. Use curl from the terminal:
   ```bash
   curl http://127.0.0.1:8000/api/health-check/
   ```
3. Use a tool like Postman or Insomnia

You should see the JSON response: `{"status": "ok"}`

## 12. Next Steps

After successfully initializing your Django project with a working health check endpoint, you can:

1. Configure your database settings (see step 6 in the [Hybrid Backend Setup Guide](../hybrid-backend-setup-guide.md))
2. Begin implementing additional API endpoints following the same TDD process
3. Set up authentication if required

Always remember to follow the TDD cycle: RED (write failing test) → GREEN (make it pass) → REFACTOR (improve the code).
