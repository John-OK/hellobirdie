# Environment Configuration

This guide provides detailed instructions for setting up the environment configuration for the HelloBirdie backend, as referenced in [Step 2 of the Hybrid Backend Setup Guide](../hybrid-backend-setup-guide.md). This step focuses on setting up the requirements files and environment variables needed for the project.

## Requirements Files

Create the following requirements files in the `backend/requirements/` directory:

### base.txt

This file contains the core dependencies needed for both development and production. Create a file named `base.txt` in the `backend/requirements/` directory with the following content:

```
# Core Django dependencies
Django==5.1.6
djangorestframework==3.15.2

# Database - PostgreSQL adapter for Python 3.13.1
psycopg==3.2.6  # Modern PostgreSQL adapter with Python 3.13.1 compatibility

# Environment variables
python-dotenv==1.0.0

# Database URL parsing (for flexible database configuration)
dj-database-url==2.3.0

# API documentation
drf-spectacular==0.27.0

# CORS
django-cors-headers==4.3.1
```

### local.txt

This file contains dependencies needed for local development. Create a file named `local.txt` in the `backend/requirements/` directory with the following content:

```
# Import base requirements
-r base.txt

# Development tools
django-debug-toolbar==4.2.0
django-extensions==3.2.3

# Code quality
black==24.1.1
isort==5.13.2
flake8==7.0.0
```

### test.txt

This file contains dependencies needed for testing. Create a file named `test.txt` in the `backend/requirements/` directory with the following content:

```
# Import base requirements
-r base.txt

# Testing
pytest==7.4.3
pytest-django==4.7.0
pytest-cov==4.1.0
factory-boy==3.3.0
```

### docker.txt

This file contains dependencies needed for the Docker environment. Create a file named `docker.txt` in the `backend/requirements/` directory with the following content:

```
# Import base and test requirements
-r base.txt
-r test.txt

# Production-ready server
gunicorn==21.2.0

# Monitoring
sentry-sdk==1.39.1
```

## Environment Variables

### 1. Create Sample Environment Files

To support our hybrid workflow with proper separation of concerns, we'll create two environment files:

1. **Project Root `.env`**: Contains shared infrastructure settings used by Docker Compose and multiple services
2. **Backend `.env`**: Contains Django-specific settings used only by the backend application

This separation helps maintain clean architecture as the project scales.

#### Project Root Environment Sample

Create a file named `.env.sample` in the project root directory with the following content:

```
# Docker Compose PostgreSQL settings
POSTGRES_DB=hellobirdie
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db  # Service name in Docker Compose
POSTGRES_PORT=5432
DOCKER_DB_HOST_PORT=5433  # Port exposed to host
POSTGRES_TEST_DB=test_hellobirdie

# Docker environment configuration
# This is automatically set to True in the Docker container via docker-compose.yml
# IN_DOCKER=True

# Time zone setting
TZ=UTC
```

#### Backend Environment Sample

Create a file named `.env.backend.sample` in the backend directory with the following content:

```
# Django settings
DJANGO_ENV=local  # Options: local, test, production
# Do not set DJANGO_SETTINGS_MODULE here - it's handled by settings/__init__.py
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True

# Database URLs for environment detection
# For Docker environment (used when IN_DOCKER=True)
DATABASE_URL=postgres://postgres:postgres@db:5432/hellobirdie

# For Local Development (default when IN_DOCKER is not set)
LOCAL_DATABASE_URL=postgres://hellobirdie_user:hellobirdie_password@localhost:5432/hellobirdie

# Local database settings (these are used as fallbacks and for tests)
LOCAL_POSTGRES_DB=hellobirdie
LOCAL_POSTGRES_USER=hellobirdie_user
LOCAL_POSTGRES_PASSWORD=hellobirdie_password
LOCAL_POSTGRES_HOST=localhost
LOCAL_POSTGRES_PORT=5432

# API settings
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173
```

### 2. Create or Update Your Local Environment Files

We'll create two environment files: one in the project root for Docker and shared infrastructure settings, and one in the backend directory for Django-specific settings.

#### Project Root Environment File

First, let's check if a root `.env` file already exists:

```bash
# From the project root
if [ -f .env ]; then
  echo "*** Warning: Root .env file already exists. Please merge the contents manually. ***"
  echo "You can use the following command to see what's in the existing file:"
  echo "cat .env"
  echo "And compare with the sample:"
  echo "cat .env.sample"
else
  cp .env.sample .env
  echo "Root .env file created successfully."
fi
```

> **Important**: If a root .env file already exists (possibly created during frontend setup), DO NOT overwrite it. Instead, carefully merge the infrastructure-related variables into the existing file to avoid losing frontend configuration.

#### Backend Environment File

Now, let's create the backend-specific `.env` file:

```bash
# From the project root
mkdir -p backend  # Make sure backend directory exists

if [ -f backend/.env ]; then
  echo "*** Warning: Backend .env file already exists. Please merge the contents manually. ***"
  echo "You can use the following command to see what's in the existing file:"
  echo "cat backend/.env"
  echo "And compare with the sample:"
  echo "cat .env.backend.sample"
else
  cp .env.backend.sample backend/.env
  echo "Backend .env file created successfully."
fi
```

> **Important**: Keep Django-specific settings in the backend/.env file and infrastructure settings in the root .env file for proper separation of concerns. This separation will be leveraged in [Step 5: Settings Structure Refactoring](./step5-settings-structure-refactoring.md) when we implement a comprehensive settings structure.

#### How to Safely Merge Environment Variables

If you already have an .env file, follow these steps to merge in the backend variables:

1. **Create a temporary file** with just the backend variables:

   ```bash
   # Create a temporary file with backend variables
   cp .env.sample .env.backend_temp
   ```

2. **Compare the files** to identify what needs to be added:

   ```bash
   # View differences (variables in .env.backend_temp that aren't in .env)
   grep -Fxv -f .env .env.backend_temp
   ```

3. **Manually add missing variables** to your existing .env file:

   ```bash
   # Open your existing .env file in an editor
   nano .env  # or your preferred editor
   ```

4. **Clean up** the temporary file:
   ```bash
   # Remove the temporary file when done
   rm .env.backend_temp
   ```

> **Tip**: When merging, organize your .env file with clear section headers (e.g., `# BACKEND VARIABLES`, `# FRONTEND VARIABLES`) to make future maintenance easier.

### 4. Customize Environment Variables

Edit the `.env` file to customize the variables based on your local development environment. Here's when and why you might need to modify specific variables:

| Variable                                | When to Change                        | Why                                                           |
| --------------------------------------- | ------------------------------------- | ------------------------------------------------------------- |
| `DJANGO_SECRET_KEY`                     | **Always** for production             | Security: Each environment should have a unique secret key    |
| `POSTGRES_USER`, `POSTGRES_PASSWORD`    | If using custom database credentials  | Security: Use your local PostgreSQL credentials               |
| `POSTGRES_HOST`                         | If database is on a different host    | Configuration: Use `localhost` for local dev, `db` for Docker |
| `POSTGRES_PORT`                         | If using non-standard PostgreSQL port | Configuration: Default is 5432                                |
| `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS` | If using different frontend URLs      | Security: Only add domains you trust                          |

> **Note**: The `.env` file contains sensitive information and should never be committed to version control. The `.env.sample` file serves as a template with safe default values.

### 4.1 Understanding the Dual Environment Files Strategy

The HelloBirdie project uses a dual environment files strategy for better separation of concerns:

#### Project Root `.env`

- **Purpose**: Shared infrastructure settings used by Docker Compose and multiple services
- **Location**: Project root directory (`/.env`)
- **Used By**: Docker Compose, CI/CD pipelines, and shared infrastructure services
- **Contains**: Database credentials for Docker, infrastructure ports, shared service variables
- **Why**: Centralized location for Docker Compose variables and easier team collaboration

#### Backend `.env`

- **Purpose**: Django-specific settings used only by the backend
- **Location**: Backend directory (`/backend/.env`)
- **Used By**: Django application, tests, and backend-specific scripts
- **Contains**: Django settings, database URLs, API configuration, authentication secrets
- **Why**: Clearer separation of concerns, easier maintenance as the project grows

### 4.2 Understanding the Dual Database Configuration

The HelloBirdie project uses a hybrid workflow with a dual database configuration approach:

#### Local Development Environment (Primary)

- **Connection String**: `LOCAL_DATABASE_URL=postgres://hellobirdie_user:hellobirdie_password@localhost:5432/hellobirdie`
- **Credentials**: Username `hellobirdie_user`, password `hellobirdie_password`
- **Host**: `localhost` (your local PostgreSQL server)
- **When Used**: For daily development with `python manage.py runserver` and `python manage.py test`
- **Why**: Faster iterations, better IDE integration, more secure than default credentials
- **Note**: The user needs CREATEDB permission for running Django tests locally

#### Docker Environment (Verification)

- **Connection String**: `DATABASE_URL=postgres://postgres:postgres@db:5432/hellobirdie`
- **Credentials**: Username `postgres`, password `postgres`
- **Host**: `db` (the Docker service name)
- **When Used**: For verification before commits with `docker compose up` and `docker compose exec backend python manage.py test`
- **Why**: Ensures consistent environment for team collaboration and CI/CD

> **Important**: In Step 3, you'll set up both configurations:
>
> - The Docker configuration is handled automatically by `docker-compose.yml` using the project root `.env`
> - The local PostgreSQL setup requires manual database and user creation (Step 3, Section 5.4)
>
> The Django settings will detect which environment you're using and select the appropriate connection string from the backend `.env` file.

### 4.2 Environment Variables in a Full-Stack Project

Since HelloBirdie is a full-stack project with separate frontend and backend components, it's important to manage environment variables carefully:

#### Option 1: Single .env File (Recommended for Development)

For local development, a single `.env` file in the project root can work if:

- Variables are clearly sectioned (e.g., `# BACKEND VARIABLES` and `# FRONTEND VARIABLES`)
- There are no naming conflicts between frontend and backend variables

#### Option 2: Separate .env Files (Recommended for Production)

For more complex setups or production environments:

- Backend: `/backend/.env` for Django-specific variables
- Frontend: `/frontend/.env` for React-specific variables

> **Important**: If you're using separate .env files, make sure to update any scripts or documentation that reference environment variables to point to the correct file location.

## Next Steps

After configuring the environment:

1. Proceed to [Step 3: Django Project Initialization](./step3-django-project-initialization.md) to create the Django project structure and configure Docker.
2. Then follow the TDD process to implement your first feature.
