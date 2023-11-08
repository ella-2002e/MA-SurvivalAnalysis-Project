from survival_analysis.database_preparation.sql_interactions import SqlHandler
import pandas as pd


# Get Data From CSV

# For Mac Users
data = pd.read_csv(r'Raw Data/telco.csv')

# For Windows users
# data = pd.read_csv(r'Raw Data\telco.csv')

# Insert Data to DimCustomer
Inst = SqlHandler('sa_db', 'DimCustomer')
Inst.insert_many(data) 

"""
UNCOMMENT THE BELOW IF NEEDED
"""
# Inst.truncate_table() - for deleting table contents

# Inst.get_table_columns() - for getting column names

#new_dict = {"Customer_ID": 1003, "Age": 67, "Gender": "Male", "Tenure": 5, "Income": 88}
#Inst.insert_one(new_dict) - for adding a new row to thedatabase

#set_dict = {"Gender": "Female", "Age": 45}
#cond_dict = {"Customer_ID": "= 1400"}
#Inst.update_table(set_dict, cond_dict) - for updating the database based on some condition

# Close the connection
Inst.close_cnxn()

