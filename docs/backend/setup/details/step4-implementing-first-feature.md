# Implementing First Feature with TDD

This guide provides detailed instructions for implementing the health check endpoint using Test-Driven Development (TDD) principles. This corresponds to **Step 4** in the [Hybrid Backend Setup Guide](../hybrid-backend-setup-guide.md).

## Why Start with a Health Check?

A health check endpoint is an ideal first feature because:

- It's simple to implement but provides immediate value
- It establishes the basic API structure and testing patterns
- It helps verify that your entire stack (Django, database, web server) is functioning correctly
- It's a standard practice in modern API development for monitoring and reliability
- It serves as a foundation for more complex features

## TDD Workflow Overview

We'll follow the classic RED-GREEN-REFACTOR cycle:

1. **RED**: Write a failing test
2. **GREEN**: Implement the minimal code to make the test pass
3. **REFACTOR**: Improve the code while keeping tests passing

## 1. Write the Test (RED Phase)

Ensure you're in the project root directory before proceeding with these steps.

Create a file named `test_health.py` in the `backend/api/tests/` directory:

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

Run the test to verify it fails (expected at this stage):

```bash
# Using default settings
python manage.py test api.tests.test_health

# Or using test-specific settings
DJANGO_ENV=test python manage.py test api.tests.test_health
```

You should see an error about 'health-check' not being a valid view or pattern name.

## 2. Implement the View (GREEN Phase)

Create or update the file named `views.py` in the `backend/api/` directory:

```python
# backend/api/views.py
from django.http import JsonResponse

def health_check(request):
    data = {"status": "ok"}
    return JsonResponse(data)
```

## 3. Configure URLs

Create a file named `urls.py` in the `backend/api/` directory:

```python
# backend/api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('health-check/', views.health_check, name='health-check'),
]
```

Update the file named `urls.py` in the `backend/hellobirdie/` directory:

```python
# backend/hellobirdie/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
```

## 4. Run Tests Again (GREEN Phase)

Run the test again to verify it now passes:

```bash
# Using default settings
python manage.py test api.tests.test_health

# Or using test-specific settings
DJANGO_ENV=test python manage.py test api.tests.test_health
```

You should see that the test passes successfully.

## 5. Refactor (REFACTOR Phase)

This is where you would refactor your code if needed, while ensuring tests continue to pass. For our simple health check, there might not be much to refactor yet.

## 6. Manual Verification

You can manually verify the endpoint by starting the development server:

```bash
python manage.py runserver
```

Then navigate to http://127.0.0.1:8000/api/health-check/ in your browser or use a tool like curl:

```bash
curl http://127.0.0.1:8000/api/health-check/
```

You should see the JSON response: `{"status": "ok"}`

## Next Steps

After completing this feature, proceed to [Step 5: Settings Structure Refactoring](./step5-settings-structure-refactoring.md) to improve the project organization.
