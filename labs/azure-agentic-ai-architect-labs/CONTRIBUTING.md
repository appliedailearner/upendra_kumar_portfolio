# Contributing to Azure Agentic AI Architect Labs

Thank you for your interest in contributing! This document outlines the process and guidelines for contributing to this project.

## Code of Conduct

Be respectful, inclusive, and professional. All contributors are expected to abide by our community standards.

## Getting Started

### Prerequisites
- Git and GitHub account
- Azure subscription (for testing)
- Python 3.9+
- Terraform 1.5+
- Azure CLI

### Development Setup

```bash
git clone https://github.com/appliedailearner/azure-agentic-ai-architect-labs.git
cd azure-agentic-ai-architect-labs

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install development dependencies
cd 09-end-to-end-reference-implementation
pip install -r requirements.txt
```

## How to Contribute

### 1. Fork and Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Code Guidelines

- **Python**: Follow PEP 8 standards
- **Naming**: Use clear, descriptive names
- **Documentation**: Update README and docstrings
- **Testing**: Add tests for new features
- **Formatting**: Use Black for code formatting

### 3. Pre-commit Checks

Before committing, run:

```bash
# Format code
black app/

# Lint
ruff check app/

# Type checking
mypy app/ --ignore-missing-imports

# Tests
pytest app/tests/ -v
```

### 4. Commit Messages

Use conventional commits format:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `refactor:` Code refactoring
- `ci:` CI/CD changes
- `chore:` Maintenance

Example: `feat: Add user authentication to agent`

### 5. Pull Request

- Create PR with clear description
- Reference related issues
- Ensure all CI checks pass
- Request review from maintainers

## Module Development

### Adding a New Module

1. Create directory: `0X-module-name/`
2. Add README.md with:
   - Learning objectives
   - Prerequisites
   - Architecture diagram
   - Step-by-step instructions
   - Key concepts

3. Include example code
4. Update main README with module link

## Infrastructure Changes

### Terraform

- Validate: `terraform validate`
- Format: `terraform fmt -recursive`
- Plan: `terraform plan`

## Testing

### Unit Tests
```bash
pytest app/tests/test_agent.py -v
```

### Integration Tests
```bash
pytest app/tests/test_integration.py -v
```

### Coverage
```bash
pytest --cov=app --cov-report=html
```

## Documentation

- Update relevant READMEs
- Add docstrings to functions
- Include examples
- Keep DEPLOYMENT-GUIDE updated

## Release Process

1. Update version in documentation
2. Create release notes
3. Tag release: `v1.0.0`
4. Create GitHub Release

## Questions?

Open an issue or contact the maintainers. We're here to help!

## License

Contributions are licensed under the MIT License.
