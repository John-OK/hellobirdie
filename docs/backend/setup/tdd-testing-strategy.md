# TDD Testing Strategy for HelloBirdie

## Test-Driven Development Overview

Test-Driven Development (TDD) follows a cycle:

1. **Red**: Write a failing test
2. **Green**: Write minimal code to make the test pass
3. **Refactor**: Improve the code while keeping tests passing

## Testing Tools

For HelloBirdie, we're using:

- **pytest**: Modern testing framework
- **pytest-django**: Django-specific pytest extensions
- **factory_boy**: Test data generation
- **pytest-cov**: Test coverage reporting

## Test Types and Organization

### Unit Tests

- Test individual components in isolation
- Fast execution (milliseconds)
- Located close to implementation code
- Example: Testing a single model method

### Integration Tests

- Test interactions between components
- Medium execution time
- Located in dedicated test modules
- Example: Testing API endpoints with database

### End-to-End Tests

- Test complete user flows
- Slower execution
- Located in dedicated test directories
- Example: Testing a complete bird sighting submission

## Directory Structure

```
backend/
├── api/
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   ├── test_views.py
│   │   ├── test_serializers.py
│   │   └── factories.py
│   ├── models.py
│   ├── views.py
│   └── serializers.py
```

## Hybrid TDD Workflow

We employ a hybrid TDD approach with both local and Docker environments to maximize development speed and reliability.

### Local Development (Primary)

#### Benefits

- **Faster Feedback**: Quick test runs without Docker overhead
- **Simplified Debugging**: Direct access to Python debuggers
- **Enhanced TDD Flow**: Red-Green-Refactor cycle speed increased

#### Workflow

```bash
# Make sure your virtual environment is activated
source .venv/bin/activate

# Run all tests with pytest (from backend directory)
cd backend
python -m pytest

# Run specific tests with clear module paths
python manage.py test api.tests.test_models

# Run with coverage
python -m pytest --cov=api
```

### Docker Verification (Secondary)

#### Benefits

- **Consistent Environment**: Verifies tests work the same for all developers
- **Service Integration**: Validates database interactions
- **CI/CD Ready**: Tests in Docker match CI environment

#### Workflow

```bash
# Start all services
docker compose up -d

# Run all tests in Docker
docker compose exec backend pytest

# Run specific tests with explicit module paths
docker compose exec backend python manage.py test api.tests.test_models

# Run with coverage
docker compose exec backend pytest --cov=api
```

> **Note:** For Docker Compose V1 (older versions), use `docker-compose` instead of `docker compose`. The project requires Docker Compose 2.33.0 or newer, which uses the V2 syntax without the hyphen.

## Split Settings and TDD

The test.py settings file provides several TDD benefits:

1. **Reliability**:

   - Uses dedicated PostgreSQL test database
   - Simpler password hashing
   - Disabled non-essential middleware

2. **Isolation**:

   - Separate test database
   - Disabled caching
   - Controlled environment variables

3. **Reproducibility**:
   - Same settings for all developers
   - Consistent test behavior

## TDD Best Practices for HelloBirdie

### 1. Test Naming

Use descriptive test names that explain the behavior:

```python
def test_bird_sighting_within_radius_is_included_in_results():
    # Test code
```

### 2. Test Organization

Group tests by feature and behavior:

```python
class TestBirdSightingFiltering:
    def test_filter_by_species(self):
        # Test code

    def test_filter_by_date_range(self):
        # Test code
```

### 3. Test Data

Use factories for consistent test data:

```python
# In factories.py
class BirdSightingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BirdSighting

    species = "Common Blackbird"
    latitude = 52.5200
    longitude = 13.4050

# In tests
def test_filter_by_species():
    BirdSightingFactory(species="Common Blackbird")
    BirdSightingFactory(species="European Robin")

    response = client.get("/api/sightings/?species=Robin")
    assert len(response.data) == 1
```

### 4. Test Coverage Goals

- **Models**: 100% coverage
- **Serializers**: 100% coverage
- **Views**: 90%+ coverage
- **Overall**: 85%+ coverage

## TDD Learning Path

1. **Start Simple**: Begin with model tests
2. **Build Up**: Move to serializer tests
3. **Add Complexity**: Implement view and API tests
4. **Refine**: Add edge cases and error handling tests

## Common TDD Pitfalls to Avoid

1. **Testing Implementation**: Test behavior, not implementation details
2. **Brittle Tests**: Avoid tests that break with minor changes
3. **Test Duplication**: Don't repeat the same test logic
4. **Slow Tests**: Keep tests fast to maintain development flow
