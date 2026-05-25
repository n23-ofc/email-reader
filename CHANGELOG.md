# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-05-25

### Added
- Initial release of IMAP Email Reader
- Interactive email selection using fzf
- Cross-platform support (macOS, Linux, Windows)
- Support for both plain text and HTML emails
- Automatic link extraction from emails
- Link categorization (verification, unsubscribe, tracking, social media)
- Environment variable configuration via .env files
- Command-line argument support
- Verbose logging mode for debugging
- Comprehensive README with installation instructions for all platforms
- Setup scripts for Unix (setup.sh) and Windows (setup.ps1)
- Professional error handling with specific exception types
- PEP 8 compliant code with full docstrings
- Security best practices (no hardcoded credentials)
- Cross-platform terminal clearing
- fzf installation detection and guidance
- Support for python-dotenv for .env file management

### Security
- Removed hardcoded credentials from source code
- Added .gitignore to prevent credential leaks
- Implemented secure environment variable handling
- Added .env.example template for safe credential management

### Documentation
- Comprehensive README.md with platform-specific instructions
- CONTRIBUTING.md with development guidelines
- Code of Conduct for contributors
- MIT License
- Inline code documentation with Google-style docstrings
- Troubleshooting guide for common issues
- IMAP server configuration examples for popular providers

## [Unreleased]

### Planned Features
- Support for multiple IMAP folders
- Email search functionality
- Attachment download capability
- Email composition and sending
- Configuration file support (YAML/JSON)
- Email threading support
- Mark as read/unread functionality
- Automated tests
- Package distribution via PyPI

---

## Version History

- **1.0.0** - Initial public release with core functionality
