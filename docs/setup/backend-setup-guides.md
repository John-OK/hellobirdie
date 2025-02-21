# Backend Setup Guides

These guides outline the process for setting up and extending the HelloBirdie backend, following Test-Driven Development (TDD) principles.

## Basic Setup Guide

### 1. Project Foundation

- Create backend directory structure within existing project
- Update .gitignore with any additional backend-specific patterns if needed
  - Already includes Python, Django, and testing patterns
- Update project README.md with any new backend setup instructions
- Commit Point: "Backend project structure setup"
  > Why: Establishes backend foundation within existing project

### 2. Development Environment Setup

- Create Dockerfile and docker-compose.yml
- Configure PostgreSQL container
- Setup Python environment in container
- Create requirements structure
  - requirements/
    - base.txt
    - local.txt
    - test.txt
- Commit Point: "Backend development environment configuration"
  > Why: Complete environment setup before adding application code

### 3. Django Project Initialization

- Create Django project
- Configure settings structure
  - settings/
    - base.py
    - local.py
    - test.py
- Setup environment variables
  - Add backend-specific variables to existing .env structure
- Configure initial URLs and views
- Commit Point: "Django project initialization"
  > Why: Framework setup complete

### 4. Testing Framework Setup

- Configure pytest with Django settings
- Setup test directory structure following Django conventions
- Create base test classes extending Django test classes
- Write first health check test using Django test client
- Commit Point: "Backend testing framework setup"
  > Why: Establishes TDD foundation with proper Django integration

### 5. Database Configuration

- Configure PostgreSQL connection
- Create initial migrations
- Add health check endpoint (implementing the test from previous step)
- Run and verify tests
- Commit Point: "Database configuration and health check"
  > Why: Verifies complete working environment

## Feature Setup Guide

### 1. API Structure Setup

- Create API app
- Configure DRF
- Setup API test structure
- Create base test classes
- Commit Point: "API foundation setup"
  > Why: Framework for feature development

### 2. Authentication Setup

- Write authentication tests
- Implement authentication
- Configure JWT
- Commit Point: "Authentication implementation"
  > Why: Core security feature complete

### 3. Bird Data Models

- Write model tests
- Create bird-related models
- Setup model validation
- Commit Point: "Bird data models"
  > Why: Core data structure defined

### 4. API Endpoints

- Write endpoint tests
- Implement CRUD endpoints
- Add validation
- Configure serializers
- Commit Point: "API endpoints implementation"
  > Why: Core functionality complete

### 5. Integration Tests

- Write integration tests
- Setup test data fixtures
- Configure API documentation
- Commit Point: "Integration tests and documentation"
  > Why: Ensures system works as a whole
