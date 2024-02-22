import pandas as pd

# Ignore warning when running unit-test
pd.options.mode.chained_assignment = None

def transform_staff_table(staff_df: pd.DataFrame, department_df: pd.DataFrame) -> pd.DataFrame:
    ''' 
    Parameters:
    - staff_df (DataFrame): The `DataFrame` containing staff information.
    - department_df (DataFrame): The `DataFrame` containing department information.

    Returns:
    - DataFrame: A new `DataFrame` with the following columns:
        `staff_id`,`first_name`,`last_name`,`department_name`,`location`,`email_address`
    '''
    transformed_df = pd.DataFrame([])
    merged_df = staff_df.merge(department_df, on='department_id', how='left')
    transformed_df = merged_df[['staff_id', 'first_name',
                                'last_name', 'department_name', 'location', 'email_address']]
    transformed_df.fillna({'location': 'N/A'}, inplace=True)
    
    return transformed_df