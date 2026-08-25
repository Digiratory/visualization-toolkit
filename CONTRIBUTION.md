# Contributing to visualization-toolkit

Thank you for your interest in contributing to visualization-toolkit! This document outlines the guidelines and requirements for contributing.

## Development Setup

1. Fork the repository
2. Clone your fork locally
3. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -e ".[stats]"
```

## Pre-commit Hooks

This project uses [pre-commit](https://pre-commit.com/) to enforce code quality standards. All contributors must install and run pre-commit before submitting changes.

### Installation

```bash
pip install pre-commit
pre-commit install
```

### Running Checks Manually

```bash
pre-commit run --all-files
```

### What Gets Checked

- **black**: Code formatting
- **isort**: Import sorting
- **trailing-whitespace**: Removes trailing whitespace
- **end-of-file-fixer**: Ensures files end with a newline
- **check-yaml**: Validates YAML syntax
- **check-json**: Validates JSON syntax
- **check-added-large-files**: Prevents large files from being committed
- **check-case-conflict**: Detects case-insensitive filename conflicts
- **detect-private-key**: Prevents private keys from being committed

## CI/CD Pipeline

The CI/CD pipeline runs automatically on:

- All pull requests to `master`/`main`
- Pushes to `master`/`main`
- Manual trigger via `workflow_dispatch`

### Pipeline Stages

1. **Pre-commit Validation** (first gate) - Runs all pre-commit hooks
2. **Tests** - Runs pytest across Python 3.10, 3.11, 3.12
3. **Build** - Builds the package wheel

All pre-commit checks must pass before tests and build stages execute. If pre-commit validation fails, downstream jobs will not run.

## Pull Request Guidelines

1. Ensure all pre-commit checks pass locally before pushing
2. Write clear commit messages
3. Update documentation if your changes affect public APIs
4. Ensure tests pass for all supported Python versions

## Code Style

- Follow PEP 8 guidelines (enforced by black)
- Use isort for import ordering (profile: black)
- All code must pass pre-commit checks
