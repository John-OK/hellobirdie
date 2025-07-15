# Frontend Setup Guide

This directory will contain documentation for setting up and configuring the HelloBirdie frontend.

## Coming Soon

The frontend setup documentation will be developed as the frontend implementation progresses. It will include:

- Development environment setup
- Package management
- Build and deployment processes
- Testing strategy

## Technology Stack

- nvm 0.40.1
- Node.js 22.14.0 (LTS)
- TypeScript 5.7.3
- React 18.3
- Vite 6.1.0
- Axios 1.7.9
- TailwindCSS 4.0.6
- Leaflet 1.9.4

## Node.js Setup

We recommend using nvm (Node Version Manager) to install and manage Node.js versions:

```bash
# Install nvm 0.40.1 (if not already installed)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash

# Reload shell configuration
source ~/.bashrc  # or source ~/.zshrc if using zsh

# Install the required Node.js version
nvm install 22.14.0

# Set as default version for the project
nvm use 22.14.0

# Verify versions
node -v  # Should output v22.14.0
npm -v   # Should output the corresponding npm version
```

## Development Principles

The frontend development will follow these principles:

1. **Component-Based Architecture**

   - Reusable UI components
   - Clear separation of concerns

2. **Type Safety**

   - TypeScript for all code
   - Strict type checking

3. **Testing**

   - Unit tests for components
   - Integration tests for workflows

4. **Performance**
   - Code splitting
   - Lazy loading
   - Optimized bundle size
