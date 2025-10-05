# Contributing to Agentic Labeling Orchestrator (ALO)

Thank you for your interest in contributing to ALO! 🎉

We welcome contributions from the community and are grateful for your support in making this project better.

## 🤝 How to Contribute

### Reporting Bugs

1. **Search existing issues** to see if the bug has already been reported
2. **Create a new issue** with a clear title and description
3. **Include reproduction steps** and expected vs. actual behavior
4. **Provide system information** (OS, Python version, package versions)

### Suggesting Features

1. **Check existing feature requests** in GitHub Discussions
2. **Create a discussion** explaining the feature and its use case
3. **Be open to feedback** from maintainers and community

### Contributing Code

#### Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/labellerr-alo.git
   cd labellerr-alo
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install in development mode**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

#### Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards

3. **Write tests** for new functionality

4. **Run tests locally**
   ```bash
   pytest tests/
   ```

5. **Format your code**
   ```bash
   black alo/
   isort alo/
   flake8 alo/
   ```

6. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

7. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Open a Pull Request** on GitHub

## 📝 Coding Standards

### Python Style Guide

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use [Black](https://github.com/psf/black) for code formatting
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Maximum line length: 88 characters (Black default)

### Code Quality

- Write docstrings for all public functions and classes (Google style)
- Add type hints to function signatures
- Keep functions focused and small
- Write meaningful variable names
- Add comments for complex logic

### Testing

- Write unit tests for new features
- Maintain test coverage above 80%
- Test edge cases and error conditions
- Use descriptive test names

Example:
```python
def test_workflow_orchestrator_loads_valid_config():
    """Test that orchestrator successfully loads a valid YAML config."""
    orchestrator = WorkflowOrchestrator("tests/fixtures/valid_workflow.yaml")
    assert orchestrator.config is not None
    assert orchestrator.config.name == "test_workflow"
```

## 🔀 Pull Request Process

1. **Update documentation** if you're changing functionality
2. **Add entries to CHANGELOG.md** for significant changes
3. **Ensure all tests pass** and CI is green
4. **Request review** from maintainers
5. **Address feedback** promptly
6. **Squash commits** if requested before merging

### PR Title Format

Use conventional commits:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Adding or updating tests
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

Example: `feat: add GPT-4V classifier agent`

## 🏗️ Project Structure

```
alo/
├── orchestrator/      # Workflow engine
├── connectors/        # Platform integrations
├── agents/           # AI agents for pre-labeling
├── validators/       # Quality assurance modules
├── active_learning/  # Sample selection strategies
└── utils/            # Utility functions
```

## 🧪 Testing Guidelines

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=alo --cov-report=html

# Run specific test file
pytest tests/test_orchestrator.py

# Run specific test
pytest tests/test_orchestrator.py::test_workflow_loads_config
```

### Writing Tests

- Place tests in the `tests/` directory
- Mirror the structure of the `alo/` directory
- Use fixtures for common setup
- Mock external API calls

## 📚 Documentation

### Updating Documentation

- Update docstrings when changing function signatures
- Update README.md for major features
- Add examples to `examples/` directory
- Update API documentation in `docs/`

### Documentation Style

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of the function.
    
    Longer description if needed, explaining the purpose,
    behavior, and any important details.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is empty
        
    Example:
        >>> result = function_name("test", 42)
        >>> print(result)
        True
    """
    pass
```

## 🎯 Areas We Need Help

- **New Agents**: Implement foundation model integrations (GPT-4V, SAM, YOLO, etc.)
- **Validators**: Build quality assurance modules
- **Active Learning**: Implement sample selection strategies
- **Documentation**: Improve tutorials and examples
- **Testing**: Increase test coverage
- **Performance**: Optimize workflow execution

## 🙏 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and beginners
- Provide constructive feedback
- Focus on the technical merits
- Report unacceptable behavior to maintainers

## ❓ Questions?

- **GitHub Discussions**: For general questions and ideas
- **GitHub Issues**: For bugs and feature requests
- **Email**: support@labellerr.com

## 🎉 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Featured in our community showcase

Thank you for contributing to ALO! 🚀
