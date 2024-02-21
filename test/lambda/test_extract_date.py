from src.extract_date import extract_date


def test_correctly_returns_year_month_day_from_timestamp():
    test_timestamp = '2022-11-03 14:20:52.186'

    output = extract_date(test_timestamp)

    assert [output['year'], output['month'], output['day']] == [2022, 11, 3]


def test_correctly_returns_day_of_week():
    test_timestamp = '2024-02-21 00:00:00.000'

    output = extract_date(test_timestamp)

    assert output['day_of_week'] == 2


def test_correctly_returns_day_name():
    test_timestamp = '2024-02-21 00:00:00.000'

    output = extract_date(test_timestamp)

    assert output['day_name'] == 'Wednesday'


def test_correctly_returns_month_name():
    test_timestamp = '2024-02-21 00:00:00.000'

    output = extract_date(test_timestamp)

    assert output['month_name'] == 'February'

def test_correctly_returns_quarter():
    test_timestamp = '2024-02-21 00:00:00.000'

    output = extract_date(test_timestamp)

    assert output['quarter'] == 1