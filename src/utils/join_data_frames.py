import pandas as pd


def left_join_df(
    df_table_1: pd.DataFrame,
    df_table_2: pd.DataFrame,
    foreign_key_1: str,
    foreign_key_2="",
) -> pd.DataFrame:
    """
    The function does a left join on two tables which are passed to it in the form of data frames.

    Inputs:
    df_table_1,df_table_2-(pd.DataFrame) data frames in form of list os lists representing two tables that are to be joined
    foreign_key_1(str)-Name of the column in df1 which is referencing to foreign_key_2 in df2
    foreign_key_2(Optional)-(str)Name of the column in df2 which is referencing to foreign_key_1 in df1, if the foreign key is referenced with same name in
    both tables then this argument can be ignored.


    Outputs:
    merged_df-(pd.DataFrame) -> The merged table is the result of the left join with column names having prefix of 'table1_','table2_' to add information
    about the table the column refrences to.


    """
    try:
        if foreign_key_2 == "":
            foreign_key_2 = foreign_key_1
        df_table_1.columns = ["table1_" + field for field in df_table_1.columns]
        df_table_2.columns = ["table2_" + field for field in df_table_2.columns]
        merged_df = pd.merge(
            df_table_1,
            df_table_2,
            left_on="table1_" + foreign_key_1,
            right_on="table2_" + foreign_key_2,
        )
        return merged_df
    except Exception as e:
        print(e)
        return e


def column_filter(
    df_table: pd.DataFrame, columns_filter=[], columns_renamed=[]
) -> pd.DataFrame:
    """
    This function transforms a table in data frame in 2 ways.
    Firstly, it filters out the columns that we need.
    Secondly, it renames the name of the columns that are filtered.


    Input :
    df_table - (data frame) ->The table in form of data frame which is to be tranformed.
    columns_filter - (list) -> THe  list of columns that need to be filtered from the table
    columns_renamed - (list) -> The list of new names for the columns that are filtered. This is an optional argument, if this is not passed then
                            the columns retain the same names.

    Output :
    df_final_table(Optional) - (data frame) -> The final transformed table in form of data frame.

    """
    try:

        if columns_renamed == []:
            columns_renamed = columns_filter
        if columns_filter == []:
            return df_table

        if len(columns_renamed) != len(columns_filter):
            raise ValueError(
                "The columns to be filtered have a different length than the new names you want to assign to them with columns_renamed list"
            )
        if False in [
            bool(field in df_table.columns.to_list()) for field in columns_filter
        ]:
            raise Exception(
                "The column name in columns_filter list is not found inside the data frame"
            )

        df_final_table = pd.DataFrame()
        for field in columns_filter:
            new_field = columns_renamed[columns_filter.index(field)]
            df_final_table[new_field] = df_table[field].copy()
        print(df_table, df_final_table, sep="\n")
        return df_final_table

    except ValueError as e:
        print(e)
        raise e

    except Exception as e:
        print(e)
        raise e
