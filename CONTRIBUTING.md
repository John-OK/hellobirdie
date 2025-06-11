# Contributing to HelloBirdie

## Development Workflow

### Branch Naming Convention

- Format: `type/description`
- Types:
  - `feature/` - New functionality
  - `fix/` - Bug fixes
  - `refactor/` - Code improvements
  - `test/` - Test additions/modifications
  - `docs/` - Documentation updates
- Examples:
  - `feature/add-map-clustering`
  - `fix/audio-playback-mobile`

### Pull Request Process

1. Create a feature branch from `main`
2. Implement changes with appropriate tests
3. Run the local test suite
4. Create a pull request using the PR template
5. Address review feedback
6. Merge after approval

### Development Environment

We use Docker for development to ensure consistency:

```bash
# Start the development environment
docker compose up -d

# Run tests
docker compose exec backend pytest

# Format code
docker compose exec backend black .
docker compose exec backend isort .
```

See our [Docker Guide](docs/setup/docker-guide.md) for detailed instructions.

### Code Review Guidelines

1. Testing:

   - Tests must be written first (TDD)
   - All tests must pass
   - Coverage must be maintained
   - Integration tests for API endpoints

2. Code Quality:

   - Follow project style guide
   - Documentation must be updated
   - No security vulnerabilities
   - Mobile-friendly implementation
   - Proper error handling
   - Performance considerations

3. Docker:
   - Changes to Dockerfile or docker-compose.yml must be documented
   - Container builds must succeed
   - New dependencies must be properly versioned

## Code Standards

### General Principles

- Privacy and user respect are paramount
- Test-driven development (TDD)
  - Write tests before implementation
  - Use pytest for backend testing
  - Maintain test coverage
- Clean, maintainable code
  - Follow SOLID principles
  - Use type hints in Python
  - Document complex logic
- Security by design
  - Follow security best practices
  - Validate all inputs
  - Use environment variables for secrets
- Mobile-first approach
  - Responsive design
  - Touch-friendly interfaces
- Docker-based development
  - Use containers for consistency
  - Document container changes
  - Follow Docker best practices

### IDE Configuration

When documenting IDE extensions or tools:

- Always include the unique extension ID (e.g., `dbaeumer.vscode-eslint`)
- Specify minimum required versions if applicable
- Note any required extension configuration

Example:

```json
{
  "recommendations": [
    "dbaeumer.vscode-eslint", // ESLint
    "esbenp.prettier-vscode", // Prettier
    "ms-python.python" // Python
  ]
}
```

This ensures consistent development environments across the team and avoids confusion with similarly named extensions.

### Code Quality Standards

- Maximum function length: 20 lines
- Follow Single Responsibility Principle
- Use pure functions when possible
- Implement early returns for guard clauses

### Testing Requirements

- Unit tests for all new features
- Integration tests for component interactions
- E2E tests for critical user flows
- Maintain or improve code coverage
- Test error scenarios and edge cases

### Testing Tools

#### Current (MVP)

- **Backend**: pytest + pytest-django with factory_boy
- **Frontend**:
  - Vitest + React Testing Library for component testing
  - axios-mock-adapter for API mocking

#### Future Enhancements

- End-to-end testing
- Component development tools
- Accessibility testing
- Enhanced API mocking solutions

### SOLID Principles

1. **Single Responsibility**: Classes and functions should do one thing well

   - Example: Separate data fetching from rendering

2. **Open/Closed**: Open for extension, closed for modification

   - Example: Use strategy pattern for different map providers

3. **Liskov Substitution**: Subtypes must be substitutable for base types

   - Example: All bird markers must work like base markers

4. **Interface Segregation**: Many specific interfaces over one general

   - Example: Split IMapProps into IMapView and IMapControls

5. **Dependency Inversion**: Depend on abstractions, not implementations
   - Example: Use service interfaces over concrete implementations

### Logging Standards

Use the following format for all logging:

```json
{
  "timestamp": "ISO-8601 (e.g., 2025-02-14T13:44:21+01:00)",
  "level": "ERROR|WARNING|INFO|DEBUG",
  "service": "api|web|db",
  "message": "Human-readable message",
  "context": {
    "user_id": "anonymous",
    "action": "action_name",
    "details": {}
  }
}
```

> Note: The timestamp follows ISO-8601 format where:
>
> - `YYYY-MM-DD`: Date (year-month-day)
> - `T`: Time separator
> - `HH:mm:ss`: Time (hours:minutes:seconds)
> - `+/-xx:xx`: Timezone offset from UTC

#### Logging Levels

- **ERROR**: Application failures (API errors, DB issues)
- **WARNING**: Unexpected but handled issues
- **INFO**: Important operations (API calls, user actions)
- **DEBUG**: Development details

## Development Setup

See [Development Environment Setup](/docs/setup/development-environment.md) for detailed instructions.

## Code of Conduct

This project follows the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) Code of Conduct. By participating, you are expected to:

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

## Team Communication

### Platforms

- **Primary**: GitHub Issues and Pull Requests
- **Discussions**: GitHub Discussions for feature requests and community engagement

### Communication Guidelines

- **Hours**: 0800-2200 UTC
- **Response Time**:
  - Issues: Within 48 hours
  - Pull Requests: Within 72 hours
  - Discussions: Within 1 week

## Release Process

### Version Control

We use semantic versioning (MAJOR.MINOR.PATCH):

- MAJOR: Breaking changes
- MINOR: New features, backward compatible
- PATCH: Bug fixes, backward compatible

### Branching Strategy

We use a simplified Git flow:

- `main`: Production-ready code
- `develop`: Integration branch for features
- Feature branches: `feature/description`
- Bug fix branches: `fix/description`

### Release Schedule

- Regular releases every 2-4 weeks
- Patch releases as needed for critical bugs
- Version numbers tracked in CHANGELOG.md

### Release Steps

1. Update CHANGELOG.md
2. Update version numbers
3. Create release branch
4. Test thoroughly
5. Merge to main
6. Tag release

## Team Responsibilities

### Code Review

- Review PRs within 72 hours
- Focus on:
  - Code quality
  - Test coverage
  - Documentation updates
  - Security implications

### Documentation

- Update docs with code changes
- Required documentation:
  - Function/component descriptions
  - API changes
  - New feature guides
  - Breaking changes
- Optional but encouraged:
  - Code examples
  - Troubleshooting guides
  - Performance considerations

## Questions or Problems?

1. Check existing [GitHub Issues](https://github.com/John-OK/hellobirdie/issues)
2. Review [Documentation](/docs)
3. Open a new issue with:
   - Clear description
   - Steps to reproduce (if bug)
   - Expected vs actual behavior

<!-- TODO: Review missing items in DOCUMENTATION_TODO.md -->
