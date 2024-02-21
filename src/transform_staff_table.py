import pandas as pd


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
    return transformed_df


staff_df = pd.DataFrame([[1, 'Jeremie', 'Franey', 2, 'jeremie.franey@terrifictotes.com', '2022-11-03 14:20:51.563', '2022-11-03 14:20:51.563'],
                         [2, 'Deron', 'Beier', 3, 'deron.beier@terrifictotes.com',
                             '2022-11-03 14:20:51.563', '2022-11-03 14:20:51.563'],
                         [3, 'Jeanette', 'Erdman', 1, 'jeanette.erdman@terrifictotes.com', '2022-11-03 14:20:51.563', '2022-11-03 14:20:51.563']])
staff_df.columns = ['staff_id', 'first_name', 'last_name',
                    'department_id', 'email_address', 'created_at', 'last_updated']

department_df = pd.DataFrame([[1, 'Sales', 'Manchester', 'Richard Roma', '2022-11-03 14:20:49.962', '2022-11-03 14:20:49.962'],
                              [2, 'Purchasing', 'Manchester', 'Naomi Lapaglia',
                                  '2022-11-03 14:20:49.962', '2022-11-03 14:20:49.962'],
                              [3, 'Production', 'Leeds', 'Chester Ming', '2022-11-03 14:20:49.962', '2022-11-03 14:20:49.962']])
department_df.columns = ['department_id', 'department_name',
                         'location', 'manager', 'created_at', 'last_updated']
