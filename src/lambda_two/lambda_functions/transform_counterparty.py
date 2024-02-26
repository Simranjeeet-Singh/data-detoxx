from utils.join_data_frames import left_join_df
from utils.join_data_frames import column_filter
import pandas as pd



def dim_counterparty(df_counterparty:pd.DataFrame,df_address:pd.DataFrame):
    """
    This function tranforms the counterparty_table into the dim_counterparty_table as needed for the final scheme in
    the data warehouse, by pulling in the required data from the address_table.
    This function makes use of two functions-
        left_join_df-->which performs the left join on the two dataframes supplied to it with the foreign key referenced as 'counterparty_address_id'
        in counterparty_table and referred to as 'address_id'.

        column_filter-->filtering the columns from the dataframes and renaming them as per requirement of our new schema.

    Input:
    df_counterparty(pd.DataFrame)->The dataframe storing the counterparty_table as in the database.
    df_address(pd.DataFrame)->The dataframe storing the address_table as in the database.

    Output:
    filtered_df(pd.DataFrame)->The final dataframe pointing to the table in the Data warehouse as per the schema.
    """
    if len(df_counterparty.columns.to_list())==0 or len(df_address.columns.to_list())==0:
        return pd.DataFrame()
    df_address.fillna({'district': 'N/A'}, inplace=True)
    df_address.fillna({'address_line_2': 'N/A'}, inplace=True)
    df_counterparty.to_csv('./counterparty.csv')
    df_address.to_csv('./address.csv')
    merged_df=left_join_df(df_counterparty,df_address,'legal_address_id','address_id')
    #df_counterparty.merge(df_address)
    columns_needed_table1=['counterparty_id','counterparty_legal_name']
    columns_needed_table2=['address_line_1','address_line_2','district','city','postal_code','country','phone']
    filtered_df=column_filter(merged_df,['table1_'+field for field in columns_needed_table1]+['table2_'+field for field in columns_needed_table2],
                    ['counterparty_id','counterparty_legal_name','counterparty_legal_address_line_1','counterparty_legal_address_line_2', 
                            'counterparty_legal_district','counterparty_legal_city','counterparty_legal_postal_code','counterparty_legal_country','counterparty_legal_phone_number'])
    return filtered_df
