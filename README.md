# HelloBirdie

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.7-blue)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![Backend Coverage](https://img.shields.io/badge/backend_coverage-100%25-brightgreen.svg)](https://github.com/John-OK/hellobirdie/actions)
[![Frontend Coverage](https://img.shields.io/badge/frontend_coverage-100%25-brightgreen.svg)](https://github.com/John-OK/hellobirdie/actions)

A modern, type-safe web application for visualizing bird locations from the xeno-canto database. Built with TypeScript and Python, following Test-Driven Development principles and focusing on code quality and user privacy.

## Quick Start

1. Prerequisites:

   - Docker Desktop 4.38.0 or Docker Engine 28.0.0
   - Docker Compose 2.33.0
   - Node.js 22.14.0 (LTS)
   - Git

   Optional for local development:
   - Node.js 22.x (for frontend development)
   - Python 3.13 (for backend development)
   - PostgreSQL 17 (for database management)

2. Installation:

   ```bash
   # Clone the repository
   git clone https://github.com/John-OK/hellobirdie.git
   cd hellobirdie
   ```

3. Configuration:

   ```bash
   # Copy environment files
   cp .env.example .env
   ```

4. Start the Application:

   ```bash
   # Start backend services (Docker)
   docker-compose up -d

   # Start frontend development server
   cd frontend
   npm install
   npm run dev
   ```

   The application will be available at:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - Admin Interface: http://localhost:8000/admin

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on:

- Code style and standards
- Development workflow
- Testing requirements
- Pull request process

## Documentation

- [Project Architecture](/docs/architecture/system-overview.md)
- [Development Guide](/docs/setup/development-environment.md)
- [API Documentation](/docs/api/endpoints.md)
- [Contributing Guidelines](CONTRIBUTING.md)

## Tech Stack

- **Backend**: Python 3.13, Django 5.1, PostgreSQL 17.4
- **Frontend**: TypeScript 5.7, React 18, Vite 6.1
- **Libraries**: Axios 1.7, Leaflet 1.9, TailwindCSS 4.0
- **Testing**: Pytest, Vitest, React Testing Library

## Team

- [@John-OK](https://github.com/John-OK) - Project Lead & Developer
  - Core development
  - Project maintenance

## License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0) - see the [LICENSE](LICENSE) file for details.

In summary, this license:

- Allows personal use and modification
- Requires sharing of source code for any modifications
- Prevents commercial use without explicit permission
- Requires attribution to the original author

