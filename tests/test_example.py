"""This module contains example tests."""

from mechabellum_scraper import my_function


def test_my_function() -> None:
    expected_value = 42
    assert my_function() == expected_value