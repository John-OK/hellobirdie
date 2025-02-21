# HelloBirdie Frontend

The frontend for HelloBirdie, built with React, TypeScript, and Vite. This application provides an interactive interface for visualizing bird sightings and audio recordings.

## Development

The frontend is developed locally (not in Docker) to provide the best development experience with features like:
- Fast hot reloading
- Quick feedback cycles
- Efficient debugging
- IDE integration

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

> Note: For production deployment information, see the [Docker Guide](../docs/setup/docker-guide.md)

## Development Tools

### Code Quality

We use several tools to maintain code quality:

```bash
# Run type checking
npm run type-check

# Run linting
npm run lint

# Run tests
npm run test

# Format code
npm run format
```

### Testing

We use Vitest for testing. Write tests in the `__tests__` directory next to the component being tested.

```bash
# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
```

## Building for Production

```bash
# Build production assets
npm run build

# Preview production build
npm run preview
```

## Additional Resources

- [Project Documentation](../docs)
- [Contributing Guidelines](../CONTRIBUTING.md)
- [Docker Guide](../docs/setup/docker-guide.md)
