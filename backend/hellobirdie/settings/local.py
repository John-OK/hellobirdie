import os
import dj_database_url
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

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
            "NAME": (
                os.environ.get("LOCAL_POSTGRES_DB", "hellobirdie")
                if not IN_DOCKER
                else os.environ.get("POSTGRES_DB", "hellobirdie")
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
