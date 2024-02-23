
import pandas as pd
import math 
from lambda_two.lambda_functions.transform_transaction import (dim_transaction)

def test_returns_the_transformed_transaction_table_when_passed_transaction_dataframe():
    nan_value=math.nan

    transaction=[
        {
            "transaction_id" : 1,
            "transaction_type" : "PURCHASE",
            "sales_order_id" : nan_value,
            "purchase_order_id" : 2,
            "created_at" : "2022-11-03T14:20:52.186Z",
            "last_updated" : "2022-11-03T14:20:52.186Z"
        },
        {
            "transaction_id" : 2,
            "transaction_type" : "PURCHASE",
            "sales_order_id" : nan_value,
            "purchase_order_id" : 3,
            "created_at" : "2022-11-03T14:20:52.187Z",
            "last_updated" : "2022-11-03T14:20:52.187Z"
        },
        {
            "transaction_id" : 3,
            "transaction_type" : "SALE",
            "sales_order_id" : 1,
            "purchase_order_id" : nan_value,
            "created_at" : "2022-11-03T14:20:52.186Z",
            "last_updated" : "2022-11-03T14:20:52.186Z"
        },
        {
            "transaction_id" : 4,
            "transaction_type" : "PURCHASE",
            "sales_order_id" : nan_value,
            "purchase_order_id" : 1,
            "created_at" : "2022-11-03T14:20:52.187Z",
            "last_updated" : "2022-11-03T14:20:52.187Z"
        },
        {
            "transaction_id" : 5,
            "transaction_type" : "PURCHASE",
            "sales_order_id" : nan_value,
            "purchase_order_id" : 4,
            "created_at" : "2022-11-03T14:20:52.187Z",
            "last_updated" : "2022-11-03T14:20:52.187Z"
        },
        {
            "transaction_id" : 6,
            "transaction_type" : "SALE",
            "sales_order_id" : 2,
            "purchase_order_id" : nan_value,
            "created_at" : "2022-11-03T14:20:52.186Z",
            "last_updated" : "2022-11-03T14:20:52.186Z"
        },
        {
            "transaction_id" : 7,
            "transaction_type" : "SALE",
            "sales_order_id" : 3,
            "purchase_order_id" : nan_value,
            "created_at" : "2022-11-03T14:20:52.188Z",
            "last_updated" : "2022-11-03T14:20:52.188Z"
        },
        {
            "transaction_id" : 8,
            "transaction_type" : "PURCHASE",
            "sales_order_id" : nan_value,
            "purchase_order_id" : 5,
            "created_at" : "2022-11-03T14:20:52.186Z",
            "last_updated" : "2022-11-03T14:20:52.186Z"
        }
    ]

    df_transaction=pd.DataFrame(transaction)
    result=dim_transaction(df_transaction)
    cols_list=['transaction_id','transaction_type','sales_order_id','purchase_order_id']
    assert result.columns.to_list()==cols_list