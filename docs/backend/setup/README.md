# HelloBirdie Backend Setup Documentation

## For New Team Members

If you're new to the project, you likely won't need to follow the entire setup process from scratch. Instead:

1. Clone the existing repository
2. Follow the [Development Environment Setup](../../project/development-environment.md) guide
3. Use these documents as a reference to understand the backend architecture

## Purpose of This Documentation

This directory contains documentation that serves as:

- A historical record of how the backend was built
- A reference for understanding the backend architecture
- A guide for rebuilding the backend if necessary
- A learning resource for Django and TDD practices

## Contents

- [hybrid-backend-setup-guide.md](./hybrid-backend-setup-guide.md) - The main step-by-step guide for setting up the backend
- [tdd-testing-strategy.md](./tdd-testing-strategy.md) - Our approach to Test-Driven Development

- **[details/](./details/)** - Detailed implementation guides for each setup step

  - [step1-project-structure-setup.md](./details/step1-project-structure-setup.md) - Initial project structure
  - [step2-environment-configuration.md](./details/step2-environment-configuration.md) - Environment variables and configuration
  - [step3-django-project-initialization.md](./details/step3-django-project-initialization.md) - Django setup
  - [step4-implementing-first-feature.md](./details/step4-implementing-first-feature.md) - First feature with TDD
  - [step5-settings-structure-refactoring.md](./details/step5-settings-structure-refactoring.md) - Settings refactoring
  - [step6-database-configuration.md](./details/step6-database-configuration.md) - Database setup

- **[concepts/](./concepts/)** - Conceptual documentation explaining our development approach

- **[guides/](./guides/)** - Additional guides for specific tools and workflows
  - [feature-setup-guide.md](./guides/feature-setup-guide.md) - Process for implementing new features following TDD

## Navigation

- [← Backend Documentation](../README.md)
- [Project-Wide Documentation](../../project/README.md)
- [Documentation Home](../../README.md)

## Development Philosophy

HelloBirdie follows these core principles:

1. **Test-Driven Development** - We write tests before implementation
2. **PostgreSQL for all environments** - Consistent database across development, testing, and production
3. **Hybrid development approach** - Local-first development and testing, with Docker-based verification
4. **Mobile-first design** - All features are designed for mobile compatibility first

## Need Help?

If you encounter any issues during setup:

1. Check the troubleshooting section in the [Hybrid Backend Setup Guide](./hybrid-backend-setup-guide.md)
2. Review the detailed guide for the specific step you're working on
3. Reach out to the team for assistance
