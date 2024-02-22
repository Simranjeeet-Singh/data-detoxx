
from join_data_frames import left_join_df
from join_data_frames import column_filter
import pandas as pd



def dim_counterparty(df_counterparty,df_address):
    merged_df=left_join_df(df_counterparty,df_address,'counterparty_address_id','address_id')

    columns_needed_table1=['counterparty_id','counterparty_legal_name']
    columns_needed_table2=['address_line_1','address_line_2','district','city','postal_code','country','phone']
    filtered_df=column_filter(merged_df,['table1_'+field for field in columns_needed_table1]+['table2_'+field for field in columns_needed_table2],
                            ['counterparty_id','counterparty_legal_name','counterparty_legal_address_line_1','counterparty_legal_address_line_2', 
                            'counterparty_legal_district','counterparty_legal_city','counterparty_legal_postal_code','counterparty_legal_country','counterparty_legal_phone_number'])
    return filtered_df
    









counterparty_df=pd.DataFrame([[1,'Fahey and Sons',15,'Micheal Toy','Mrs. Lucy Runolfsdottir','2022-11-03 14:20:51.563','2022-11-03 14:20:51.563'],
                              [2,"Leannon,'Predovic and Morar",28,'Melba Sanford','Jean Hane III','2022-11-03 14:20:51.563','2022-11-03 14:20:51.563'],
                              [3,'Armstrong Inc',2,'Jane Wiza','Myra Kovacek','2022-11-03 14:20:51.563','2022-11-03 14:20:51.563']
                              ])
counterparty_df.columns=['counterparty_id','counterparty_legal_name','counterparty_address_id','commercial_contact','delivery_contact','created_at','last_updated']
address_df=pd.DataFrame([
                         [1,'6826 Herzog Via','N/A','Avon','New Patienceburgh','28441''Turkey','1803 637401''2022-11-03 14:20:49.962','2022-11-03 14:20:49.962'],
                         [2,'179 Alexie Cliffs','N/A','N/A','Aliso Viejo','99305-7380','San Marino','9621 880720','2022-11-03 14:20:49.962','2022-11-03 14:20:49.962'],
                         [7,'148 Sincere Fort','N/A','N/A','Lake Charles','89360','Samoa''0730 783349','2022-11-03 14:20:49.962','2022-11-03 14:20:49.962'],
                         [15,'6102 Rogahn Skyway','N/A','Bedfordshire','Olsonside','47518','Republic of Korea','1239 706295','2022-11-03 14:20:49.962','2022-11-03 14:20:49.962'],
                         [19,'34177 Upton Track','N/A','N/A','Fort Shadburgh','55993-8850','Bosnia and Herzegovina','0081 009772','2022-11-03 14:20:49.962','2022-11-03 14:20:49.962'],
                         [21,'846 Kailey Island','N/A','N/A','Kendraburgh','08841','Zimbabwe','0447 798320','2022-11-03 14:20:49.962','2022-11-03 14:20:49.962'],
                         [21,'846 Kailey Island','N/A','N/A','Kendraburgh','08841','Zimbabwe','0447 798320','2022-11-03 14:20:49.962','2022-11-03 14:20:49.962'],
                         [21,'846 Kailey Island','N/A','N/A','Kendraburgh','08841','Zimbabwe','0447 798320','2022-11-03 14:20:49.962','2022-11-03 14:20:49.962'],
                         [21,'846 Kailey Island','N/A','N/A','Kendraburgh','08841','Zimbabwe','0447 798320','2022-11-03 14:20:49.962','2022-11-03 14:20:49.962'],
                         [28,'75653 Ernestine Ways','N/A','Buckinghamshire','North Deshaun','02813','Faroe Islands','1373 796260','2022-11-03 14:20:49.962','2022-11-03 14:20:49.962']
                         ])
address_df.columns=['address_id','address_line_1','address_line_2','district','city','postal_code','country','phone','created_at','last_updated']

dim_counterparty.columns=['counterparty_id','counterparty_legal_name','counterparty_legal_address_line_1','counterparty_legal_address_line_2', 
                          'counterparty_legal_district','counterparty_legal_city','counterparty_legal_postal_code','counterparty_legal_country','counterparty_legal_phone_number']

print(dim_counterparty(counterparty_df,address_df))