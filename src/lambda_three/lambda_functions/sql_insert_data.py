#Connect with data warehouse-Lambda_three main fucntion
#insert a table in data warehouse-Lambda_three main function
#enter the rows

import pandas as pd
import pg8000
from pg8000.native import Connection

secret_dict={}
secret_dict['Hostname']='nc-data-eng-project-dw-prod.chpsczt8h1nu.eu-west-2.rds.amazonaws.com'

secret_dict['Database_name']= 'postgres'
secret_dict['Username']='project_team_4'
secret_dict['Password']='uPgzrj1lDG0KuEQE'
secret_dict['Port']=5432
# Schema: project_team_4


conn = Connection(
            host=secret_dict["Hostname"],
            user=secret_dict["Username"],
            password=secret_dict["Password"],
            database=secret_dict["Database_name"],
            port=secret_dict["Port"])

data_currency = {
    'currency_record_id':[0,1,2],
    'currency_id': [1, 2, 3],
    'currency_code': ['USD', 'EUR', 'GBP'],
    'currency_name': ['US Dollar', 'Euro', 'British Pound'],
    'last_updated_date':['2024-05-20','2024-05-20','2024-05-20'],
    'last_updated_time':['12:30:00','12:30:00','12:30:00']
}






data_date=[{
        'date_id':'2022-01-01',
        'year':2022,
        'month':1,
        'day':1,
        'day_of_week':6,
        'day_name':'Saturday',
        'month_name':'January',
        'quarter':1,
        'last_updated_date':'2023-01-01',
        'last_updated_time':'12:30:00'
        
},
    {
    'date_id':'2022-01-03',
    'year':2022,
    'month':1,
    'day':3,
    'day_of_week':1,
    'day_name':'Monday',
    'month_name':'January',
    'quarter':1,
    'last_updated_date':'2023-01-01',
    'last_updated_time':'12:30:00'  
}]
data_location=[{
        "location_record_id":1,
        "address_id":1,
        "address_line_1":'10, Straford Street',
        "address_line_2":'Birmingham',
        "district":'West Midlands',
        "city":'Birmingham',
        "postal_code":'BI21 3QW',
        "country":'England',
        "phone":'07777777777',
        "last_updated_date":'2023-01-01',
        "last_updated_time":'12:30:00'
}]

data_design=[{
        "design_record_id":1,
        "design_id":1,
        "design_name":'Wood',
        "file_location":'design/textures',
        "file_name":'Wood.jpeg',
        "last_updated_date":'2021-01-01',
        "last_updated_time":'12:30:00'}]


data_payment_type=[{
    'payment_type_record_id':1,
    'payment_record_id':1,
    'payment_type_name':'Bank Transfer',
    'last_updated_date':'2021-01-01',
    'last_updated_time':'12:30:00'
}]

data_staff=[{'staff_id':1,
        'first_name':'Nicolo',
        'last_name':'Primi',
        'department_name':'Research',
        'location':'Birmingham',
        'email_address':'abc@gmail.com',
        'last_updated_date':'2021-01-01',
        'last_updated_time':'12:30:00.000'}] 


data_counterparty=[{
    'counterparty_record_id':1,'counterparty_id':1,'counterparty_legal_name':'North Coders','counterparty_legal_address_line_1':'Manchester Office','counterparty_legal_address_line_2':'Bull Ring','counterparty_legal_district':'Manchester','counterparty_legal_city':'Chester','counterparty_legal_postal_code':'MN12 2HQ','counterparty_legal_country':'England','counterparty_legal_phone_number':'07777777777',
    'last_updated_date':'2021-01-01',
    'last_updated_time':'12:30:00'
    }]  
data_transaction=[{'transaction_record_id':1,'transaction_id':1,'transaction_type':'Bank Transfer','sales_order_id':1001,'purchase_order_id':2001,
                   'last_updated_date':'2021-01-01',
    'last_updated_time':'12:30:00'}]


data_fact_sales=[
            {
                "sales_order_id": 1,
                "created_date": "2022-01-01",
                "created_time": "14:20:52.186000",
                "last_updated_date": "2022-01-03",
                "last_updated_time": "14:20:52.186000",
                "sales_staff_id": 1,
                "counterparty_record_id": 1,
                "units_sold": 1,
                "unit_price": 10.12,
                "currency_record_id": 1,
                "design_record_id": 1,
                "agreed_payment_date": '2022-01-01',
                "agreed_delivery_date": '2022-01-01',
                "agreed_delivery_location_id": 1,
            },
            {
                "sales_order_id": 2,
                "created_date": "2022-01-01",
                "created_time": "14:20:52.186000",
                "last_updated_date": "2022-01-03",
                "last_updated_time": "14:20:52.186000",
                "sales_staff_id": 1,
                "counterparty_record_id": 1,
                "units_sold": 2,
                "unit_price": 99999999.00,
                "currency_record_id": 1,
                "design_record_id": 1,
                "agreed_payment_date": '2022-01-01',
                "agreed_delivery_date": '2022-01-01',
                "agreed_delivery_location_id": 1,
            },
        ]


tables_data={}
tables_data['dim_currency']=pd.DataFrame(data_currency)
tables_data['dim_location']=pd.DataFrame(data_location)
tables_data['dim_counterparty']=pd.DataFrame(data_counterparty)
tables_data['dim_date']=pd.DataFrame(data_date)
tables_data['dim_design']=pd.DataFrame(data_design)
tables_data['dim_payment_type']=pd.DataFrame(data_payment_type)
tables_data['dim_staff']=pd.DataFrame(data_staff)
tables_data['dim_transaction']=pd.DataFrame(data_transaction)

tables_data['fact_sales_order']=pd.DataFrame(data_fact_sales)
# tables_data['fact_payment']=pd.DataFrame(data_fact_payment)
# tables_date['fact_purchase_order']

# tables_columns={}
# tables_columns['dim_currency']=['currency_record_id','currency_id','currency_code',
#     'currency_name','last_updated_date','last_updated_time']
# tables_columns['fact_sales_order']=["sales_order_id",
#                 "created_date",
#                 "created_time",
#                 "last_updated_date",
#                 "last_updated_time",
#                 "sales_staff_id",
#                 "counterparty_record_id",
#                 "units_sold",
#                 "unit_price",
#                 "currency_record_id",
#                 "design_record_id",
#                 "agreed_payment_date",
#                 "agreed_delivery_date",
#                 "agreed_delivery_location_id"]
# tables_columns['dim_location']=[
#         "location_id",
#         "address_line_1",
#         "address_line_2",
#         "district",
#         "city",
#         "postcode",
#         "country",
#         "phone",
#     ]
# tables_columns=['transaction_record_id','transaction_id','transaction_type','sales_order_id','purchase_order_id','last_updated_date',
#     'last_updated_time']


def sql_query(conn:Connection,tables_data:dict):

# for table in tables_data:
#     for index, row in tables_data[table].iterrows():
#         values = ', '.join([f"'{value}'" for value in row.values])
#         sql_query = f"INSERT INTO {table} ({tables_columns[table]}) VALUES ({values})"
#         conn.run(sql_query)
    for table in tables_data:
        conn.run(f"DELETE FROM {table}")
        table_columns = tables_data[table].columns.to_list()  # Get the list of columns for the current table
        for index, row in tables_data[table].iterrows():
            # Construct the column list as a comma-separated string
            columns_str = ', '.join(table_columns)
            # Construct the values list for the current row
            values_str = ', '.join([f"'{value}'" for value in row.values])
            # Construct the SQL INSERT statement
            sql_query = f"INSERT INTO {table} ({columns_str}) VALUES ({values_str})"
            # Execute the SQL query
            conn.run(sql_query)

    
                    

    
    # conn.close()
    

























   
sql_query(conn,tables_data)

sql="DELETE FROM dim_currency WHERE currency_id IN (0,1,2,3,4,5,6,7,8)"
# conn.run(sql)
conn.close()