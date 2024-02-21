from src.transform_date_table import transform_date_table as tdt

import pandas as pd


def test_creates_a_pd_dataframe():
    test_sales_order_df = pd.DataFrame([['2022-11-05 14:20:52.186'], ['2022-11-04 14:20:52.186'],
                                        ['2022-11-03 14:20:52.188'], ['2022-11-02 14:20:52.188'], ['2022-11-01 14:20:52.186']])
    test_sales_order_df.columns = ['created_date']
    output = tdt(test_sales_order_df)

    # print(output)
    # assert False
    assert output.columns.tolist() == [
        'date_id', 'year', 'month', 'day', 'day_of_week', 'day_name', 'month_name', 'quarter']


def test_duplicates_are_removed():
    test_sales_order_df = pd.DataFrame([['2022-11-05 14:20:52.186'], ['2022-11-05 14:20:52.186'], ['2022-11-04 14:20:52.186'],
                                        ['2022-11-03 14:20:52.188'], ['2022-11-02 14:20:52.188'], ['2022-11-01 14:20:52.186']])
    test_sales_order_df.columns = ['created_date']
    output = tdt(test_sales_order_df)

    print(output)

    assert len(output) == 5


def test_takes_dates_from_multiple_rows():
    test_sales_order_df = pd.DataFrame([['2022-11-16 00:00:00.000', '2023-09-03 00:00:00.000'],
                                        ['2020-02-04 00:00:00.000',
                                            '2020-11-09 00:00:00.000'],
                                        ['2020-09-27 00:00:00.000',
                                            '2021-01-23 00:00:00.000'],
                                        ['2021-11-13 00:00:00.000',
                                            '2022-09-30 00:00:00.000'],
                                        ['2022-10-30 00:00:00.000', '2023-05-08 00:00:00.000']])
    test_sales_order_df.columns = ['created_date', 'last_updated']

    output = tdt(test_sales_order_df)

    print(output)

    assert False
