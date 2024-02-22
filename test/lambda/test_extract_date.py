from src.extract_date import extract_date


def test_correctly_returns_year_month_day_from_timestamp():
    test_timestamp = "2022-11-03 14:20:52.186"

    output = extract_date(test_timestamp)

    assert [output["year"], output["month"], output["day"]] == [2022, 11, 3]


def test_correctly_returns_day_of_week():
    test_timestamp = "2024-02-21 00:00:00.000"

    output = extract_date(test_timestamp)

    assert output["day_of_week"] == 2


def test_correctly_returns_day_name():
    test_timestamp = "2024-02-21 00:00:00.000"

    output = extract_date(test_timestamp)

    assert output["day_name"] == "Wednesday"


def test_correctly_returns_month_name():
    test_timestamp = "2024-02-21 00:00:00.000"

    output = extract_date(test_timestamp)

    assert output["month_name"] == "February"


def test_correctly_returns_quarter():
    test_timestamp = "2024-02-21 00:00:00.000"

    output = extract_date(test_timestamp)

    print(output)

    assert output["quarter"] == 1


def test_returns_correct_dict_when_passed_date_instead_of_timestamp():
    test_date = "2024-02-21"

    output = extract_date(test_date)

    assert output == {
        "date": "2024-02-21",
        "year": 2024,
        "month": 2,
        "day": 21,
        "day_of_week": 2,
        "day_name": "Wednesday",
        "month_name": "February",
        "quarter": 1,
    }
