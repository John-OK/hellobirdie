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
                os.environ.get("POSTGRES_TEST_DB", "test_hellobirdie")
                if IN_DOCKER
                else os.environ.get("LOCAL_POSTGRES_DB", "hellobirdie_test")
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
