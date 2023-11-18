from survival_analysis.database_preparation.sql_interactions import SqlHandler
from survival_analysis.model_preparation.model_AFT import AFTModelSelector
from survival_analysis.utils import format_dataframe
import pandas as pd


#Initiate the connection
Inst=SqlHandler('sa_db', 'DimCustomer')

#Get data in dataframe format
df = Inst.from_sql_to_pandas(chunksize=100, id_value = 'Customer_ID')

#Close the connection
Inst.close_cnxn()

#Format the data - dummifying categorical variables
df = format_dataframe(df)

'''
pseudo_model = PseudoModel(df)
result_df = pseudo_model.pseudo_model('Customer_ID')
'''

#Running the AFT model for next 12 time periods
duration_column = 'Tenure'
event_column = 'Churn_Yes'
primary = 'Customer_ID'

aft_model_selector = AFTModelSelector(df, primary, duration_column, event_column)
aft_model_selector.select_best_model()
aft_model_selector.fit_and_predict(n_time_periods=12)
aft_model_selector.calculate_clv()

# Save the results to a CSV file

#For Windows
aft_model_selector.predictions_df.to_csv('Raw Data\model_output.csv', index=False)

#For MAC
#aft_model_selector.predictions_df.to_csv('Raw Data/model_output.csv', index=False)

# Get Data

#For Windows
data =pd.read_csv(r'Raw Data\model_output.csv')

#For MAC
#data =pd.read_csv(r'Raw Data/model_output.csv')

#Making sure the table does not contain previous results
#Insert Data to FactPredictions
Inst=SqlHandler('sa_db', 'FactPredictions')


Inst.truncate_table() # for deleting table contents
#Inst.get_table_columns() - for getting column names

Inst.close_cnxn()


#Inserting the results to DB

Inst=SqlHandler('sa_db', 'FactPredictions')

Inst.insert_many(data)

#Close the connection
Inst.close_cnxn()
