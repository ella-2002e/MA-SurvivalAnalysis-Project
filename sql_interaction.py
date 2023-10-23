from survival_analysis.database_preparation.sql_interactions import SqlHandler
import pandas as pd

# Get Data

data=pd.read_csv(r'survival_analysis\Raw Data\telco.csv')

#Insert Data to DimCustomer
Inst=SqlHandler('sa_db', 'DimCustomer')

# Inst.truncate_table() - for deleting table contents
#Inst.get_table_columns() - for getting column names
Inst.insert_many(data)

#Close the connection
Inst.close_cnxn()




