# from lambda_two.lambda_functions.transform_currency_table import (
#     transform_currency_table as tct,
# )

# import pandas as pd


# def test_correct_column_names_are_present():
#     test_currency_df = pd.DataFrame(
#         [
#             [1, "GBP", "2022-11-03 14:20:49.962", "2022-11-03 14:20:49.962"],
#             [2, "EUR", "2022-11-03 14:20:49.962", "2022-11-03 14:20:49.962"],
#             [3, "USD", "2022-11-03 14:20:49.962", "2022-11-03 14:20:49.962"],
#         ]
#     )
#     test_currency_df.columns = [
#         "currency_id",
#         "currency_code",
#         "created_at",
#         "last_updated",
#     ]
#     output = tct(test_currency_df)

#     assert output.columns.tolist() == [
#         "currency_id",
#         "currency_code",
#         "currency_name"
#     ]


# def test_return_type_is_pd_dataframe():
#     test_currency_df = pd.DataFrame(
#         [
#             [1, "GBP", "2022-11-03 14:20:49.962", "2022-11-03 14:20:49.962"],
#             [2, "EUR", "2022-11-03 14:20:49.962", "2022-11-03 14:20:49.962"],
#             [3, "USD", "2022-11-03 14:20:49.962", "2022-11-03 14:20:49.962"],
#         ]
#     )
#     test_currency_df.columns = [
#         "currency_id",
#         "currency_code"
#     ]
#     output = tct(test_currency_df)

#     assert isinstance(output, pd.DataFrame)
