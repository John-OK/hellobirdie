# Project Structure Setup

This guide provides detailed instructions for setting up the initial project structure for the HelloBirdie backend, as referenced in [Step 1 of the Hybrid Backend Setup Guide](../hybrid-backend-setup-guide.md).

## Directory Structure

Create the following directory structure for the backend:

```
hellobirdie/
├── backend/            # Backend root directory
│   ├── requirements/   # Dependency management
│   └── ...             # Django project files (added later)
├── docs/               # Project documentation
│   └── setup/          # Setup guides
├── frontend/           # Frontend code (not covered in this guide)
└── ...                 # Other project files
```

Use these commands to create the initial structure:

```bash
# From project root
mkdir -p backend/requirements
mkdir -p docs/setup
```

## .gitignore Configuration

Update the project's `.gitignore` file to include Python and Django-specific patterns:

```bash
# From project root
cat >> .gitignore << 'EOF'

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg
.pytest_cache/
.coverage
htmlcov/

# Django
*.log
local_settings.py
media/

# Database
*.dump
*.sql
*.bak

# Virtual Environment
.venv/
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Environment variables
.env
.env.local
.env.development
.env.test
.env.production
EOF
```

## README.md Updates

Add backend setup instructions to the project README.md:

````markdown
## Backend Setup

The HelloBirdie backend is built with Django and follows a Test-Driven Development approach.

### Local Development Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Linux/Mac
   ```
````

2. Install dependencies:

   ```bash
   pip install -r backend/requirements/local.txt
   ```

3. Run the development server:
   ```bash
   cd backend
   python manage.py runserver
   ```

### Docker Testing

1. Start services:

   ```bash
   docker-compose up -d
   ```

2. Run tests:
   ```bash
   docker-compose exec backend pytest
   ```

For detailed setup instructions, see the [documentation](../hybrid-backend-setup-guide.md).

````

## Project Documentation

Create a basic README for the backend directory:

```bash
# From project root
cat > backend/README.md << 'EOF'
# HelloBirdie Backend

This directory contains the Django backend for the HelloBirdie application.

## Directory Structure

- `hellobirdie/` - Django project directory
- `api/` - Django app containing API endpoints
- `requirements/` - Dependency management files

## Development

See the [Hybrid Backend Setup Guide](../docs/setup/hybrid-backend-setup-guide.md) for detailed setup and development instructions.
EOF
````

## Next Steps

After setting up the basic project structure:

1. Proceed to [Environment Configuration](./environment-configuration.md) to set up requirements files and Docker configuration.
2. Then follow the [Django Project Initialization](./django-project-initialization.md) guide to create the Django project.
