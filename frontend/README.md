# HelloBirdie Frontend

The frontend for HelloBirdie, built with React and TypeScript following Test-Driven Development principles. This application provides a type-safe, interactive interface for visualizing bird sightings and audio recordings.

## Development Philosophy

### TypeScript-First Approach

We embrace TypeScript's type system to:
- Catch errors at compile time
- Improve code maintainability
- Enable better IDE support
- Document component interfaces

### Test-Driven Development

We follow TDD principles:
1. Write failing test
2. Implement feature
3. Refactor
4. Repeat

## Local Development

The frontend is developed locally (not in Docker) for optimal developer experience:
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

## Development Tools

### TypeScript Configuration

We enforce strict TypeScript settings:
```json
{
  "strict": true,
  "noImplicitAny": true,
  "strictNullChecks": true,
  "noImplicitReturns": true
}
```

### Code Quality

```bash
# Type checking
npm run type-check

# Linting
npm run lint

# Tests
npm run test

# Format
npm run format
```

### Testing Strategy

We use Vitest and follow the Testing Trophy approach:

1. Static Analysis (TypeScript)
2. Unit Tests (Functions/Hooks)
3. Integration Tests (Components)
4. E2E Tests (User Flows)

#### Test File Structure
```typescript
// BirdMap.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { BirdMap } from './BirdMap';
import { MapProvider } from '../context/MapContext';

describe('BirdMap Component', () => {
  const defaultProps = {
    center: { lat: 51.5074, lng: -0.1278 },
    zoom: 13,
    markers: [],
    onMarkerClick: vi.fn()
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders map with correct initial position', () => {
    // Arrange
    const { container } = render(
      <MapProvider>
        <BirdMap {...defaultProps} />
      </MapProvider>
    );

    // Assert
    expect(container.querySelector('.leaflet-container')).toBeInTheDocument();
  });

  it('handles marker clicks correctly', async () => {
    // Arrange
    const markers = [{
      id: '1',
      position: { lat: 51.5074, lng: -0.1278 },
      title: 'Test Bird'
    }];

    render(
      <MapProvider>
        <BirdMap {...defaultProps} markers={markers} />
      </MapProvider>
    );

    // Act
    const marker = await screen.findByTitle('Test Bird');
    fireEvent.click(marker);

    // Assert
    expect(defaultProps.onMarkerClick).toHaveBeenCalledWith('1');
  });
});
```

```bash
# Watch mode
npm run test:watch

# Coverage report
npm run test:coverage
```

## Production Build

```bash
# Build
npm run build

# Preview
npm run preview
```

## Resources

- [TypeScript Guidelines](../docs/typescript)
- [Testing Strategy](../docs/testing)
- [Contributing Guidelines](../CONTRIBUTING.md)
- [Docker Guide](../docs/setup/docker-guide.md)
