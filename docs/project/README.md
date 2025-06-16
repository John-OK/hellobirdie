# HelloBirdie Project Documentation

This directory contains project-wide documentation that applies to both frontend and backend components.

## Contents

- **[architecture/](./architecture/)** - System architecture and design

  - [system-overview.md](./architecture/system-overview.md) - High-level system architecture
  - Component interactions
  - Data flow diagrams
  - Technology decisions

- **[development-environment.md](./development-environment.md)** - Development environment setup for both frontend and backend

  - Required software and tools
  - IDE configuration
  - Local development setup

- **[hybrid_workflow_guide.md](./hybrid_workflow_guide.md)** - Our hybrid development workflow

  - Local development approach (primary)
  - Docker verification approach (secondary)
  - Environment consistency guidelines
  - Workflow best practices

- **[docker-guide.md](./docker-guide.md)** - Comprehensive Docker usage and configuration
  - Container architecture
  - Docker verification workflow
  - Troubleshooting

## Navigation

- [← Documentation Home](../README.md)
- [Backend Documentation](../backend/README.md)
- [Frontend Documentation](../frontend/README.md)

## Project Overview

HelloBirdie is a mobile-friendly web application for birders to visualize and interact with bird sighting data from the xeno-canto API. The application follows:

- Test-Driven Development methodology
- Clean, maintainable code principles
- Security by design
- Accessibility compliance

## Development Workflow

The project follows a Git workflow with:

- Feature branches for new functionality
- Pull request reviews
- Comprehensive testing before merging
- Continuous integration

See the [system overview](./architecture/system-overview.md) for more details on the overall architecture.
