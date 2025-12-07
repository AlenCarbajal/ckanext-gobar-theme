"""Tests for validators.py."""

import pytest

import ckan.plugins.toolkit as tk

from ckanext.gobar_theme.logic import validators


def test_gobar_theme_reauired_with_valid_value():
    assert validators.gobar_theme_required("value") == "value"


def test_gobar_theme_reauired_with_invalid_value():
    with pytest.raises(tk.Invalid):
        validators.gobar_theme_required(None)
