"""Tests for bnb_test_project_plz_ignore."""

import pytest

import bnb_test_project_plz_ignore


def test_version_available() -> None:
    """Test that the module has a version dunder."""
    assert hasattr(bnb_test_project_plz_ignore, "__version__")


if __name__ == "__main__":
    pytest.main([__file__])
