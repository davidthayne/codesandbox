# Contributing to Advanced Python Sandbox

Thank you for your interest in contributing to the Advanced Python Sandbox project! This document provides guidelines and information for contributors.

## Getting Started

### Prerequisites
- Python 3.7+
- Docker (recommended for testing)
- Basic knowledge of Flask, HTML/CSS/JavaScript

### Development Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd codesandbox
   ```

2. **Set up development environment:**
   ```bash
   # Option 1: Docker (recommended)
   docker build -t python-sandbox .
   docker run -d -p 7111:7111 --name python-sandbox python-sandbox
   
   # Option 2: Local development
   pip3 install flask
   python3 codesandbox_backend.py
   ```

3. **Run tests:**
   ```bash
   python3 test_apps_workflow.py
   python3 test_html.py
   ```

## How to Contribute

### Reporting Issues
- Use the GitHub issue tracker
- Include detailed reproduction steps
- Provide system information (OS, Python version, browser)
- Include error messages and logs

### Submitting Changes

1. **Fork the repository**
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with clear messages:**
   ```bash
   git commit -m "Add: Brief description of your change"
   ```
6. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request**

### Code Style

#### Python (Backend)
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep functions focused and concise
- Handle errors gracefully

#### JavaScript/HTML/CSS (Frontend)
- Use consistent indentation (2 spaces)
- Use semantic HTML elements
- Follow modern CSS practices
- Use descriptive class and ID names
- Comment complex logic

#### General Guidelines
- Write self-documenting code
- Add comments for complex algorithms
- Keep security in mind (input validation, XSS prevention)
- Test your changes thoroughly
- Update documentation when necessary

## Development Areas

### High Priority
- Performance optimizations
- Additional security hardening
- Mobile UI improvements
- Accessibility enhancements

### New Features
- Additional built-in applications
- More code examples and tutorials
- Advanced debugging tools
- Code sharing capabilities
- Plugin system

### Documentation
- API documentation
- Video tutorials
- Deployment guides
- Troubleshooting guides

## Testing Guidelines

### Backend Testing
- Test all API endpoints
- Verify security restrictions
- Test user authentication flows
- Check resource limitations

### Frontend Testing
- Test on multiple browsers
- Verify responsive design
- Test keyboard shortcuts
- Check fullscreen functionality

### Security Testing
- Verify code sandbox restrictions
- Test authentication bypasses
- Check for XSS vulnerabilities
- Validate input sanitization

## Pull Request Guidelines

### Before Submitting
- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No security vulnerabilities introduced
- [ ] Backward compatibility maintained

### PR Description
Include in your PR description:
- Summary of changes
- Motivation for the change
- Testing performed
- Screenshots (for UI changes)
- Breaking changes (if any)

## Code Review Process

1. **Automated checks** run on all PRs
2. **Manual review** by maintainers
3. **Testing** in development environment
4. **Security review** for security-related changes
5. **Merge** after approval

## Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Documentation**: Check existing docs first

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Code of Conduct

### Our Standards
- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain professional communication

### Enforcement
Violations of the code of conduct should be reported to the project maintainers.

---

Thank you for contributing to Advanced Python Sandbox! 🎉
