# Settings Structure Refactoring

This guide provides detailed instructions for refactoring the Django settings structure to follow best practices. This corresponds to **Step 5** in the [Hybrid Backend Setup Guide](../hybrid-backend-setup-guide.md).

## Overview

In Step 3 (Django Project Initialization), we created a minimal settings structure to support Docker testing. Now we'll enhance and properly organize this structure following best practices.

## Split Settings Approach

For the HelloBirdie project, we're using a split settings approach with three main files. This approach follows the REFACTOR phase of our TDD cycle, improving project organization while maintaining functionality.

```
settings/
├── __init__.py  # Settings loader (already created in Step 3)
├── base.py      # Common settings
├── local.py     # Development settings (enhance the minimal version from Step 3)
└── test.py      # Test-specific settings
```

## Benefits

### 1. Clear Separation of Concerns

- **Conceptual Organization**: Each environment has distinct requirements
- **Learning Progression**: Understand which settings belong in which environments
- **Explicit Configuration**: Makes environment-specific settings obvious

### 2. Easier Testing

- **Isolated Test Environment**: Test settings don't affect development
- **Production-like Tests**: Using PostgreSQL for tests ensures compatibility
- **Reproducible Tests**: Consistent test environment configuration

### 3. Safer Production Deployments

- **Reduced Risk**: Development settings never leak to production
- **Environment-Specific Optimizations**: Each environment can be tuned
- **Security Separation**: Secrets stay in appropriate environments

### 4. Better Collaboration

- **Team Standards**: Clear structure for where settings belong
- **Onboarding**: New developers understand the project structure faster
- **Code Reviews**: Easier to verify environment-specific changes

## Implementation Steps

### 1. Enhance the Minimal Settings Structure

The directory structure should already exist from Step 3. If not, create it with:

```bash
# From the backend directory
mkdir -p hellobirdie/settings
touch hellobirdie/settings/__init__.py
```

### 2. Create Base Settings (base.py)

Create a file named `base.py` in the `backend/hellobirdie/settings/` directory with the following common settings that will be shared across all environments:

```python
# hellobirdie/settings/base.py
import os
from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-default-key-for-dev')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local apps
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hellobirdie.urls'

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

WSGI_APPLICATION = 'hellobirdie.wsgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

### 3. Enhance Local Settings (local.py)

**Note**: This will completely replace the minimal version of `local.py` created in Step 3 with a more comprehensive implementation that better handles database connections for our hybrid workflow:

```python
# hellobirdie/settings/local.py
import os
import dj_database_url
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

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
            "NAME": os.environ.get("LOCAL_POSTGRES_DB", "hellobirdie") if not IN_DOCKER else os.environ.get("POSTGRES_DB", "hellobirdie"),
            "USER": os.environ.get("LOCAL_POSTGRES_USER", "hellobirdie_user") if not IN_DOCKER else os.environ.get("POSTGRES_USER", "postgres"),
            "PASSWORD": os.environ.get("LOCAL_POSTGRES_PASSWORD", "hellobirdie_password") if not IN_DOCKER else os.environ.get("POSTGRES_PASSWORD", "postgres"),
            "HOST": os.environ.get("LOCAL_POSTGRES_HOST", "localhost") if not IN_DOCKER else os.environ.get("POSTGRES_HOST", "db"),
            "PORT": os.environ.get("LOCAL_POSTGRES_PORT", "5432") if not IN_DOCKER else os.environ.get("POSTGRES_PORT", "5432"),
        }
    }
```

### 4. Create Test Settings (test.py)

Create a file named `test.py` in the `backend/hellobirdie/settings/` directory with the following content:

```python
# hellobirdie/settings/test.py
import os
import dj_database_url
from .base import *

DEBUG = False

# Normalize IN_DOCKER to bool
IN_DOCKER = os.environ.get('IN_DOCKER', '').lower() == 'true'

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

# Faster password hashing for tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable logging during tests
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}
```

### 5. Create Settings Loader (**init**.py)

Update the `__init__.py` file in `backend/hellobirdie/settings/` to load the appropriate settings based on the environment:

```python
# hellobirdie/settings/__init__.py
import os

# Default to local settings if DJANGO_ENV is not set
env = os.environ.get('DJANGO_ENV', 'local')

if env == 'production':
    from .production import *
elif env == 'test':
    from .test import *
else:
    from .local import *
```

### 6. Update WSGI and ASGI Configuration

Update `wsgi.py` and `asgi.py` in `backend/hellobirdie/` to use the new settings module:

```python
# hellobirdie/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hellobirdie.settings')
application = get_wsgi_application()
```

```python
# hellobirdie/asgi.py
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hellobirdie.settings')
application = get_asgi_application()
```

### 7. Test the Refactored Settings

Run tests to ensure the refactoring didn't break functionality:

#### Local Testing (Development)

```bash
# Run tests with local settings
python manage.py test api.tests.test_health

# Run tests with test settings
DJANGO_ENV=test python manage.py test api.tests.test_health
```

#### Docker Testing (Pre-Commit Verification)

Following our hybrid approach, also verify in Docker before committing:

```bash
# From the project root
docker compose up -d

# Run tests in the Docker container
docker compose exec backend python manage.py test api.tests.test_health

# Or with test settings explicitly
docker compose exec backend bash -c "DJANGO_ENV=test python manage.py test api.tests.test_health"
```

This ensures tests pass in both local and Docker environments, which is essential for our hybrid testing workflow.

## Next Steps

After completing the settings structure refactoring, proceed to [Step 6: Database Configuration and Initial Migrations](./step6-database-configuration.md) to set up the database.
