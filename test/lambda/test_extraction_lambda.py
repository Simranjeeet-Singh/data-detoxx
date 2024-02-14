from src.lambda_functions.extraction_lambda import extract_tablenames, save_table_to_csv, save_db_to_csv, convert_to_utc
from unittest.mock import patch, Mock
import datetime
import pandas as pd

def test_import_works():
    assert True

def test_extract_tablenames_one_table():
    '''
    extract_tablenames extracts names from db with one table
    '''
    with patch("src.lambda_functions.extraction_lambda.Connection") as conn_patched:
        conn_patched.run.return_value=[['ciao']]
        assert extract_tablenames(conn_patched)==['ciao']

def test_extract_tablenames_zero_tables():
    '''
    extract_tablenames extracts names from db with zero tables
    '''
    with patch("src.lambda_functions.extraction_lambda.Connection") as conn_patched:
        conn_patched.run.return_value=[]
        assert extract_tablenames(conn_patched)==[]

def test_extract_tablenames_many_tables():
    '''
    extract_tablenames extracts names from db with many tables,
    including a "_prisma_migrations" that should not be extracted
    '''
    with patch("src.lambda_functions.extraction_lambda.Connection") as conn_patched:
        conn_patched.run.return_value=[['a'],['b'],['c'],['d'],['e'],['_prisma_migrations'],['f']]
        assert extract_tablenames(conn_patched)==['a','b','c','d','e','f']

def test_save_table_empty_table():
    '''
    Check that pandas is not called if we don't get any rows from the db query
    '''
    with patch("src.lambda_functions.extraction_lambda.Connection") as conn_patched:
        conn_patched.run.return_value=[]
        conn_patched.columns=[]
        with patch("src.lambda_functions.extraction_lambda.pd.DataFrame") as mock_df:
            save_table_to_csv(conn_patched, 'table','daste','0')
            mock_df.assert_not_called()

# def test_save_table_table_with_one_row():
#     '''
#     Check that pandas is called if we get one row from the db query
#     '''
#     with patch("src.lambda_functions.extraction_lambda.Connection") as conn_patched:
#         conn_patched.run.return_value=[['mock','data','nah','2024-02-13 18:19:09.733']]
#         conn_patched.columns=[{'name':'id'},{'name':'data'},{'name':'yayornay'},{'name':'last_updated'}]
#     with patch("src.lambda_functions.extraction_lambda.pd.DataFrame") as mock_df:
#         mock_df.return_value = pd.DataFrame([{'id':'mock','data':'data','yayornay':'nah','last_updated': '2024-02-13 18:19:09.733'}])
#         print(mock_df.return_value.iloc[-1]['last_updated'])
#         assert False
#         # save_table_to_csv(conn_patched, 'table','data','2024-02-13 18:19:09.700')
#         # mock_df.assert_called_once_with([['mock','data','nah','2024-02-13 18:19:09.733']])

# def test_save_table_table_with_three_rows():
#     '''
#     Check that pandas is called if we get three row from the db query
#     '''
#     with patch("src.lambda_functions.extraction_lambda.Connection") as conn_patched:
#         conn_patched.run.return_value=[['mock','data','nah'],['mock','data','nah'],['mock','data','nah']]
#         conn_patched.columns=[{'name':'id'},{'name':'data'},{'name':'yayornay'}]
#         with patch("src.lambda_functions.extraction_lambda.pd.DataFrame") as mock_df:
#                 save_table_to_csv(conn_patched, 'table','data',0)
#                 mock_df.assert_called_once_with([['mock','data','nah'],['mock','data','nah'],['mock','data','nah']])
