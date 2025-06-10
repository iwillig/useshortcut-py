"""Pytest configuration and fixtures for tests."""

import pytest


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "integration: mark test as an integration test")
