from lambda_two.lambda_functions.transform_location_table import (
    transform_location_table as tlt,
)
import pandas as pd


def test_all_correct_columns_are_present():
    test_location_df = pd.DataFrame(
        [
            [
                1,
                "123 Baker Street",
                "",
                "Westminster",
                "London",
                "NW1 6XE",
                "UK",
                "+44 20 7946 0912",
                "2023-01-01",
                "2023-01-02",
            ],
            [
                2,
                "47 The Lanes",
                "East Side",
                "Brighton",
                "Brighton and Hove",
                "BN1 1AL",
                "UK",
                "+44 1273 123 456",
                "2023-02-15",
                "2023-02-16",
            ],
            [
                3,
                "88 Castle Street",
                "",
                "Edinburgh",
                "Edinburgh",
                "EH2 3HT",
                "UK",
                "+44 131 226 4142",
                "2023-03-10",
                "2023-03-11",
            ],
            [
                4,
                "2 Water Lane",
                "Thames Dock",
                "Liverpool",
                "Liverpool",
                "L2 0RR",
                "UK",
                "+44 151 909 8101",
                "2023-04-05",
                "2023-04-06",
            ],
        ]
    )
    test_location_df.columns = [
        "address_id",
        "address_line_1",
        "address_line_2",
        "district",
        "city",
        "postal_code",
        "country",
        "phone",
        "created_at",
        "last_updated",
    ]

    output = tlt(test_location_df)

    assert output.columns.tolist() == [
        "location_id",
        "address_line_1",
        "address_line_2",
        "district",
        "city",
        "postcode",
        "country",
        "phone",
    ]


def test_return_type_is_pd_dataframe():
    test_location_df = pd.DataFrame(
        [
            [
                1,
                "123 Baker Street",
                "",
                "Westminster",
                "London",
                "NW1 6XE",
                "UK",
                "+44 20 7946 0912",
                "2023-01-01",
                "2023-01-02",
            ],
            [
                2,
                "47 The Lanes",
                "East Side",
                "Brighton",
                "Brighton and Hove",
                "BN1 1AL",
                "UK",
                "+44 1273 123 456",
                "2023-02-15",
                "2023-02-16",
            ],
            [
                3,
                "88 Castle Street",
                "",
                "Edinburgh",
                "Edinburgh",
                "EH2 3HT",
                "UK",
                "+44 131 226 4142",
                "2023-03-10",
                "2023-03-11",
            ],
            [
                4,
                "2 Water Lane",
                "Thames Dock",
                "Liverpool",
                "Liverpool",
                "L2 0RR",
                "UK",
                "+44 151 909 8101",
                "2023-04-05",
                "2023-04-06",
            ],
        ]
    )
    test_location_df.columns = [
        "address_id",
        "address_line_1",
        "address_line_2",
        "district",
        "city",
        "postal_code",
        "country",
        "phone",
        "created_at",
        "last_updated",
    ]

    output = tlt(test_location_df)

    assert isinstance(output, pd.DataFrame)
