import pytest
import pandas as pd
from datetime import datetime
from lambda_two.lambda_functions.fact_sales_transform import (
    sales_dt_transform,
    precision_changer,
    fact_sales_transformer,
)


def test_sales_dt_transform():
    date = "2022-11-03 14:20:52.186"
    date2 = "2023-11-03 00:20:52.186"
    assert sales_dt_transform(date) == ("2022-11-03", "14:20:52.186000")
    assert sales_dt_transform(date2) == ("2023-11-03", "00:20:52.186000")


def test_precision_changer_rounds_to_2_decimal_digits():
    input_float = 10.123456789
    assert precision_changer(input_float) == 10.12
    input_float = 10.999
    assert precision_changer(input_float) == 11.00


def test_precision_changer_rounds_to_8_integer_digits():
    input_float = 1234567890.123456789
    assert precision_changer(input_float) == 99999999.12
    assert len(str(precision_changer(input_float))) == 11


def test_fact_sales_transformer_output_is_df_with_correct_cols():
    test_df = pd.DataFrame(
        [
            {
                "sales_order_id": 12 - 10 - 1234,
                "staff_id": 1,
                "created_at": "2022-11-03 14:20:52.186",
                "last_updated": "2022-11-03 14:20:52.186",
                "counterparty_id": 3,
                "units_sold": 1,
                "currency_id": 1,
                "design_id": 1,
                "agreed_delivery_location_id": 2,
                "unit_price": 10.1234,
                "agreed_delivery_date": 12 - 10 - 1994,
                "agreed_payment_date": 12 - 10 - 1994,
            },
            {
                "agreed_delivery_date": 13 - 10 - 1994,
                "agreed_payment_date": 13 - 10 - 1995,
                "sales_order_id": 2,
                "last_updated": "2022-11-03 14:20:52.186",
                "staff_id": 3,
                "created_at": "2022-11-03 14:20:52.186",
                "counterparty_id": 2,
                "units_sold": 2,
                "currency_id": 5,
                "design_id": 2,
                "agreed_delivery_location_id": 1,
                "unit_price": 1000000000,
            },
        ]
    )
    return_df = fact_sales_transformer(test_df)
    assert type(return_df) == type(test_df)
    print(list(return_df.columns.values))
    assert list(return_df.columns.values) == [
        "sales_order_id",
        "created_date",
        "created_time",
        "last_updated_date",
        "last_updated_time",
        "sales_staff_id",
        "counterparty_id",
        "units_sold",
        "unit_price",
        "currency_id",
        "design_id",
        "agreed_payment_date",
        "agreed_delivery_date",
        "agreed_delivery_location_id",
    ]


def test_fact_sales_transformer_transforms_df_correctly():
    test_df = pd.DataFrame(
        [
            {
                "sales_order_id": 12 - 10 - 1234,
                "staff_id": 1,
                "created_at": "2022-11-03 14:20:52.186",
                "last_updated": "2022-11-03 14:20:52.186",
                "counterparty_id": 3,
                "units_sold": 1,
                "currency_id": 1,
                "design_id": 1,
                "agreed_delivery_location_id": 2,
                "unit_price": 10.1234,
                "agreed_delivery_date": 12 - 10 - 1994,
                "agreed_payment_date": 12 - 10 - 1994,
            },
            {
                "agreed_delivery_date": 13 - 10 - 1994,
                "agreed_payment_date": 13 - 10 - 1995,
                "sales_order_id": 2,
                "last_updated": "2022-11-03 14:20:52.186",
                "staff_id": 3,
                "created_at": "2022-11-03 14:20:52.186",
                "counterparty_id": 2,
                "units_sold": 2,
                "currency_id": 5,
                "design_id": 2,
                "agreed_delivery_location_id": 1,
                "unit_price": 1000000000,
            },
        ]
    )

    expected_return_df = pd.DataFrame(
        [
            {
                "sales_order_id": 12 - 10 - 1234,
                "created_date": "2022-11-03",
                "created_time": "14:20:52.186000",
                "last_updated_date": "2022-11-03",
                "last_updated_time": "14:20:52.186000",
                "sales_staff_id": 1,
                "counterparty_id": 3,
                "units_sold": 1,
                "unit_price": 10.12,
                "currency_id": 1,
                "design_id": 1,
                "agreed_payment_date": 12 - 10 - 1994,
                "agreed_delivery_date": 12 - 10 - 1994,
                "agreed_delivery_location_id": 2,
            },
            {
                "sales_order_id": 2,
                "created_date": "2022-11-03",
                "created_time": "14:20:52.186000",
                "last_updated_date": "2022-11-03",
                "last_updated_time": "14:20:52.186000",
                "sales_staff_id": 3,
                "counterparty_id": 2,
                "units_sold": 2,
                "unit_price": 99999999.00,
                "currency_id": 5,
                "design_id": 2,
                "agreed_payment_date": 13 - 10 - 1995,
                "agreed_delivery_date": 13 - 10 - 1994,
                "agreed_delivery_location_id": 1,
            },
        ]
    )

    return_df = fact_sales_transformer(test_df)

    expected_return_df.to_csv("./expected.csv")
    return_df.to_csv("./actual.csv")
    assert (return_df == expected_return_df).all().all()