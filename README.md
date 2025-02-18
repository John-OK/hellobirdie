# HelloBirdie

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)

A web application for visualizing bird locations from the xeno-canto database, with a focus on user privacy and clean code.

## Quick Start

1. Prerequisites:

   - Node.js 20.x
   - Python 3.13
   - PostgreSQL 17
   - Git

2. Installation:

   ```bash
   # Clone the repository
   git clone [repository-url]

   # Backend setup
   cd hellobirdie/backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

   # Frontend setup
   cd ../frontend
   npm install
   ```

3. Configuration:

   - Copy `.env.example` to `.env` in both frontend and backend directories
   - Set up your PostgreSQL database
   - Configure your xeno-canto API credentials

4. Run the application:

   ```bash
   # Backend
   cd backend
   python manage.py runserver

   # Frontend (new terminal)
   cd frontend
   npm run dev
   ```

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

- **Backend**: Python 3.13, Django 5.1, PostgreSQL 17.3
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

<!-- TODO: Review missing items in DOCUMENTATION_TODO.md -->
