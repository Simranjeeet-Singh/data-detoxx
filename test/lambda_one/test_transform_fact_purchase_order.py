from src.lambda_two.utils.transform_fact_purchase_order import (
    transform_fact_purchase_order as tfpo,
)
import pandas as pd

data = {
    "purchase_order_id": [1, 2, 3, 5, 62, 6, 7, 8, 10, 11],
    "created_at": [
        "2022-11-03 14:20:52.187",
        "2022-11-03 14:20:52.186",
        "2022-11-03 14:20:52.187",
        "2022-11-03 14:20:52.186",
        "2022-11-30 08:02:10.683",
        "2022-11-04 11:59:09.990",
        "2022-11-04 12:18:09.885",
        "2022-11-04 18:03:10.233",
        "2022-11-07 17:06:10.294",
        "2022-11-07 17:36:09.898",
    ],
    "last_updated": [
        "2022-11-03 14:20:52.187",
        "2022-11-03 14:20:52.186",
        "2022-11-03 14:20:52.187",
        "2022-11-03 14:20:52.186",
        "2022-11-30 08:02:10.683",
        "2022-11-04 11:59:09.990",
        "2022-11-04 12:18:09.885",
        "2022-11-04 18:03:10.233",
        "2022-11-07 17:06:10.294",
        "2022-11-07 17:36:09.898",
    ],
    "staff_id": [12, 20, 12, 18, 13, 11, 20, 15, 3, 15],
    "counterparty_id": [11, 17, 15, 2, 12, 5, 5, 20, 10, 4],
    "item_code": [
        "ZDOI5EA",
        "QLZLEXR",
        "AN3D85L",
        "I9MET53",
        "QKQQ9IS",
        "DAOECK5",
        "PBF02WW",
        "8R25O35",
        "M9NO0XK",
        "RRGNEG2",
    ],
    "item_quantity": [371, 286, 839, 316, 597, 926, 51, 119, 14, 991],
    "item_unit_price": [
        361.39,
        199.04,
        658.58,
        803.82,
        714.89,
        155.70,
        909.87,
        782.15,
        695.86,
        225.64,
    ],
    "currency_id": [2, 2, 2, 3, 2, 2, 2, 2, 2, 3],
    "agreed_delivery_date": [
        "2022-11-09",
        "2022-11-04",
        "2022-11-05",
        "2022-11-10",
        "2022-12-03",
        "2022-11-04",
        "2022-11-10",
        "2022-11-10",
        "2022-11-12",
        "2022-11-13",
    ],
    "agreed_payment_date": [
        "2022-11-07",
        "2022-11-07",
        "2022-11-04",
        "2022-11-05",
        "2022-12-03",
        "2022-11-08",
        "2022-11-07",
        "2022-11-09",
        "2022-11-09",
        "2022-11-08",
    ],
    "agreed_delivery_location_id": [6, 8, 16, 2, 11, 24, 7, 5, 13, 29],
}


def test_returns_a_pd_dataframe():
    input = pd.DataFrame(data)
    output = tfpo(input)

    assert isinstance(output, pd.DataFrame)


def test_returns_correct_column_headers():
    input = pd.DataFrame(data)
    output = tfpo(input)

    assert output.columns.tolist() == [
        "purchase_record_id",
        "purchase_order_id",
        "staff_id",
        "counterparty_id",
        "item_code",
        "item_quantity",
        "item_unit_price",
        "currency_id",
        "agreed_delivery_date",
        "agreed_payment_date",
        "agreed_delivery_location_id",
        "created_date",
        "created_time",
        "last_updated_date",
        "last_updated_time",
    ]
