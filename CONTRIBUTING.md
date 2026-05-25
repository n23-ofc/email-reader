# Contributing to IMAP Email Reader

Thank you for considering contributing to this project! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help create a welcoming environment for all contributors

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Your environment (OS, Python version, etc.)
- Any relevant logs or screenshots

### Suggesting Enhancements

Enhancement suggestions are welcome! Please:
- Use a clear, descriptive title
- Provide a detailed description of the proposed feature
- Explain why this enhancement would be useful
- Include examples if applicable

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes**:
   - Follow the existing code style (PEP 8)
   - Add docstrings to new functions
   - Update documentation if needed
3. **Test your changes**:
   - Test on multiple platforms if possible
   - Ensure existing functionality still works
4. **Commit your changes**:
   - Use clear, descriptive commit messages
   - Reference any related issues
5. **Submit a pull request**:
   - Provide a clear description of the changes
   - Reference any related issues

## Development Setup

### 1. Fork and Clone

```bash
git clone https://github.com/n23-ofc/email-reader.git
cd email-reader
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install flake8 black mypy  # Development dependencies
```

### 4. Set Up Pre-commit Hooks (Optional)

```bash
pip install pre-commit
pre-commit install
```

## Coding Standards

### Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints where appropriate
- Maximum line length: 100 characters
- Use descriptive variable and function names

### Code Quality Tools

**Check style:**
```bash
flake8 email_reader.py
```

**Format code:**
```bash
black email_reader.py
```

**Type checking:**
```bash
mypy email_reader.py
```

### Documentation

- Add docstrings to all functions, classes, and modules
- Use Google-style docstrings
- Update README.md for user-facing changes
- Add inline comments for complex logic

Example docstring:
```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of function.
    
    Longer description if needed, explaining the function's
    purpose and behavior in detail.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: Description of when this is raised
    """
    pass
```

## Testing

### Manual Testing

Test your changes on:
- Different operating systems (macOS, Linux, Windows)
- Different Python versions (3.7+)
- Different IMAP servers (Gmail, Outlook, etc.)

### Testing Checklist

- [ ] Code runs without errors
- [ ] All existing features still work
- [ ] New features work as expected
- [ ] Error handling works properly
- [ ] Cross-platform compatibility verified
- [ ] Documentation updated

## Project Structure

```
email-reader/
├── email_reader.py      # Main application code
├── README.md            # User documentation
├── CONTRIBUTING.md      # This file
├── LICENSE              # MIT License
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── .gitignore          # Git ignore rules
└── tests/              # Test directory (if added)
```

## Commit Message Guidelines

Use clear, imperative commit messages:

```
Add feature to categorize links by type
Fix authentication error with special characters
Update README with Windows installation steps
```

For larger changes:

```
Add support for custom IMAP folders

- Implement folder selection in main menu
- Add configuration option for default folder
- Update documentation with folder examples
```

## Release Process

(For maintainers)

1. Update version number in relevant files
2. Update CHANGELOG.md
3. Create a new tag: `git tag -a v1.0.0 -m "Version 1.0.0"`
4. Push tags: `git push origin --tags`
5. Create GitHub release with release notes

## Questions?

Feel free to open an issue for:
- Questions about contributing
- Clarification on project direction
- Discussion of major changes before implementation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing! 🎉
