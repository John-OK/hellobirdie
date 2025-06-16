# Feature Development Guide

This guide builds upon the backend setup and provides detailed steps for implementing new features in HelloBirdie following TDD principles.

## Feature Development Workflow

### 1. Planning Phase

- Define feature requirements and acceptance criteria
- Break down into testable units
- Create test plan document
- Create feature branch following naming convention
  > Example: `feature/bird-location-tracking`

### 2. Test Implementation

- Write unit tests for models
- Write unit tests for services
- Write integration tests for API endpoints
- Write end-to-end tests if applicable
- Document test coverage expectations

### 3. Feature Implementation

- Implement models and migrations
- Add service layer logic
- Create API endpoints
- Add validation and error handling
- Document API endpoints using OpenAPI/Swagger

### 4. Code Review Preparation

- Run test suite in local environment first
- Verify all tests also pass in Docker environment

  ```bash
  # Local verification
  source .venv/bin/activate
  cd backend
  python manage.py test api.tests

  # Docker verification
  docker compose up -d
  docker compose exec backend python manage.py test api.tests
  docker compose down
  ```

- Update documentation
- Check code against style guide
- Verify mobile responsiveness
- Complete PR template

### 5. Deployment Considerations

- Update environment variables if needed
- Add feature flags if required
- Document rollback procedures
- Update monitoring and logging
- Plan staged rollout if necessary

## Example: Adding Bird Location Feature

### 1. Test First

```python
def test_bird_location_creation():
    # Given
    location_data = {
        "latitude": 51.5074,
        "longitude": -0.1278,
        "accuracy": 10.0
    }

    # When
    response = client.post("/api/bird-locations/", location_data)

    # Then
    assert response.status_code == 201
    assert "id" in response.json()
```

### 2. Implementation

- Create BirdLocation model
- Add LocationService for business logic
- Implement API endpoint
- Add validation
- Update documentation

### 3. Quality Checks

- Run performance tests
- Check error handling
- Verify logging
- Test edge cases
- Review security implications

## Best Practices Reminder

- Write tests before implementation
- Keep functions small and focused
- Document API changes
- Use type hints consistently
- Follow error handling patterns
- Maintain test coverage

## Common Pitfalls

- Skipping test coverage
- Insufficient error handling
- Missing documentation
- Tight coupling
- Inadequate validation
