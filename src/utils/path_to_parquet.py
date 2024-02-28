def path_to_parquet(table_name: str, counter: int, last_updated: str) -> str:
    """
    Generates a file path for storing a Parquet file.

    Args:
        `table_name`: The name of the table.
        `counter`: An integer counter for versioning or distinguishing files.
        `last_updated`: A string representing the date of the last updated table

    Returns:
        `str`: A string representing the file path in the format:
            "{table_name}/{table_name}__[#{counter}]__{last_updated}.parquet"
            where {table_name} is the name of the table,
            {counter} is the version or counter value,
            and {last_updated} is the date of the last updated table.
    """
    return f"{table_name}/{table_name}__[#{counter}]__{last_updated}.parquet"
