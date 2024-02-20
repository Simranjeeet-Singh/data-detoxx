from src.transform_staff_table import transform_staff_table
import pandas as pd
from unittest.mock import patch

def test_returns_correct_dataframe():
    staff_df = pd.DataFrame([[1, 'Jeremie', 'Franey', 2, 'jeremie.franey@terrifictotes.com', '2022-11-03 14:20:51.563','2022-11-03 14:20:51.563'],
                         [2, 'Deron', 'Beier', 3 , 'deron.beier@terrifictotes.com', '2022-11-03 14:20:51.563','2022-11-03 14:20:51.563'],
                         [3, 'Jeanette', 'Erdman', 1, 'jeanette.erdman@terrifictotes.com', '2022-11-03 14:20:51.563','2022-11-03 14:20:51.563']])
    staff_df.columns = ['staff_id','first_name','last_name','department_id','email_address','created_at','last_updated']
    department_df = pd.DataFrame([[1,'Sales','Manchester','Richard Roma','2022-11-03 14:20:49.962','2022-11-03 14:20:49.962'],
                              [2,'Purchasing','Manchester','Naomi Lapaglia','2022-11-03 14:20:49.962','2022-11-03 14:20:49.962'],
                              [3,'Production','Leeds','Chester Ming','2022-11-03 14:20:49.962','2022-11-03 14:20:49.962']])
    department_df.columns = ['department_id','department_name','location','manager','created_at','last_updated']
    output = transform_staff_table(staff_df,department_df).to_dict()
    expected_output = {'department_name': {0: 'Purchasing', 1: 'Production', 2: 'Sales'},
                        'email_address': {0: 'jeremie.franey@terrifictotes.com',
                                        1: 'deron.beier@terrifictotes.com',
                                        2: 'jeanette.erdman@terrifictotes.com'},
                        'first_name': {0: 'Jeremie', 1: 'Deron', 2: 'Jeanette'},
                        'last_name': {0: 'Franey', 1: 'Beier', 2: 'Erdman'},
                        'location': {0: 'Manchester', 1: 'Leeds', 2: 'Manchester'},
                        'staff_id': {0: 1, 1: 2, 2: 3}}
    assert output == expected_output