# Contributing to Django REST API with PyMongo

First off, thank you for considering contributing to this project! It's people like you that make this project better for everyone.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [How to Contribute](#how-to-contribute)
4. [Development Setup](#development-setup)
5. [Coding Standards](#coding-standards)
6. [Testing Guidelines](#testing-guidelines)
7. [Pull Request Process](#pull-request-process)
8. [Reporting Bugs](#reporting-bugs)
9. [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to:

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

- Python 3.8 or higher
- MongoDB (local or cloud)
- Git
- Basic understanding of Django and REST APIs

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/django-rest-framework-drf.git
   cd django-rest-framework-drf
   ```

3. Add upstream remote:
   ```bash
   git remote add upstream https://github.com/shivraj-prajapati/django-rest-framework-drf.git
   ```

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

1. **Bug Fixes**: Fix issues in existing code
2. **New Features**: Add new functionality
3. **Documentation**: Improve or add documentation
4. **Tests**: Add or improve test coverage
5. **Performance**: Optimize existing code
6. **Code Quality**: Refactor or improve code quality

### First Time Contributors

Look for issues labeled `good first issue` or `help wanted` to get started.

## Development Setup

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure MongoDB:**
   - Copy `.env.example` to `.env`
   - Update MongoDB connection settings
   
4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Run tests:**
   ```bash
   python manage.py test
   ```

## Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

- **Line length**: 100 characters (not 79)
- **Indentation**: 4 spaces
- **Imports**: Group by standard library, third-party, and local
- **Docstrings**: Use Google style docstrings

Example:
```python
def create_product(name, price, quantity):
    """
    Create a new product in MongoDB.
    
    Args:
        name (str): Product name
        price (float): Product price
        quantity (int): Product quantity
        
    Returns:
        dict: Created product document
        
    Raises:
        ValueError: If price is negative
    """
    if price < 0:
        raise ValueError("Price must be positive")
    
    # Implementation here
    pass
```

### Code Formatting

We recommend using:
- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting

Install these tools:
```bash
pip install black isort flake8
```

Format your code before committing:
```bash
black .
isort .
flake8 .
```

### Naming Conventions

- **Variables/Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private methods**: `_leading_underscore`

### Comments and Documentation

- Write clear, concise comments
- Document all public functions and classes
- Update documentation when changing functionality
- Include examples in docstrings when helpful

## Testing Guidelines

### Writing Tests

1. **Location**: Place tests in `products/tests.py` or create test files like `test_views.py`
2. **Naming**: Test methods should start with `test_`
3. **Coverage**: Aim for >80% code coverage

### Test Structure

```python
class ProductAPITestCase(APITestCase):
    """Test case for Product API."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create test data
        pass
    
    def tearDown(self):
        """Clean up after tests."""
        # Remove test data
        pass
    
    def test_create_product(self):
        """Test creating a product."""
        # Given
        data = {...}
        
        # When
        response = self.client.post('/api/products/', data)
        
        # Then
        self.assertEqual(response.status_code, 201)
```

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test file
python manage.py test products.tests

# Run specific test class
python manage.py test products.tests.ProductAPITestCase

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## Pull Request Process

### Before Submitting

1. **Update from upstream:**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes:**
   - Write clean, documented code
   - Add or update tests
   - Update documentation

4. **Test your changes:**
   ```bash
   python manage.py test
   python manage.py check
   ```

5. **Format your code:**
   ```bash
   black .
   isort .
   flake8 .
   ```

6. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Add feature: description of changes"
   ```
   
   Follow commit message conventions:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation
   - `test:` for tests
   - `refactor:` for code refactoring
   - `style:` for formatting changes
   - `chore:` for maintenance tasks

### Submitting the Pull Request

1. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create the PR:**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template

3. **PR Description should include:**
   - Summary of changes
   - Related issue number (if applicable)
   - Screenshots (for UI changes)
   - Testing steps
   - Breaking changes (if any)

### PR Template

```markdown
## Description
Brief description of changes

## Related Issue
Fixes #123

## Changes Made
- Change 1
- Change 2

## Testing
- [ ] All tests pass
- [ ] Added new tests
- [ ] Manual testing completed

## Screenshots
(if applicable)

## Breaking Changes
(if any)
```

### Review Process

1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, your PR will be merged

## Reporting Bugs

### Before Submitting a Bug Report

- Check existing issues to avoid duplicates
- Verify the bug exists in the latest version
- Collect relevant information

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**Steps to Reproduce**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior**
What you expected to happen

**Actual Behavior**
What actually happened

**Environment**
- OS: [e.g., Ubuntu 20.04]
- Python version: [e.g., 3.9.5]
- Django version: [e.g., 4.2]
- MongoDB version: [e.g., 5.0]

**Additional Context**
Any other relevant information
```

## Suggesting Enhancements

### Enhancement Proposal Template

```markdown
**Feature Description**
Clear description of the proposed feature

**Use Case**
Why is this feature needed?

**Proposed Solution**
How should this be implemented?

**Alternatives Considered**
What other approaches did you consider?

**Additional Context**
Any other relevant information
```

## Project Structure

```
django-rest-framework-drf/
├── drf_pymongo_project/    # Django project settings
├── products/               # Products API app
│   ├── views.py           # API views
│   ├── serializers.py     # DRF serializers
│   ├── mongo_client.py    # MongoDB connection
│   └── tests.py           # Unit tests
├── requirements.txt        # Dependencies
├── README.md              # Main documentation
└── CONTRIBUTING.md        # This file
```

## Questions?

If you have questions:

1. Check existing documentation
2. Search closed issues
3. Ask in discussions
4. Open a new issue with the `question` label

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

Thank you for contributing! 🎉
