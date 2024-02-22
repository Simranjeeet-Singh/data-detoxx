from src.transform_staff_table import transform_staff_table
import pandas as pd


def test_returns_correct_dataframe():
    staff_df = pd.DataFrame(
        [
            [
                1,
                "Jeremie",
                "Franey",
                2,
                "jeremie.franey@terrifictotes.com",
                "2022-11-03 14:20:51.563",
                "2022-11-03 14:20:51.563",
            ],
            [
                2,
                "Deron",
                "Beier",
                3,
                "deron.beier@terrifictotes.com",
                "2022-11-03 14:20:51.563",
                "2022-11-03 14:20:51.563",
            ],
            [
                3,
                "Jeanette",
                "Erdman",
                1,
                "jeanette.erdman@terrifictotes.com",
                "2022-11-03 14:20:51.563",
                "2022-11-03 14:20:51.563",
            ],
        ]
    )
    staff_df.columns = [
        "staff_id",
        "first_name",
        "last_name",
        "department_id",
        "email_address",
        "created_at",
        "last_updated",
    ]
    department_df = pd.DataFrame(
        [
            [
                1,
                "Sales",
                "Manchester",
                "Richard Roma",
                "2022-11-03 14:20:49.962",
                "2022-11-03 14:20:49.962",
            ],
            [
                2,
                "Purchasing",
                "Manchester",
                "Naomi Lapaglia",
                "2022-11-03 14:20:49.962",
                "2022-11-03 14:20:49.962",
            ],
            [
                3,
                "Production",
                "Leeds",
                "Chester Ming",
                "2022-11-03 14:20:49.962",
                "2022-11-03 14:20:49.962",
            ],
        ]
    )
    department_df.columns = [
        "department_id",
        "department_name",
        "location",
        "manager",
        "created_at",
        "last_updated",
    ]
    output = transform_staff_table(staff_df, department_df).to_dict()
    expected_output = {
        "department_name": {0: "Purchasing", 1: "Production", 2: "Sales"},
        "email_address": {
            0: "jeremie.franey@terrifictotes.com",
            1: "deron.beier@terrifictotes.com",
            2: "jeanette.erdman@terrifictotes.com",
        },
        "first_name": {0: "Jeremie", 1: "Deron", 2: "Jeanette"},
        "last_name": {0: "Franey", 1: "Beier", 2: "Erdman"},
        "location": {0: "Manchester", 1: "Leeds", 2: "Manchester"},
        "staff_id": {0: 1, 1: 2, 2: 3},
    }
    assert output == expected_output


def test_type_returned_is_dataframe():
    staff_df = pd.DataFrame(
        [
            [
                1,
                "Jeremie",
                "Franey",
                2,
                "jeremie.franey@terrifictotes.com",
                "2022-11-03 14:20:51.563",
                "2022-11-03 14:20:51.563",
            ],
            [
                2,
                "Deron",
                "Beier",
                3,
                "deron.beier@terrifictotes.com",
                "2022-11-03 14:20:51.563",
                "2022-11-03 14:20:51.563",
            ],
            [
                3,
                "Jeanette",
                "Erdman",
                1,
                "jeanette.erdman@terrifictotes.com",
                "2022-11-03 14:20:51.563",
                "2022-11-03 14:20:51.563",
            ],
        ]
    )
    staff_df.columns = [
        "staff_id",
        "first_name",
        "last_name",
        "department_id",
        "email_address",
        "created_at",
        "last_updated",
    ]
    department_df = pd.DataFrame(
        [
            [
                1,
                "Sales",
                "Manchester",
                "Richard Roma",
                "2022-11-03 14:20:49.962",
                "2022-11-03 14:20:49.962",
            ],
            [
                2,
                "Purchasing",
                "Manchester",
                "Naomi Lapaglia",
                "2022-11-03 14:20:49.962",
                "2022-11-03 14:20:49.962",
            ],
            [
                3,
                "Production",
                "Leeds",
                "Chester Ming",
                "2022-11-03 14:20:49.962",
                "2022-11-03 14:20:49.962",
            ],
        ]
    )
    department_df.columns = [
        "department_id",
        "department_name",
        "location",
        "manager",
        "created_at",
        "last_updated",
    ]

    output = transform_staff_table(staff_df, department_df)

    assert isinstance(output, pd.DataFrame)


def test_correct_column_names_present():
    staff_df = pd.DataFrame(
        [
            [
                1,
                "Jeremie",
                "Franey",
                2,
                "jeremie.franey@terrifictotes.com",
                "2022-11-03 14:20:51.563",
                "2022-11-03 14:20:51.563",
            ],
            [
                2,
                "Deron",
                "Beier",
                3,
                "deron.beier@terrifictotes.com",
                "2022-11-03 14:20:51.563",
                "2022-11-03 14:20:51.563",
            ],
            [
                3,
                "Jeanette",
                "Erdman",
                1,
                "jeanette.erdman@terrifictotes.com",
                "2022-11-03 14:20:51.563",
                "2022-11-03 14:20:51.563",
            ],
        ]
    )
    staff_df.columns = [
        "staff_id",
        "first_name",
        "last_name",
        "department_id",
        "email_address",
        "created_at",
        "last_updated",
    ]
    department_df = pd.DataFrame(
        [
            [
                1,
                "Sales",
                "Manchester",
                "Richard Roma",
                "2022-11-03 14:20:49.962",
                "2022-11-03 14:20:49.962",
            ],
            [
                2,
                "Purchasing",
                "Manchester",
                "Naomi Lapaglia",
                "2022-11-03 14:20:49.962",
                "2022-11-03 14:20:49.962",
            ],
            [
                3,
                "Production",
                "Leeds",
                "Chester Ming",
                "2022-11-03 14:20:49.962",
                "2022-11-03 14:20:49.962",
            ],
        ]
    )
    department_df.columns = [
        "department_id",
        "department_name",
        "location",
        "manager",
        "created_at",
        "last_updated",
    ]

    output = transform_staff_table(staff_df, department_df)

    cols_list = output.columns.tolist()

    assert cols_list == [
        "staff_id",
        "first_name",
        "last_name",
        "department_name",
        "location",
        "email_address",
    ]


def test_swap_NaN_to_NA_when_no_location_provided():

    staff_df = pd.DataFrame(
        [
            [
                1,
                "Jeremie",
                "Franey",
                2,
                "jeremie.franey@terrifictotes.com",
                "2022-11-03 14:20:51.563",
                "2022-11-03 14:20:51.563",
            ],
            [
                2,
                "Deron",
                "Beier",
                3,
                "deron.beier@terrifictotes.com",
                "2022-11-03 14:20:51.563",
                "2022-11-03 14:20:51.563",
            ],
            [
                3,
                "Jeanette",
                "Erdman",
                1,
                "jeanette.erdman@terrifictotes.com",
                "2022-11-03 14:20:51.563",
                "2022-11-03 14:20:51.563",
            ],
        ]
    )
    staff_df.columns = [
        "staff_id",
        "first_name",
        "last_name",
        "department_id",
        "email_address",
        "created_at",
        "last_updated",
    ]

    department_df = pd.DataFrame(
        [
            [
                1,
                "Sales",
                float("NaN"),
                "Richard Roma",
                "2022-11-03 14:20:49.962",
                "2022-11-03 14:20:49.962",
            ],
            [
                2,
                "Purchasing",
                "Manchester",
                "Naomi Lapaglia",
                "2022-11-03 14:20:49.962",
                "2022-11-03 14:20:49.962",
            ],
            [
                3,
                "Production",
                "Leeds",
                "Chester Ming",
                "2022-11-03 14:20:49.962",
                "2022-11-03 14:20:49.962",
            ],
        ]
    )
    department_df.columns = [
        "department_id",
        "department_name",
        "location",
        "manager",
        "created_at",
        "last_updated",
    ]
    expected_output = {
        "staff_id": {0: 1, 1: 2, 2: 3},
        "first_name": {0: "Jeremie", 1: "Deron", 2: "Jeanette"},
        "last_name": {0: "Franey", 1: "Beier", 2: "Erdman"},
        "department_name": {0: "Purchasing", 1: "Production", 2: "Sales"},
        "location": {0: "Manchester", 1: "Leeds", 2: "N/A"},
        "email_address": {
            0: "jeremie.franey@terrifictotes.com",
            1: "deron.beier@terrifictotes.com",
            2: "jeanette.erdman@terrifictotes.com",
        },
    }
    output = transform_staff_table(staff_df, department_df).to_dict()
    assert output == expected_output
