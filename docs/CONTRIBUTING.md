# Contributing to LifeOS

Thank you for your interest in contributing to **LifeOS — Personal Life Management & Analytics Platform**!

## Code Style & Guidelines

1. **Python (Backend)**
   - Follow PEP 8 guidelines.
   - All domain services must use standard type hints (`typing.List`, `typing.Dict`, `typing.Tuple`).
   - Keep methods focused with docstrings describing input parameters and return types.

2. **JavaScript (Frontend)**
   - Native ES6+ Vanilla JavaScript.
   - Use ES modules (`import`/`export`).
   - Avoid external UI libraries or React dependencies.

3. **CSS Design System**
   - Use CSS custom variables defined in `variables.css`.
   - Ensure responsive mobile breakpoints (`@media (max-width: 768px)`).

## Pull Request Checklist

- [ ] All unit tests pass cleanly (`python -m unittest discover -s backend/tests`).
- [ ] No syntax or encoding errors.
- [ ] Documentation updated if API routes or schema change.
