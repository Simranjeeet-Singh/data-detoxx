def currency_code_to_currency_name(currency_code: str) -> str:
    currency_names = {
        "EUR": "Euro",
        "GBP": "Pounds Sterling",
        "USD": "United States dollar"
    }

    return currency_names.get(currency_code, "Unknown currency code")
