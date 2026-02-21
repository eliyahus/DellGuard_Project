# DellGuard Tests

This directory contains the test suite for DellGuard.

## Structure

- `unit/` - Unit tests for individual components
- `integration/` - Integration tests for full workflows
- `fixtures/` - Test data and fixtures

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_analyzer.py
```
