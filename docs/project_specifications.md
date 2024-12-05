# HelloBirdie Project Specification

## Project Overview
A web application for visualizing bird locations from the xeno-canto database, with a focus on user privacy and clean code.

## Application Type
- Primary: Web Application
- Future: Mobile Application (later iteration)

## Core Functionality (MVP)

### Map Features
- Center map on user's current location (with permission)
- Display 50km radius circle around center point
- Map Navigation:
  - Primary interaction through drag/pan
  - Search bar with autocomplete for location search
  - "Center on Me" button for returning to user's location
  - Optional: Double-click to zoom in
  - Optional: Shift+drag to zoom to area
  - Map controls:
    - Zoom in/out buttons
    - Compass/rotation reset
    - Full screen toggle
    - Scale indicator

### Bird Data Integration
- Data Source: xeno-canto API (v2)
  - Endpoint: https://xeno-canto.org/api/2/recordings
  - Response caching to respect API limits
  - Error handling for API failures
- Search Parameters:
  - Species (optional)
  - Geographic coordinates
  - Implicit 50km radius filter

### Display Features
- Bird location markers on map
  - Different colors/shapes for different species
  - Marker clustering for high-density areas
  - Cluster expansion on click
- Bird Information Modal
  - Common name
  - Scientific name (Genus species subspecies)
  - Recording date
  - Recording type
  - Quality rating
  - Audio playback functionality

## Technical Stack

### Backend
- Python
- Django
- Django REST Framework
- PostgreSQL (for caching and future features)
- NOTE: Directory for backend: hellobirdie/backend
- NOTE: Always use latest versions of packages if possible. Use version numbers when necessary, but do not use "@latest."

### Frontend
- TypeScript
- React
- Vite
- Axios for API calls
- TailwindCSS
- Leaflet for mapping
- HTML/CSS
- NOTE: Directory for frontend: hellobirdie/frontend
- NOTE: Always use latest versions of packages if possible. Use version numbers when necessary, but do not use "@latest."

### Testing Frameworks

#### Backend Testing
- Primary: Pytest
  - pytest-django for Django integration
  - pytest-cov for code coverage
  - factory_boy for test data generation
  - pytest-mock for mocking

#### Frontend Testing
- Primary: Vitest
  - Better TypeScript support and Vite integration
  - Compatible with Jest API
- React Testing Library
  - Component testing focused on user behavior
- Mock Service Worker (MSW)
  - API mocking for integration tests

#### E2E Testing
- Cypress
  - Modern, developer-friendly E2E testing
  - Includes time-travel debugging
  - Built-in wait mechanisms

#### Additional Testing Tools
- Storybook
  - Component development and documentation
- Testing Library User Event
  - Enhanced user interaction simulation
- axe-core
  - Accessibility testing integration

#### Testing Tool Notes
- All recommended testing tools are open-source and free for personal use
- Cypress offers both free open-source and paid versions
  - Free version includes all core features needed for this project
  - Paid features (Dashboard Service, etc.) not required
- Storybook is free and open-source
  - Optional paid addons available but not needed

## Development Environment
- OS: Linux
- IDE: Windsurf (VSCode fork)
- Version Control: Git
- Requires professional-grade setup for team development

## Essential Professional Features (MVP)

### Error Handling
- Graceful API failure handling
- User-friendly error messages
- Detailed development logs

### Performance
- API response caching
- Efficient marker rendering
- Map tile optimization
- Lazy loading of audio files

### Security
- No user data collection
- Secure API integration
- Input sanitization
- Rate limiting implementation

### Accessibility
- Semantic HTML
- Keyboard navigation
- Screen reader compatibility
- ARIA labels

## Future Iterations
See detailed roadmap in `/docs/project_roadmap.md`