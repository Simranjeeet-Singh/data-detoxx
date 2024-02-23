from lambda_two.lambda_functions.path_to_parquet import path_to_parquet
from freezegun import freeze_time

@freeze_time("Jan 14th, 2012")
def test_returns_correct_path():
    output = path_to_parquet('fact_sales_order', 1)
    output2 = path_to_parquet('dim_date', 129)
    expected = 'fact_sales_order/fact_sales_order__[#1]__2012-01-14T000000000Z.parquet'
    expected2 = 'dim_date/dim_date__[#129]__2012-01-14T000000000Z.parquet'
    assert output == expected
    assert output2 == expected2