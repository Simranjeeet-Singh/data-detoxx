import pandas as pd
from lambda_two.lambda_functions.transform_payment_type import (dim_payment_type)

def test_returns_an_empty_frame_when_passed_an_empty_dataframe():
    df_payment_type=pd.DataFrame()
    result=dim_payment_type(df_payment_type)
    
    assert result.columns.to_list()==[]


def test_returns_an_transformed_payment_type_frame_when_passed_payment_type_dataframe():
    payment_type= [
	{
		"payment_type_id" : 1,
		"payment_type_name" : "SALES_RECEIPT",
		"created_at" : "2022-11-03T14:20:49.962Z",
		"last_updated" : "2022-11-03T14:20:49.962Z"
	},
	{
		"payment_type_id" : 2,
		"payment_type_name" : "SALES_REFUND",
		"created_at" : "2022-11-03T14:20:49.962Z",
		"last_updated" : "2022-11-03T14:20:49.962Z"
	},
	{
		"payment_type_id" : 3,
		"payment_type_name" : "PURCHASE_PAYMENT",
		"created_at" : "2022-11-03T14:20:49.962Z",
		"last_updated" : "2022-11-03T14:20:49.962Z"
	},
	{
		"payment_type_id" : 4,
		"payment_type_name" : "PURCHASE_REFUND",
		"created_at" : "2022-11-03T14:20:49.962Z",
		"last_updated" : "2022-11-03T14:20:49.962Z"
	}
    ]
    df_payment_type=pd.DataFrame(payment_type)
    result=dim_payment_type(df_payment_type)
    
    assert result.columns.to_list()==['payment_type_id','payment_type_name']