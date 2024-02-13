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
    Extract all rows from the currency SQL table
    Inputs them in a pandas dataframe
    Saves the dataframe to a .csv file
    '''
    load_dotenv()
    conn = Connection(
        host=os.environ["Hostname"],
        user=os.environ["Username"],
        password=os.environ["Password"],
        database=os.environ["Database_name"],
        port=os.environ["Port"],
    )
    rows=conn.run('SELECT * FROM currency;')
    cols_name_nested=conn.run('''SELECT COLUMN_NAME 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE 
TABLE_NAME = 'currency'
''')
    cols_name=[el[0] for el in cols_name_nested]
    conn.close()
    df=pd.DataFrame(rows)
    df.index=df[0].values
    df.columns=cols_name
    df.to_csv('./file.csv', sep=',', index=False, encoding='utf-8')

if __name__ == "__main__":
    save_db_to_csv()