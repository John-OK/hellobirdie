# Git Workflow Best Practices

This guide outlines the recommended workflow for contributing to the HelloBirdie project using Git and GitHub.

## Standard Workflow

### 1. Start with a Clean Workspace

Before making changes, check the status of your repository:

```bash
git status
```

This shows which files have been modified, staged, or are untracked.

### 2. Get the Latest Changes

Fetch and integrate changes from the remote repository:

```bash
# Fetch latest branch information
git fetch

# Pull latest changes (fetch + merge)
git pull origin main
```

> **Note:** If you're working on a feature branch, replace `main` with your branch name.

### 3. Create/Switch to a Feature Branch (Optional)

For new features or significant changes, create a dedicated branch:

```bash
# Create and switch to a new branch
git checkout -b feature/health-check-endpoint

# Or switch to an existing branch
git checkout feature/health-check-endpoint
```

### 4. Review Your Changes

Before committing, review what you're about to commit:

```bash
# Show changes between working directory and staging area
git diff

# If files are already staged
git diff --staged
```

### 5. Stage Your Changes

Add files to the staging area:

```bash
# Stage specific files
git add backend/api/views.py backend/api/urls.py

# Stage all modified files (use with caution)
git add .
```

### 6. Commit Your Changes

Create a well-structured commit with a descriptive message:

```bash
git commit -m "feature: Implement health check endpoint using TDD

- Add health_check view in api/views.py returning JSON response
- Configure URL routing in api/urls.py and include in project URLs
- Add test to verify endpoint returns correct JSON response"
```

> **Best Practice:** Write commit messages in the imperative mood ("Add feature" not "Added feature")

### 7. Push Your Changes

Send your changes to the remote repository:

```bash
# If working on main branch
git push origin main

# If working on a feature branch
git push origin feature/health-check-endpoint
```

### 8. Create a Pull Request (When Appropriate)

For collaborative projects, create a pull request through GitHub's web interface.

## Branch Naming Conventions

According to the project documentation, use the following format:

```
type/description
```

Types:

- `feature/` - New functionality
- `fix/` - Bug fixes
- `refactor/` - Code improvements
- `test/` - Test additions/modifications
- `docs/` - Documentation updates

Examples:

- `feature/add-map-clustering`
- `fix/audio-playback-mobile`

## Commit Message Guidelines

1. Start with a type prefix matching branch naming convention (e.g., `feature:`, `fix:`, `refactor:`, `docs:`, `test:`) 
2. Use a concise subject line (50 characters or less)
3. Separate subject from body with a blank line
4. Use imperative mood in the subject line
5. Include details in the commit body as bullet points
6. Reference issue numbers when applicable

## Example Commit for Current Changes

```bash
git add backend/api/tests/test_health.py backend/api/urls.py backend/api/views.py backend/hellobirdie/urls.py

git commit -m "feature: Implement health check endpoint using TDD

- Add health_check view in api/views.py returning JSON response
- Configure URL routing in api/urls.py and include in project URLs
- Add test to verify endpoint returns correct JSON response"

git push origin main
```

## Handling Merge Conflicts

If you encounter merge conflicts:

1. Run `git status` to see which files have conflicts
2. Open each conflicted file and resolve the conflicts
3. After resolving, stage the fixed files: `git add <filename>`
4. Complete the merge: `git commit`

## Pre-Commit Checklist

Before finalizing a commit:

- [ ] Tests pass (`docker compose exec backend python manage.py test api.tests.<test_module>`)
  - Example: `docker compose exec backend python manage.py test api.tests.test_health`
- [ ] Code follows project style guidelines
- [ ] No debugging code or print statements left in
- [ ] Documentation is updated if needed
- [ ] Changes are isolated to the feature being implemented
