from src.utils.file_reading_utils import path_to_parquet

def test_returns_correct_path():
    output = path_to_parquet('fact_sales_order', 1, '2024')
    output2 = path_to_parquet('dim_date', 129, '2024-01-14T000000000Z')
    expected = 'fact_sales_order/fact_sales_order__[#1]__2024.parquet'
    expected2 = 'dim_date/dim_date__[#129]__2024-01-14T000000000Z.parquet'
    assert output == expected
    assert output2 == expected2