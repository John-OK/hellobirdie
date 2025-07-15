# Development Environment Setup

## Prerequisites

### Required Software for Local Development (Primary)

- Python 3.13.1
  > Latest stable version with optimized performance and security features
- PostgreSQL 17.4
  > Latest stable version for local database development
- nvm 0.40.1
  > Node Version Manager for installing and managing Node.js versions
- Node.js 22.14.0 (LTS)
  > Latest Long Term Support version for optimal stability and security
- Git

### Required Software for Docker Verification (Secondary)

- Docker Desktop 4.38.0 or Docker Engine 28.0.0
- Docker Compose 2.33.0

### Recommended Tools

- Modern IDE (VS Code recommended for TypeScript/Python integration)
- pgAdmin or DBeaver for database management
- Postman or Insomnia for API testing

> Note: We use a hybrid development approach where daily development happens in the local environment and Docker is used for verification before commits. This approach provides faster development cycles and a better learning experience.

## Database Setup

### PostgreSQL Configuration

Before running the backend, you need to set up the PostgreSQL database:

```bash
# Connect to PostgreSQL as a superuser
# You will be prompted to enter a password. Use the password for your account on the current machine.
sudo -u postgres psql

# Inside the PostgreSQL prompt, create the user and database
CREATE USER hellobirdie_user WITH PASSWORD 'hellobirdie_password';
CREATE DATABASE hellobirdie OWNER hellobirdie_user;

# Grant necessary privileges
GRANT ALL PRIVILEGES ON DATABASE hellobirdie TO hellobirdie_user;

# Exit PostgreSQL prompt
\q
```

### Verify Database Connection

After setting up your database, you can verify the connection using:

```bash
psql -U hellobirdie_user -h localhost -d hellobirdie
```

Enter the password when prompted ('hellobirdie_password').

## TypeScript Development Setup

### IDE Configuration

Required VS Code extensions:

- TypeScript + JavaScript Language Features (built-in)
- ESLint (dbaeumer.vscode-eslint)
- Prettier (esbenp.prettier-vscode)

Recommended settings:

```json
{
  "typescript.updateImportsOnFileMove.enabled": "always",
  "typescript.suggest.completeFunctionCalls": true,
  "typescript.preferences.importModuleSpecifier": "non-relative"
}
```

### TypeScript Configuration

Our `tsconfig.json` enforces:

- Strict type checking
- No implicit any
- Strict null checks
- Explicit function return types

### Development Standards

1. Type Safety

   - All components must have explicit type definitions
   - Use TypeScript utility types where appropriate
   - Implement proper error boundaries with type checking

2. Component Architecture

   - Follow presentational/container pattern
   - Implement proper prop interfaces
   - Use typed custom hooks for shared logic

3. Performance Considerations
   - Implement proper memoization
   - Use type-safe context providers
   - Follow React performance best practices

## Initial Setup

### 1. Clone Repository

```bash
git clone https://github.com/John-OK/hellobirdie.git
cd hellobirdie
```

### 2. Backend Setup

#### Local Development Setup (Primary)

##### 1. Prerequisites: Install PostgreSQL Client Libraries

Psycopg (the PostgreSQL adapter for Python) requires system-level dependencies. Install them before proceeding:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y gcc postgresql-client libpq-dev

# macOS (using Homebrew)
brew install postgresql libpq
# You may need to add libpq to your path:
export PATH="/usr/local/opt/libpq/bin:$PATH"

# Windows
# Install PostgreSQL from the installer which includes the required client libraries
# https://www.postgresql.org/download/windows/
```

##### 2. Python Environment Setup

```bash
# Create and activate virtual environment (if not already done)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements/local.txt
```

##### 3. Database Setup and Running the Server

```bash
# Run migrations
cd backend
python manage.py migrate

# Start development server
python manage.py runserver
```

##### Troubleshooting psycopg Installation

If you encounter errors installing psycopg:

1. Ensure PostgreSQL client libraries are properly installed
2. For macOS: Try `pip install psycopg --no-binary psycopg`
3. For Windows: Ensure you have the Visual C++ build tools installed
4. For all platforms: Consider using `pip install psycopg2-binary` as an alternative (though not recommended for production)

#### Docker Configuration (Secondary - For Verification)

```bash
# Build and start containers
docker compose up --build -d

# View logs
docker compose logs -f
```

> **Note:** For Docker Compose V1 (older versions), use `docker-compose` instead of `docker compose`. The project requires Docker Compose 2.33.0 or newer, which uses the V2 syntax without the hyphen.

The Docker Compose configuration sets up:

- Python 3.13 environment
- PostgreSQL 17 database
- Development server
- Test environment

#### Environment Variables

```bash
cp .env.example .env
```

Required variables in `.env`:

```plaintext
# Django settings
DJANGO_ENV=local  # Options: local, test, production
DJANGO_SETTINGS_MODULE=hellobirdie.settings.local
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True  # Set to False in production

# Database settings - Hybrid Approach
# For Docker environment (used when IN_DOCKER=True)
DATABASE_URL=postgres://postgres:postgres@db:5432/hellobirdie
DOCKER_DB_HOST_PORT=5433  # The host port when running in Docker

# For Local Development (default when IN_DOCKER is not set)
LOCAL_DATABASE_URL=postgres://hellobirdie_user:hellobirdie_password@localhost:5432/hellobirdie

# Individual Database Components
POSTGRES_DB=hellobirdie
POSTGRES_USER=hellobirdie_user  # Used for local development
POSTGRES_PASSWORD=hellobirdie_password  # Used for local development
POSTGRES_HOST=localhost  # For local development
POSTGRES_PORT=5432  # Local PostgreSQL port
POSTGRES_TEST_DB=test_hellobirdie

# Time zone setting (consistent with Docker configuration)
TZ=UTC

# API settings
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173

# Environment detection (used in settings to determine which database URL to use)
# This is automatically set to True in the Docker container via docker-compose.yml
# IN_DOCKER=True

# Third-party APIs (add keys when obtained)
XENO_CANTO_API_KEY=your_key_here
MAP_TILES_API_KEY=your_key_here  # If using commercial map tiles
```

#### Development Tools

The Docker setup includes:

- pytest for testing
- black for code formatting
- isort for import sorting
- flake8 for linting

Run tools in both environments:

```bash
# Run tests locally (primary workflow)
cd backend
python manage.py test api.tests.<test_module>  # Run specific tests

# Run tests in Docker (verification)
docker compose exec backend python manage.py test api.tests.<test_module>

# Format code locally
cd backend
black .
isort .

# Run linting locally
flake8

# Or run tools through Docker if preferred
docker compose exec backend black .
docker compose exec backend isort .
docker compose exec backend flake8
```

#### Database Management

Both local and Docker databases are used in our hybrid workflow:

##### Local Database (Primary)

- Created manually on the local PostgreSQL server
- Used for daily development and testing
- Accessible directly via standard PostgreSQL tools

##### Docker Database (Secondary)

- Created automatically by Docker Compose
- Used for verification before commits
- Migrated during container startup

Access databases:

```bash
# Access local PostgreSQL database (primary for development)
psql -h localhost -p 5432 -U hellobirdie_user -d hellobirdie

# Access Docker PostgreSQL database (verification)
# Note the port is 5433 to avoid conflicts with local PostgreSQL
psql -h localhost -p 5433 -U postgres -d hellobirdie

# Alternatively, access Docker database directly through Docker
docker compose exec db psql -U postgres -d hellobirdie
```

### 3. Frontend Setup

#### Node Modules

```bash
cd frontend
npm install

# Install development tools
npm install -D prettier eslint
```

#### Environment Variables

```bash
cp .env.example .env
```

Required variables in frontend `.env`:

```plaintext
VITE_API_URL=http://localhost:8000
VITE_MAP_TILES_URL=https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png
```

## Running the Application

### Backend

```bash
cd backend
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm run dev
```

## Development Tools

### Code Formatting

- Python: Black
  ```bash
  black .  # Format Python code
  ```
- TypeScript: Prettier
  ```bash
  npm run format  # Format TypeScript/JavaScript
  ```

### Recommended IDE Extensions

These work in VS Code and similar IDEs:

- ESLint (dbaeumer.vscode-eslint)
- Prettier (esbenp.prettier-vscode)
- Python Extension Pack (donjayamanne.python-extension-pack)
- TypeScript + JavaScript Language Features (built-in)
- GitLens (eamodio.gitlens)

### Browser Extensions

- React Developer Tools
- Redux DevTools (if using Redux)

## Common Issues

### Initial Common Issues

1. **PostgreSQL Connection Issues**

   - Ensure PostgreSQL service is running
   - Verify database name and credentials
   - Check port availability

2. **Python Virtual Environment**

   - Ensure `venv` is activated
   - Check Python version matches project requirement

3. **Node.js Dependencies**
   - Clear npm cache if packages fail to install:
     ```bash
     npm cache clean --force
     rm -rf node_modules
     npm install
     ```
   - Ensure Node.js version matches project requirement
   - If modules are still failing, try:
     ```bash
     npm install --legacy-peer-deps
     ```

> Note: This section will be updated as new issues are discovered during development. Each issue includes specific troubleshooting steps. If you encounter a new issue, please add it here with detailed resolution steps.

## Testing

### Running Tests

```bash
# Backend tests
# Always specify the test module path to avoid import errors
python manage.py test api.tests.<test_module>

# Example: Test the health check endpoint
python manage.py test api.tests.test_health

# Frontend tests
npm test
```

### Coverage Goals

- Overall coverage: 70% (soft target)
- Critical paths: 90% (authentication, data processing)
- Utility functions: No strict requirement

> Note: Coverage requirements may be adjusted as the project evolves

## Additional Resources

- [System Overview](/docs/project/architecture/system-overview.md)
- [Contributing Guidelines](/CONTRIBUTING.md)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Django Documentation](https://docs.djangoproject.com/)
- [React Documentation](https://react.dev/)
