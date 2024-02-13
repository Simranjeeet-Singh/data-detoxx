import pprint
from pg8000.native import Connection, identifier, literal
import pandas as pd
from dotenv import load_dotenv
import os
from utils.utils import *

def extract_tablenames( conn: Connection) -> list[str]:
    '''
    Given a pg8000.native Connection object to a SQL db, returns the names of all its tables in a list.
    '''
    sql_query_tablenames='''SELECT table_name
    FROM information_schema.tables
    WHERE table_schema='public'
    AND table_type='BASE TABLE';'''
    return [el[0] for el in conn.run(sql_query_tablenames) if el[0]!='_prisma_migrations']

def save_table_to_csv(conn: Connection, table_name: str) -> None:
    '''
    Given a pg8000.native Connection object to a SQL db, and the name of one of its tables,
    stores the rows of the table in a pandas dataframe and saves it to a .csv file of the same name.
    ''' 
    rows=conn.run(f'SELECT * FROM {identifier(table_name)};')
    cols_name=[el['name'] for el in conn.columns]
    df=pd.DataFrame(rows)
    df.index=df[0].values
    df.columns=cols_name
    df.to_csv(f'./csv/{table_name}.csv', sep=',', index=False, encoding='utf-8')

def save_db_to_csv( var : None = None) -> None:
    '''
    Connects to a server specified in the .env variable via pg8000.native
    Extract all rows from all its SQL tables
    Inputs them in pandas dataframes
    Saves each dataframe to .csv files with same name as table
    '''
    load_dotenv()
    conn = Connection(
        host=os.environ["Hostname"],
        user=os.environ["Username"],
        password=os.environ["Password"],
        database=os.environ["Database_name"],
        port=os.environ["Port"],
    )
    tablenames=extract_tablenames(conn)
    for table_name in tablenames:
        save_table_to_csv(conn, table_name)
    conn.close()

if __name__ == "__main__":
    save_db_to_csv()