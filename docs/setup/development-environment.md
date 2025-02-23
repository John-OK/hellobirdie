# Development Environment Setup

## Prerequisites

### Required Software

- Docker Desktop 4.38.0 or Docker Engine 28.0.0
  > Latest stable versions with enhanced security and performance features
- Docker Compose 2.33.0
  > Latest stable version with improved compose spec support
- Node.js 22.14.0 (LTS)
  > Latest Long Term Support version for optimal stability and security
- Git

### Recommended Tools

- Modern IDE (VS Code recommended for TypeScript/Python integration)
- pgAdmin or DBeaver for database management
- Postman or Insomnia for API testing

> Note: While Docker handles the runtime environment, local installations can enhance development:
>
> - Node.js 22.x (TypeScript development)
> - Python 3.13 (backend development)
> - PostgreSQL 17 (database management)

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

#### Docker Configuration

```bash
# Build and start containers
docker-compose up --build -d

# View logs
docker-compose logs -f
```

The docker-compose.yml file sets up:

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
# Docker Compose Settings
COMPOSE_PROJECT_NAME=hellobirdie

# Database
DB_NAME=hellobirdie_dev
DB_USER=hellobirdie_user
DB_PASSWORD=your_secure_password
DB_HOST=db  # Points to Docker service
DB_PORT=5432

# Django
DJANGO_SETTINGS_MODULE=hellobirdie.settings.local
DJANGO_SECRET_KEY=generate_a_secure_key
DEBUG=True  # Set to False in production

# APIs (add keys when obtained)
XENO_CANTO_API_KEY=your_key_here
MAP_TILES_API_KEY=your_key_here  # If using commercial map tiles
GEOLOCATION_API_KEY=your_key_here  # Optional
```

#### Development Tools

The Docker setup includes:

- pytest for testing
- black for code formatting
- isort for import sorting
- flake8 for linting

Run tools through Docker:

```bash
# Run tests
docker-compose exec backend pytest

# Format code
docker-compose exec backend black .
docker-compose exec backend isort .

# Run linting
docker-compose exec backend flake8
```

#### Database Management

The database is automatically:

- Created by Docker Compose
- Configured for Django
- Migrated during container startup

Access database:

```bash
# Using Docker
docker-compose exec db psql -U hellobirdie_user -d hellobirdie_dev

# Or using local PostgreSQL client
psql -h localhost -p 5432 -U hellobirdie_user -d hellobirdie_dev
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
python manage.py test

# Frontend tests
npm test
```

### Coverage Goals

- Overall coverage: 70% (soft target)
- Critical paths: 90% (authentication, data processing)
- Utility functions: No strict requirement

> Note: Coverage requirements may be adjusted as the project evolves

## Additional Resources

- [System Overview](/docs/architecture/system-overview.md)
- [Contributing Guidelines](/CONTRIBUTING.md)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Django Documentation](https://docs.djangoproject.com/)
- [React Documentation](https://react.dev/)
