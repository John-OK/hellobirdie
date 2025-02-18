# Development Environment Setup

## Prerequisites

### Required Software

- Node.js 20.x
- Python 3.13
- PostgreSQL 17
- Git

### Recommended Tools

- Any modern IDE (e.g., VS Code, PyCharm, Sublime)
- pgAdmin or DBeaver for database management
- Postman or Insomnia for API testing

## Initial Setup

### 1. Clone Repository

```bash
git clone [repository-url]
cd hellobirdie
```

### 2. Backend Setup

#### Python Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Unix
# or
.\venv\Scripts\activate  # Windows
```

#### Dependencies

```bash
pip install -r requirements.txt

# Install development tools
pip install black  # Python formatter
```

#### Database

```bash
# PostgreSQL Setup
psql -U postgres
```

```sql
-- Run these commands in psql
CREATE DATABASE hellobirdie_dev;
CREATE USER hellobirdie_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE hellobirdie_dev TO hellobirdie_user;
```

#### Django Setup

```bash
python manage.py migrate  # Apply database migrations
python manage.py createsuperuser  # Create admin user
```

#### Environment Variables

```bash
cp .env.example .env
```

Required variables in `.env`:

```plaintext
# Database
DB_NAME=hellobirdie_dev
DB_USER=hellobirdie_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# APIs (add keys when obtained)
XENO_CANTO_API_KEY=your_key_here
MAP_TILES_API_KEY=your_key_here  # If using commercial map tiles
GEOLOCATION_API_KEY=your_key_here  # Optional

# Security
DJANGO_SECRET_KEY=generate_a_secure_key
DEBUG=True  # Set to False in production
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
