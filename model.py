from survival_analysis.database_preparation.sql_interactions import SqlHandler
from survival_analysis.model_preparation.utils import PseudoModel
import pandas as pd


#Initiate the connection
Inst=SqlHandler('sa_db', 'DimCustomer')

#get data in dataframe format
df = Inst.from_sql_to_pandas(chunksize=1, id_value = 'customer_id')

#Close the connection
Inst.close_cnxn()


pseudo_model = PseudoModel(df)
result_df = pseudo_model.pseudo_model('Customer_ID')

# Save the results to a CSV file

#For Windows
#result_df.to_csv('survival_analysis\Raw Data\model_output.csv', index=False)

#For MAC
result_df.to_csv('survival_analysis/Raw Data/model_output.csv', index=False)

# Get Data

#For Windows
#data =pd.read_csv(r'survival_analysis\Raw Data\model_output.csv')

#For MAC
data =pd.read_csv(r'survival_analysis/Raw Data/model_output.csv')

#Insert Data to DimCustomer
Inst=SqlHandler('sa_db', 'FactPredictions')

# Inst.truncate_table() - for deleting table contents
# Inst.get_table_columns() - for getting column names
Inst.insert_many(data)

#Close the connection
Inst.close_cnxn()



