# Contributing Guidelines for Director Agent

Thank you for considering contributing to the Director Agent! To keep our codebase clean, maintainable, and welcoming, please follow these sensible guidelines:

## General Principles
- Be respectful and constructive in all communications.
- Keep contributions focused and as small as practical for easier review.
- Write clear, concise commit messages.
- When in doubt, open an issue or discussion before submitting a large change.

## Code Quality
- Add descriptive docstrings to all classes and methods.
- Use type hints for all method signatures and function arguments, including publish payloads.
- Prefer clear, readable code over cleverness.
- Follow PEP8 for Python code style.
- Add error handling for possible exceptions from `reply` or `publish` methods.

## Testing
- Cover new features and bug fixes with unit tests.
- Expand tests to cover edge cases, such as:
  - Empty user input
  - Exceptions raised by `reply` or `publish`
  - Verifying logging if it's important
- Tests should be easy to understand and maintain.

## Pull Requests
- Link related issues in your PR description if applicable.
- Describe what your change does and why it’s needed.
- Make sure your branch is up to date with main before submitting.
- Be open to feedback and ready to make changes.

By following these guidelines, we ensure the Director Agent remains robust, maintainable, and welcoming to all contributors.
