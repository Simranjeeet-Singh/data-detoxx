import pprint
from pg8000.native import Connection, identifier, literal
from dotenv import load_dotenv
import os
from utils.utils import *


def connect():
    load_dotenv()
    con = Connection(
        host=os.environ["Hostname"],
        user=os.environ["Username"],
        password=os.environ["Password"],
        database=os.environ["Database_name"],
        port=os.environ["Port"],
    )
    sql_query = f"SELECT * FROM currency;"
    sql_results = con.run(sql_query)
    con.close()
    return sql_results


if __name__ == "__main__":
    print(connect())
