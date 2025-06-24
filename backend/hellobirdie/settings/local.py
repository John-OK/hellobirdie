"""
Temporary local development settings for hellobirdie project.
This will be properly refactored in Step 5 (Settings Structure Refactoring).
"""

import os
import sys
import dj_database_url
from pathlib import Path

# Get the parent directory to access the main settings file
parent_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(parent_dir.parent))

# Define BASE_DIR for database path
BASE_DIR = parent_dir.parent

# Import all settings from the main settings file
from hellobirdie.settings import *

# Root URL configuration
ROOT_URLCONF = "hellobirdie.urls"

# Security settings
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY", "django-insecure-development-key-for-testing-only"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allow all hosts in local development
ALLOWED_HOSTS = ["*"]

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"

# Time zone settings
TIME_ZONE = "UTC"
USE_TZ = True

# Add the api app to INSTALLED_APPS
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "api",
]

# Templates configuration required for admin
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Middleware configuration required for admin
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Database configuration
# Use PostgreSQL for both local development and Docker environments

# Check if we're running in a Docker environment - normalize to bool
IN_DOCKER = os.environ.get("IN_DOCKER", "").lower() == "true"

# Database URL handling logic
# 1. If in Docker, use DATABASE_URL from backend/.env
# 2. If not in Docker but LOCAL_DATABASE_URL exists, use that from backend/.env
# 3. Otherwise fallback to individual environment variables

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
