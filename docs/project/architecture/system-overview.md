# HelloBirdie System Overview

## System Purpose

HelloBirdie is a web application that visualizes bird sighting data from the xeno-canto API, focusing on:

- Location-based bird sighting visualization
- Audio playback of bird calls
- Mobile-friendly interface
- User privacy

## Architecture Overview

### Frontend

- React 18 + TypeScript 5.7
- Vite 6.1 for build tooling
- Key libraries:
  - Leaflet: Map visualization
  - Axios: API communication
  - TailwindCSS: Styling

### Backend

- Django 5.1 + Python 3.13
- PostgreSQL 17
- Hybrid development approach:
  - Local development with virtual environments (primary)
  - Docker for verification and CI/CD (secondary)
- Key features:
  - REST API endpoints
  - xeno-canto API integration
  - Data caching
  - Health check monitoring

### Testing Infrastructure

- pytest for Python testing
  - Unit tests
  - Integration tests
  - API tests
- Django test client
- Factory Boy for test data
- Coverage reporting

## Core Components

### Map Interface

- Displays bird sightings within 50km radius
- Marker clustering for performance
- Basic map controls (zoom, fullscreen)

### Bird Data Display

- Species information
- Recording details
- Audio playback interface

### System Architecture and Data Flow

The application follows a containerized client-server architecture with external service integration:

```
[Frontend Container] <-> [Backend Container] <-> [xeno-canto API]
                         [Database Container]
   ^                ^              ^
   |                |              |
[Map Data]    [PostgreSQL DB]   [Audio Files]
```

This diagram shows:

1. **Frontend to Backend**: React frontend communicates with Django backend via REST API
2. **Backend to xeno-canto**: Backend fetches bird data and audio from xeno-canto API
3. **Data Storage**:
   - Map data is cached in the frontend for performance
   - Bird data is stored in PostgreSQL for quick access
   - Audio files are streamed from xeno-canto

> Note: This is a simplified view. A full network architecture diagram would include additional details like load balancers, CDNs, and specific protocols, which will be added when we move to production deployment.

## Security Considerations

- User location privacy
  - Optional location sharing
  - No permanent storage of user locations
- API security
  - Rate limiting
  - Request validation
- Data protection
  - Secure headers
  - CORS configuration

## Performance Considerations

- Map optimization
  - Marker clustering for dense areas
  - Lazy loading of distant markers
- Audio handling
  - Progressive loading for audio files
  - Caching of frequently accessed recordings
- API efficiency
  - Response caching
  - Pagination for large datasets
- Frontend optimization
  - Code splitting
  - Component lazy loading

## Development Approach

### Phase 1 (MVP)

- Basic map integration
- Location-based bird sighting display
- Simple audio playback
- Essential data caching

### Future Considerations

- User accounts and preferences
- Offline support
- Advanced search filters
- Social features (sharing, comments)
- Mobile app potential

## Related Documentation

- [Development Environment Setup](/docs/backend/setup/guides/development-environment.md)
- [Contributing Guidelines](/CONTRIBUTING.md)

> Note: This overview will evolve as the project develops. Key decisions and architectural changes will be documented here.
