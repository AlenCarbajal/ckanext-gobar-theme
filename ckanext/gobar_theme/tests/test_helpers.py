"""Tests for helpers.py."""

import ckanext.gobar_theme.helpers as helpers


def test_gobar_theme_hello():
    assert helpers.gobar_theme_hello() == "Hello, gobar_theme!"
