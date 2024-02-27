from lambda_two.lambda_functions.transform_fact_payment import (
    sales_dt_transform,
    fact_payment,
)

import pandas as pd


def test_sales_dt_transform():
    date = "2022-11-03 14:20:52.186"
    date2 = "2023-11-03 00:20:52.186"
    assert sales_dt_transform(date) == ("2022-11-03", "14:20:52.186000")
    assert sales_dt_transform(date2) == ("2023-11-03", "00:20:52.186000")


def test_returns_transformed_fact_payment_table_when_passed_original_payment_db():
<<<<<<< HEAD
    payment = [
        {
            "payment_id": 2,
            "created_at": "2022-11-03T14:20:52.187Z",
            "last_updated": "2022-11-03T14:20:52.187Z",
            "transaction_id": 2,
            "counterparty_id": 15,
            "payment_amount": 552548.62,
            "currency_id": 2,
            "payment_type_id": 3,
            "paid": False,
            "payment_date": "2022-11-04",
            "company_ac_number": 67305075,
            "counterparty_ac_number": 31622269,
        },
        {
            "payment_id": 3,
            "created_at": "2022-11-03T14:20:52.186Z",
            "last_updated": "2022-11-03T14:20:52.186Z",
            "transaction_id": 3,
            "counterparty_id": 18,
            "payment_amount": 205952.22,
            "currency_id": 3,
            "payment_type_id": 1,
            "paid": False,
            "payment_date": "2022-11-03",
            "company_ac_number": 81718079,
            "counterparty_ac_number": 47839086,
        },
        {
            "payment_id": 5,
            "created_at": "2022-11-03T14:20:52.187Z",
            "last_updated": "2022-11-03T14:20:52.187Z",
            "transaction_id": 5,
            "counterparty_id": 17,
            "payment_amount": 57067.20,
            "currency_id": 2,
            "payment_type_id": 3,
            "paid": False,
            "payment_date": "2022-11-06",
            "company_ac_number": 66213052,
            "counterparty_ac_number": 91659548,
        },
        {
            "payment_id": 8,
            "created_at": "2022-11-03T14:20:52.186Z",
            "last_updated": "2022-11-03T14:20:52.186Z",
            "transaction_id": 8,
            "counterparty_id": 2,
            "payment_amount": 254007.12,
            "currency_id": 3,
            "payment_type_id": 3,
            "paid": False,
            "payment_date": "2022-11-05",
            "company_ac_number": 32948439,
            "counterparty_ac_number": 90135525,
        },
        {
            "payment_id": 16,
            "created_at": "2022-11-04T15:42:10.886Z",
            "last_updated": "2022-11-04T15:42:10.886Z",
            "transaction_id": 16,
            "counterparty_id": 15,
            "payment_amount": 250459.52,
            "currency_id": 2,
            "payment_type_id": 1,
            "paid": False,
            "payment_date": "2022-11-05",
            "company_ac_number": 34445327,
            "counterparty_ac_number": 71673373,
        },
        {
            "payment_id": 1,
            "created_at": "2022-11-03T14:20:52.186Z",
            "last_updated": "2022-11-07T07:55:11.885Z",
            "transaction_id": 1,
            "counterparty_id": 17,
            "payment_amount": 56925.44,
            "currency_id": 2,
            "payment_type_id": 3,
            "paid": True,
            "payment_date": "2022-11-07",
            "company_ac_number": 52923196,
            "counterparty_ac_number": 32957646,
        },
    ]
    df_payment = pd.DataFrame(payment)
    result = fact_payment(df_payment)
    cols_list = [
        "payment_record_id",
        "payment_id",
        "created_date",
        "created_time",
        "last_updated_date",
        "last_updated_time",
        "transaction_id",
        "counterparty_id",
        "payment_amount",
        "currency_id",
        "payment_type_id",
        "paid",
        "payment_date",
        "company_ac_number",
        "counterparty_ac_number",
    ]
    assert result.columns.to_list() == cols_list
=======
    payment= [
	{
		"payment_id" : 2,
		"created_at" : "2022-11-03T14:20:52.187Z",
		"last_updated" : "2022-11-03T14:20:52.187Z",
		"transaction_id" : 2,
		"counterparty_id" : 15,
		"payment_amount" : 552548.62,
		"currency_id" : 2,
		"payment_type_id" : 3,
		"paid" :False,
		"payment_date" : "2022-11-04",
		"company_ac_number" : 67305075,
		"counterparty_ac_number" : 31622269
	},
	{
		"payment_id" : 3,
		"created_at" : "2022-11-03T14:20:52.186Z",
		"last_updated" : "2022-11-03T14:20:52.186Z",
		"transaction_id" : 3,
		"counterparty_id" : 18,
		"payment_amount" : 205952.22,
		"currency_id" : 3,
		"payment_type_id" : 1,
		"paid" : False,
		"payment_date" : "2022-11-03",
		"company_ac_number" : 81718079,
		"counterparty_ac_number" : 47839086
	},
	{
		"payment_id" : 5,
		"created_at" : "2022-11-03T14:20:52.187Z",
		"last_updated" : "2022-11-03T14:20:52.187Z",
		"transaction_id" : 5,
		"counterparty_id" : 17,
		"payment_amount" : 57067.20,
		"currency_id" : 2,
		"payment_type_id" : 3,
		"paid" : False,
		"payment_date" : "2022-11-06",
		"company_ac_number" : 66213052,
		"counterparty_ac_number" : 91659548
	},
	{
		"payment_id" : 8,
		"created_at" : "2022-11-03T14:20:52.186Z",
		"last_updated" : "2022-11-03T14:20:52.186Z",
		"transaction_id" : 8,
		"counterparty_id" : 2,
		"payment_amount" : 254007.12,
		"currency_id" : 3,
		"payment_type_id" : 3,
		"paid" : False,
		"payment_date" : "2022-11-05",
		"company_ac_number" : 32948439,
		"counterparty_ac_number" : 90135525
	},
	{
		"payment_id" : 16,
		"created_at" : "2022-11-04T15:42:10.886Z",
		"last_updated" : "2022-11-04T15:42:10.886Z",
		"transaction_id" : 16,
		"counterparty_id" : 15,
		"payment_amount" : 250459.52,
		"currency_id" : 2,
		"payment_type_id" : 1,
		"paid" : False,
		"payment_date" : "2022-11-05",
		"company_ac_number" : 34445327,
		"counterparty_ac_number" : 71673373
	},
	{
		"payment_id" : 1,
		"created_at" : "2022-11-03T14:20:52.186Z",
		"last_updated" : "2022-11-07T07:55:11.885Z",
		"transaction_id" : 1,
		"counterparty_id" : 17,
		"payment_amount" : 56925.44,
		"currency_id" : 2,
		"payment_type_id" : 3,
		"paid" : True,
		"payment_date" : "2022-11-07",
		"company_ac_number" : 52923196,
		"counterparty_ac_number" : 32957646
	}]
    df_payment=pd.DataFrame(payment)
    result=fact_payment(df_payment)
    cols_list=['payment_id','created_date','created_time','last_updated_date','last_updated_time','transaction_id','counterparty_id','payment_amount','currency_id','payment_type_id',
                           'paid','payment_date','company_ac_number','counterparty_ac_number']
    assert result.columns.to_list()==cols_list

    
>>>>>>> main
