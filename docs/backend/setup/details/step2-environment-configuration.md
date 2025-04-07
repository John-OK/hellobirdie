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

# Database
psycopg2-binary==2.9.9

# Environment variables
python-dotenv==1.0.0

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

### 1. Create Sample Environment File

Create a file named `.env.sample` in the project root directory with the following content:

```
# Django settings
DJANGO_ENV=local
DJANGO_SETTINGS_MODULE=hellobirdie.settings.local
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True

# Database settings - Docker
DATABASE_URL=postgres://postgres:postgres@db:5432/hellobirdie

# Database settings - Local Development
LOCAL_DATABASE_URL=postgres://hellobirdie_user:hellobirdie_password@localhost:5432/hellobirdie

# Individual Database Components (used by some Django settings)
POSTGRES_DB=hellobirdie
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_TEST_DB=test_hellobirdie

# API settings
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 2. Create or Update Your Local Environment File

Before creating or modifying the .env file, check if one already exists:

```bash
# From the project root
if [ -f .env ]; then
  echo "Warning: .env file already exists. Please merge the contents manually."
  echo "You can use the following command to see what's in the existing file:"
  echo "cat .env"
  echo "And compare with the sample:"
  echo "cat .env.sample"
else
  cp .env.sample .env
  echo ".env file created successfully."
fi
```

> **Important**: If an .env file already exists (possibly created during frontend setup), DO NOT overwrite it. Instead, carefully merge the backend variables into the existing file to avoid losing frontend configuration.

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
   grep -v -F -x -f .env .env.backend_temp
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

### 5. Environment Variables in a Full-Stack Project

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
