# Environment Configuration

This guide provides detailed instructions for setting up the environment configuration for the HelloBirdie backend, as referenced in [Step 2 of the Hybrid Backend Setup Guide](../hybrid-backend-setup-guide.md).

## Requirements Files

Create the following requirements files in the `backend/requirements/` directory:

### base.txt

This file contains the core dependencies needed for both development and production:

```bash
# From project root
cat > backend/requirements/base.txt << 'EOF'
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
EOF
```

### local.txt

This file contains dependencies needed for local development:

```bash
# From project root
cat > backend/requirements/local.txt << 'EOF'
# Import base requirements
-r base.txt

# Development tools
django-debug-toolbar==4.2.0
django-extensions==3.2.3

# Code quality
black==24.1.1
isort==5.13.2
flake8==7.0.0
EOF
```

### test.txt

This file contains dependencies needed for testing:

```bash
# From project root
cat > backend/requirements/test.txt << 'EOF'
# Import base requirements
-r base.txt

# Testing
pytest==7.4.3
pytest-django==4.7.0
pytest-cov==4.1.0
factory-boy==3.3.0
EOF
```

### docker.txt

This file contains dependencies needed for the Docker environment:

```bash
# From project root
cat > backend/requirements/docker.txt << 'EOF'
# Import base and test requirements
-r base.txt
-r test.txt

# Production-ready server
gunicorn==21.2.0

# Monitoring
sentry-sdk==1.39.1
EOF
```

## Docker Configuration

### Dockerfile

Create a Dockerfile for the backend:

```bash
# From project root
cat > backend/Dockerfile << 'EOF'
FROM python:3.13.1-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_ENV=production

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements /app/requirements
RUN pip install --no-cache-dir -r requirements/docker.txt

# Copy project
COPY . /app/

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "hellobirdie.wsgi:application"]
EOF
```

### docker-compose.yml

Create a docker-compose.yml file in the project root:

```bash
# From project root
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  backend:
    build: ./backend
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    environment:
      - DJANGO_ENV=development
      - DATABASE_URL=postgres://postgres:postgres@db:5432/hellobirdie
    depends_on:
      - db

  db:
    image: postgres:17.4
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=hellobirdie
    ports:
      - "5432:5432"

volumes:
  postgres_data:
EOF
```

## Environment Variables

Create a sample `.env` file in the project root:

```bash
# From project root
cat > .env.sample << 'EOF'
# Django settings
DJANGO_ENV=local
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True

# Database settings
POSTGRES_DB=hellobirdie
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_TEST_DB=test_hellobirdie

# API settings
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
EOF
```

Add instructions to create a real `.env` file:

```bash
# From project root
echo "# Copy the sample .env file to create your own .env file:" > README.env
echo "cp .env.sample .env" >> README.env
echo "# Then edit .env to set your own values" >> README.env
```

## Testing Docker Setup

To verify your Docker setup is working correctly:

```bash
# From project root
docker-compose build
docker-compose up -d
docker-compose ps  # Should show both services running
docker-compose logs backend  # Check for any errors
```

To run tests in the Docker environment:

```bash
docker-compose exec backend pytest
```

## Next Steps

After configuring the environment:

1. Proceed to [Django Project Initialization](./django-project-initialization.md) to create the Django project.
2. Then follow the TDD process to implement your first feature.
