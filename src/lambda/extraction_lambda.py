import pprint
from pg8000.native import Connection, identifier, literal
import pandas as pd
from dotenv import load_dotenv
import os
from utils.utils import *


def save_db_to_csv():
    '''
    Null -> Null
    This function connects to a server specified in the .env variable via pg8000.native
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
    sql_query_tablenames='''SELECT table_name
    FROM information_schema.tables
    WHERE table_schema='public'
    AND table_type='BASE TABLE';'''
    tablenames=[el[0] for el in conn.run(sql_query_tablenames) if el[0]!='_prisma_migrations']
    for name in tablenames:
        rows=conn.run(f'SELECT * FROM {identifier(name)};')
        cols_name=[el['name'] for el in conn.columns]
        df=pd.DataFrame(rows)
        df.index=df[0].values
        df.columns=cols_name
        df.to_csv(f'./csv/{name}.csv', sep=',', index=False, encoding='utf-8')
    conn.close()
if __name__ == "__main__":
    save_db_to_csv()