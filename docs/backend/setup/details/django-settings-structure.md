# Django Settings Structure

## Split Settings Approach

For the HelloBirdie project, we're using a split settings approach with three main files. This approach follows the REFACTOR phase of our TDD cycle, as referenced in [Step 5 of the Hybrid Backend Setup Guide](../hybrid-backend-setup-guide.md), improving our project organization while maintaining functionality.

```
settings/
├── __init__.py  # Settings loader
├── base.py      # Common settings
├── local.py     # Development settings
└── test.py      # Test-specific settings
```

## Benefits for Learning

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

### 1. Create Settings Directory Structure

```bash
# From the backend directory
mkdir -p hellobirdie/settings
touch hellobirdie/settings/__init__.py
```

### 2. Create Base Settings (base.py)

Copy the core settings from your existing `settings.py` file to a new `base.py` file:

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

### 3. Create Local Settings (local.py)

Create development-specific settings:

```python
# hellobirdie/settings/local.py
import os
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database
# Use PostgreSQL for local development
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

### 4. Create Test Settings (test.py)

Create test-specific settings for faster test execution:

```python
# hellobirdie/settings/test.py
import os
from .base import *

DEBUG = False

# Use a dedicated PostgreSQL database for tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_TEST_DB', 'test_hellobirdie'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        'TEST': {
            'NAME': 'test_hellobirdie',
        },
    }
}

# Use faster password hasher for testing
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable non-critical middleware for faster tests
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]
```

### 5. Create Settings Loader (**init**.py)

Set up the settings loader to select the appropriate settings file based on environment variables:

```python
# hellobirdie/settings/__init__.py
import os

# Default to local settings
env = os.environ.get('DJANGO_ENV', 'local')

if env == 'test':
    from .test import *
elif env == 'production':
    from .production import *  # We'll create this later
else:  # 'local' or any other value
    from .local import *
```

### 6. Update WSGI and ASGI Configuration

Update the WSGI and ASGI configuration files to use the new settings module:

```python
# hellobirdie/wsgi.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hellobirdie.settings')
```

### 7. Update manage.py

Update manage.py to use the new settings module:

```python
# manage.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hellobirdie.settings')
```

## Environment Variables

Key environment variables for settings:

- `DJANGO_ENV`: Determines which settings file to use ('local', 'test', 'production')
- `DJANGO_SECRET_KEY`: Secret key for security
- `DJANGO_DEBUG`: Override debug mode flag
- `DATABASE_URL`: Database connection string (for production)

## Testing the Settings Structure

After implementing the split settings structure, run the tests to ensure everything still works:

```bash
# Run with default settings (local)
python manage.py test api.tests.test_health

# Run with test settings
DJANGO_ENV=test python manage.py test api.tests.test_health
```

## Common Issues and Solutions

1. **Import Errors**: If you encounter import errors, check that your relative imports use the correct paths after restructuring.

2. **Path Issues**: The `BASE_DIR` path needs to be adjusted since settings.py is now in a subdirectory.

3. **Environment Variables**: Ensure environment variables are properly set before running Django commands.

4. **Missing Settings**: If you split settings but forgot to move some values, Django will raise exceptions about missing settings.
