def currency_code_to_currency_name(currency_code: str) -> str:
    """
    Convert a currency code to its corresponding currency name.

    Parameters:
    - currency_code (str): The three-letter currency code (ISO 4217) for which the currency name is desired.

    Returns:
    - str: The name of the currency corresponding to the given code. If the code is not recognized, returns "Unknown currency code".

    Example:
    >>> currency_code_to_currency_name("EUR")
    'Euro'
    >>> currency_code_to_currency_name("XYZ")
    'Unknown currency code'
    """
    currency_names = {
        "EUR": "Euro",
        "GBP": "Pounds Sterling",
        "USD": "United States dollar",
    }

    return currency_names.get(currency_code, "Unknown currency code")
