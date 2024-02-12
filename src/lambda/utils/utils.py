import pprint
from pg8000.native import Connection, identifier, literal
from dotenv import load_dotenv
import os


def return_safe_sql_identifiers_str_from_list(list_of_identifiers: list) -> str:
    safe_identifiers_str = ""
    for index, value in enumerate(list_of_identifiers):
        if index == len(list_of_identifiers) - 1:
            str_to_add = identifier(value)
        else:
            str_to_add = f"{identifier(value)}, "
        safe_identifiers_str = safe_identifiers_str + str_to_add
    return safe_identifiers_str


def return_list_of_dicts_from_sql_results(results_list: list, keys: list) -> dict:
    list_of_dicts = []
    for values in results_list:
        result_dict = dict(zip(keys, values))
        list_of_dicts.append(result_dict)
    return list_of_dicts


def select_movies(sort_by="title", order="ASC", min_rating=None, location=None) -> list:

    load_dotenv()
    con = Connection(
        user=os.environ["USER"], password=os.environ["PASSWORD"], database="nc_flix"
    )

    columns_to_select = [
        "movie_id",
        "title",
        "release_date",
        "rating",
        "classification",
        "cost",
        "city",
    ]

    columns_to_select_sql_str = return_safe_sql_identifiers_str_from_list(
        columns_to_select
    )

    order = order.upper()
    if order not in ["ASC", "DESC"]:
        order = "ASC"

    sql_query = f"SELECT movies.*, city FROM movies "
    if location:
        sql_query += f"JOIN stock ON movies.movie_id = stock.movie_id JOIN stores ON stock.store_id = stores.store_id WHERE city = {literal(location)} "
    if min_rating:
        if location:
            sql_query += "AND "
        sql_query += f"WHERE rating > {literal(min_rating)} "
    sql_query += f"ORDER BY movies.{identifier(sort_by)} {order}"

    print(sql_query)

    sql_results = con.run(sql_query)

    con.close()

    list_of_movie_dicts = return_list_of_dicts_from_sql_results(
        sql_results, columns_to_select
    )

    pprint(list_of_movie_dicts)

    return list_of_movie_dicts
