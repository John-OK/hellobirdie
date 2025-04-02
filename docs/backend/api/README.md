# HelloBirdie API Documentation

This directory contains documentation for the HelloBirdie API endpoints and integration details.

## Contents

- [endpoints.md](./endpoints.md) - API endpoint specifications

## API Overview

The HelloBirdie API provides:

- Bird sighting data retrieval
- Location-based filtering
- Integration with xeno-canto for bird call recordings
- Health check monitoring

## Authentication

The API uses token-based authentication for protected endpoints. Authentication details will be expanded as the authentication system is implemented.

## Response Format

All API responses follow a consistent JSON format:

```json
{
  "data": {}, // Response data
  "meta": {}, // Metadata (pagination, etc.)
  "errors": [] // Error details if applicable
}
```

## Error Handling

The API uses standard HTTP status codes and provides detailed error messages in the response body when errors occur.
