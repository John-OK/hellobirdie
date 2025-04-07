# HelloBirdie Documentation

Welcome to the HelloBirdie project documentation. This directory contains comprehensive documentation for all aspects of the project.

## Documentation Map

```
HelloBirdie Documentation
├── project/ - Project-wide documentation
│   ├── architecture/ - System architecture and design
│   ├── development-environment.md - Development tools and environment setup
│   └── docker-guide.md - Docker usage and configuration
│
├── backend/ - Backend-specific documentation
│   ├── setup/ - Backend setup and configuration
│   │   ├── details/ - Step-by-step setup instructions
│   │   ├── guides/ - Supplementary backend guides
│   │   └── concepts/ - Backend concepts and patterns
│   └── api/ - API documentation and endpoints
│
└── frontend/ - Frontend-specific documentation
    └── setup/ - Frontend setup and configuration
```

## Documentation Structure

### Project-Wide Documentation

- **[project/](./project/)** - Documentation that applies to both frontend and backend
  - [architecture/](./project/architecture/) - System architecture and design
  - [development-environment.md](./project/development-environment.md) - Development environment setup
  - [docker-guide.md](./project/docker-guide.md) - Docker usage and configuration

### Component-Specific Documentation

- **[backend/](./backend/)** - Backend-specific documentation

  - [setup/](./backend/setup/) - Backend setup and configuration
    - [hybrid-backend-setup-guide.md](./backend/setup/hybrid-backend-setup-guide.md) - Main backend setup guide
    - [details/](./backend/setup/details/) - Detailed step-by-step instructions
    - [guides/](./backend/setup/guides/) - Supplementary backend guides
    - [concepts/](./backend/setup/concepts/) - Backend concepts and patterns
  - [api/](./backend/api/) - API documentation and endpoints

- **[frontend/](./frontend/)** - Frontend-specific documentation
  - [setup/](./frontend/setup/) - Frontend setup and configuration

## Getting Started

New team members should start with:

1. [Development Environment Setup](./project/development-environment.md) - Set up your development tools
2. [Project Architecture Overview](./project/architecture/system-overview.md) - Understand the system design
3. [Docker Guide](./project/docker-guide.md) - Learn container usage for the project
4. [Backend Setup Guide](./backend/setup/hybrid-backend-setup-guide.md) - Set up the backend
5. [API Endpoints](./backend/api/endpoints.md) - Explore available API endpoints

## Development Principles

HelloBirdie follows these core principles:

1. **Test-Driven Development** - We write tests before implementation
2. **PostgreSQL for all environments** - Consistent database across development, testing, and production
3. **Mobile-first design** - All features are designed for mobile compatibility first
4. **Clean, maintainable code** - Following best practices and design patterns
