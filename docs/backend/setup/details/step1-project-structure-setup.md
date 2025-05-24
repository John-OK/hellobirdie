# Project Structure Setup

This guide walks through setting up the initial project structure for the HelloBirdie backend. This document corresponds to **Step 1** in the [Hybrid Backend Setup Guide](../hybrid-backend-setup-guide.md) and provides detailed steps for creating the necessary directory structure and configuration files.

## Directory Structure

### Why This Structure?

The HelloBirdie project follows a structured approach to organizing code and documentation that provides several benefits:

- **Separation of Concerns**: Clearly separating backend and frontend code makes the codebase easier to navigate and maintain
- **Modular Organization**: Grouping related files (like requirements) into dedicated directories improves discoverability
- **Documentation Proximity**: Keeping documentation close to the code it describes helps maintain documentation accuracy
- **Industry Standards**: This structure follows common practices in professional Django projects
- **Scalability**: As the project grows, this organization will accommodate new components without major restructuring

Create the following directory structure for the backend:

```
hellobirdie/
├── backend/            # Backend root directory
│   ├── requirements/   # Dependency management
│   └── ...             # Django project files (added later)
├── docs/               # Project documentation
│   ├── backend/        # Backend documentation
│   │   ├── api/        # API documentation
│   │   └── setup/      # Setup guides and details
│   ├── frontend/       # Frontend documentation
│   └── project/        # Project-wide documentation
│       └── architecture/ # System architecture docs
├── frontend/           # Frontend code (not covered in this guide)
└── ...                 # Other project files
```

Use these commands to create the initial structure:

```bash
# From project root
mkdir -p backend/requirements
mkdir -p docs/backend/api
mkdir -p docs/backend/setup
mkdir -p docs/frontend
mkdir -p docs/project/architecture
```

## .gitignore Configuration

You'll need to update the project's `.gitignore` file to include Python and Django-specific patterns. First, check if a `.gitignore` file already exists (it might if the frontend was set up first):

```bash
# Check if .gitignore exists
if [ -f .gitignore ]; then
  echo ".gitignore file already exists. You'll need to merge backend patterns."
else
  echo "Creating new .gitignore file"
  touch .gitignore
fi
```

### If Creating a New .gitignore

If you're creating a new `.gitignore` file, add the following Python and Django-specific patterns:

```
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
```

### If Merging with an Existing .gitignore

If a `.gitignore` file already exists (likely from frontend setup), follow these steps to merge the backend patterns:

1. **Create a temporary backend .gitignore file**:

   ```bash
   # Create a temporary file with backend .gitignore patterns
   cat > .gitignore.backend_temp << 'EOL'
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
   EOL
   ```

2. **Compare and identify missing patterns**:

   ```bash
   # View what's in the existing .gitignore
   cat .gitignore

   # View differences (variables in .gitignore.backend_temp that aren't in .gitignore)
   grep -Fxv -f .gitignore .gitignore.backend_temp
   ```

3. **Manually merge the missing patterns** into your existing `.gitignore` file, ensuring you don't duplicate entries.

4. **Clean up**:

   ```bash
   # Remove the temporary file
   rm .gitignore.backend_temp
   ```

## Next Steps

After setting up the basic project structure:

1. Proceed to [Step 2: Environment Configuration](./step2-environment-configuration.md) to set up requirements files and Docker configuration.
2. Then follow the [Step 3: Django Project Initialization](./step3-django-project-initialization.md) guide to create the Django project.
