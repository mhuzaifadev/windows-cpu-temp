# Contributing to Windows CPU & GPU Temperature Monitor

Thank you for your interest in contributing to Windows CPU & GPU Temperature Monitor! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How Can I Contribute?

### Reporting Bugs

- Check if the bug has already been reported in the Issues section
- Use the bug report template when creating a new issue
- Include detailed steps to reproduce the bug
- Include screenshots if applicable
- Specify your operating system and version

### Suggesting Features

- Check if the feature has already been suggested
- Use the feature request template
- Provide a clear description of the feature
- Explain why this feature would be useful
- Include any relevant examples or mockups

### Pull Requests

1. Fork the repository
2. Create a new branch for your feature/fix
3. Make your changes
4. Test your changes thoroughly
5. Update documentation if necessary
6. Submit a pull request

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/mhuzaifadev/windows-cpu-temp.git
cd windows-cpu-temp
```

2. Create a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python main.py
```

## Coding Standards

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add comments for complex logic
- Write docstrings for functions and classes
- Keep functions small and focused
- Use type hints where appropriate

## Testing

Before submitting a pull request:

1. Test on different Windows versions
2. Verify temperature readings are accurate
3. Check for memory leaks
4. Ensure UI is responsive
5. Test system tray functionality
6. Verify error handling

## Building the Application

To build the executable:

```bash
pyinstaller --onefile --windowed --icon=assets/icon.ico main.py
```

## Version Control

We follow semantic versioning (MAJOR.MINOR.PATCH):

- MAJOR: Incompatible API changes
- MINOR: Backwards-compatible functionality
- PATCH: Backwards-compatible bug fixes

## Documentation

- Update README.md if necessary
- Add comments to complex code
- Update developer documentation
- Keep the website up to date

## Need Help?

- Open an issue on GitHub
- Check existing issues and discussions
- Join our Discord community
- Email: mhuzaifadev@gmail.com

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License. 