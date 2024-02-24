from utils.currency_code_to_currency_name import (
    currency_code_to_currency_name as cccn,
)


def test_function_returns_correct_string_for_inputs():
    assert cccn("EUR") == "Euro"


def test_function_returns_error_message_if_code_not_found():
    assert cccn("JPY") == "Unknown currency code"
