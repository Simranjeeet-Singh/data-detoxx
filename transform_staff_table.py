import pandas as pd

def transform_staff_table(staff_df, department_df):
    pass



staff_df = pd.DataFrame([[1, 'Jeremie', 'Franey', 2, 'jeremie.franey@terrifictotes.com', '2022-11-03 14:20:51.563','2022-11-03 14:20:51.563'],
                         [2, 'Deron', 'Beier', 6, 'deron.beier@terrifictotes.com', '2022-11-03 14:20:51.563','2022-11-03 14:20:51.563'],
                         [3, 'Jeanette', 'Erdman', 6, 'jeanette.erdman@terrifictotes.com', '2022-11-03 14:20:51.563','2022-11-03 14:20:51.563']])
staff_df.columns = ['staff_id','first_name','last_name','department_id','email_address','created_at','last_updated']

department_df = pd.DataFrame([[1,'Sales','Manchester','Richard Roma','2022-11-03 14:20:49.962','2022-11-03 14:20:49.962'],
                              [1,'Sales','Manchester','Richard Roma','2022-11-03 14:20:49.962','2022-11-03 14:20:49.962']])
department_df.columns = ['department_id','department_name','location','manager','created_at','last_updated']

print(staff_df.to_markdown())
print(department_df.to_markdown())