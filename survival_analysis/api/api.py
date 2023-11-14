from fastapi import FastAPI, HTTPException, Query
import sqlite3
import logging
from ..logger import CustomFormatter
from ..database_preparation import SqlHandler
import os
import pandas as pd
from fastapi import Path
from typing import Any, List, Union, Optional
#from pydantic import BaseModel

app = FastAPI()
    
logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

# logger.debug("debug message")
# logger.info("Warning: Email has not been sent......")
# logger.warning("warning message")
# logger.error("error message")
# logger.critical("critical message")

# Creating instances of SqlHandler for each table
dim_customer_handler = SqlHandler(dbname='sa_db', table_name='DimCustomer')
fact_predictions_handler = SqlHandler(dbname='sa_db', table_name='FactPredictions')

# Defining functions to open connections to the databases
def get_dim_customer_db():
    return dim_customer_handler.cnxn

def get_fact_predictions_db():
    return fact_predictions_handler.cnxn

@app.on_event("shutdown")
async def shutdown_event():
    # Closing the database connections on shutdown
    dim_customer_handler.close_cnxn()
    fact_predictions_handler.close_cnxn()

@app.get("/")
async def root():
    return {
        """
            Initializing API for Survival Analysis project with selecting data from database, inserting data, and updating data. It now contains also several endpoints that help to identify top customers with the highest churn rate, customers with the highest/lowest CLV.
        """
    }


@app.get("/get_dim_customer/{customer_id}")
async def get_dim_customer_record(customer_id: int):
    handler = dim_customer_handler

    # Calling the from_sql_to_pandas function to get the data
    data = handler.from_sql_to_pandas(chunksize=1000, id_value='Customer_ID')

    # Filtering the data based on the customer_id
    record = data[data['Customer_ID'] == customer_id].to_dict(orient='records')

    if not record:
        return {"error": "Record not found"}

    return record[0]

@app.get("/get_fact_predictions/{customer_id}")
async def get_fact_predictions_record(customer_id: int, pred_period: int):
    handler = fact_predictions_handler

    # Calling the from_sql_to_pandas function to get the data
    data = handler.from_sql_to_pandas(chunksize=1000, id_value='customer_ID')

    # Filtering the data based on the customer_id and pred_period if applicable
    if pred_period is None:
        return {"error": "Missing pred_period for FactPredictions"}

    record = data[(data['customer_ID'] == customer_id) & (data['pred_period'] == pred_period)].to_dict(orient='records')

    if not record:
        return {"error": "Record not found"}

    return record[0]


@app.post("/create_dim_customer/{customer_id}")
async def create_dim_customer_record(customer_id: int, new_data: Union[dict, List[dict]]):
    try:
        # Selecting the appropriate SqlHandler instance based on the table_name
        handler = dim_customer_handler

        # Checking if the input data is a list of dictionaries, then use insert_many
        if isinstance(new_data, list):
            # Ensuring that the customer_id is set for each record
            for record in new_data:
                record['Customer_ID'] = customer_id
            handler.insert_many(pd.DataFrame(new_data))
        elif isinstance(new_data, dict):
            # Setting the customer_id for the single record
            new_data['Customer_ID'] = customer_id
            handler.insert_one(new_data)
        else:
            return {"error": "Invalid input format"}

        return {"message": "Record(s) created successfully"}
    except Exception as e:
        logger.error(f"Failed to insert data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to insert data: {str(e)}")

@app.post("/create_fact_predictions/{customer_id}/{pred_period}")
async def create_fact_predictions_record(customer_id: int, pred_period: int, new_data: Union[dict, List[dict]]):
    try:
        # Selecting the appropriate SqlHandler instance based on the table_name
        handler = fact_predictions_handler

        # Checking if the input data is a list of dictionaries, then use insert_many
        if isinstance(new_data, list):
            # Ensuring that the customer_id and pred_period are set for each record
            for record in new_data:
                record['customer_ID'] = customer_id
                record['pred_period'] = pred_period
            handler.insert_many(pd.DataFrame(new_data))
        elif isinstance(new_data, dict):
            # Setting the customer_id and pred_period for the single record
            new_data['customer_ID'] = customer_id
            new_data['pred_period'] = pred_period
            handler.insert_one(new_data)
        else:
            return {"error": "Invalid input format"}

        return {"message": "Record(s) created successfully"}
    except Exception as e:
        logger.error(f"Failed to insert data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to insert data: {str(e)}")

@app.put("/update_dim_customer/{customer_id}")
async def update_dim_customer_record(customer_id: int, update_request: dict):
    try:
        # Selecting the appropriate SqlHandler instance based on the table_name
        handler = dim_customer_handler

        # Initializing set_dict and cond_dict
        set_dict = {}
        cond_dict = {}

        # Ensuring required fields are present in the request for DimCustomer
        required_fields_dim = {'column_name', 'new_value'}
        if not required_fields_dim.issubset(update_request.keys()):
            return {"error": "Missing required fields in the request for DimCustomer"}

        # Converting request data to dictionaries for set_dict and cond_dict
        set_dict = {update_request['column_name']: update_request['new_value']}
        cond_dict = {'customer_id': customer_id}

        # Logging the details before the update
        logger.info(f"Before update - Table: DimCustomer, Set: {set_dict}, Condition: {cond_dict}")

        # Calling the update_table method to update the record
        handler.update_table(set_dict=set_dict, cond_dict=cond_dict)

        # Logging the details after the update
        logger.info(f"After update - Table: DimCustomer, Set: {set_dict}, Condition: {cond_dict}")

        return {"message": "Record updated successfully"}
    except Exception as e:
        logger.error(f"Failed to update data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update data: {str(e)}")

@app.put("/update_fact_predictions/{customer_id}/{pred_period}")
async def update_fact_predictions_record(customer_id: int, pred_period: int, update_request: dict):
    try:
        # Selecting the appropriate SqlHandler instance based on the table_name
        handler = fact_predictions_handler

        # Initializing set_dict and cond_dict
        set_dict = {}
        cond_dict = {}

        # Ensuring required fields are present in the request for FactPredictions
        required_fields = {'column_name', 'new_value'}
        if not required_fields.issubset(update_request.keys()):
            return {"error": "Missing required fields in the request for FactPredictions"}

        # Converting request data to dictionaries for set_dict and cond_dict
        set_dict = {update_request['column_name']: update_request['new_value']}
        cond_dict = {'customer_id': customer_id, 'pred_period': pred_period}

        # Logging the details before the update
        logger.info(f"Before update - Table: FactPredictions, Set: {set_dict}, Condition: {cond_dict}")

        # Calling the update_table method to update the record
        handler.update_table(set_dict=set_dict, cond_dict=cond_dict)

        # Logging the details after the update
        logger.info(f"After update - Table: FactPredictions, Set: {set_dict}, Condition: {cond_dict}")

        return {"message": "Record updated successfully"}
    except Exception as e:
        logger.error(f"Failed to update data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update data: {str(e)}")
    

## Adding endpoints for different scenarios

@app.get("/get_top_10p_churn_customers")
async def get_top_churn_customers():
    try:
        handler = fact_predictions_handler

        # Calling the from_sql_to_pandas function to get the data for FactPredictions
        fact_data = handler.from_sql_to_pandas(chunksize=1000, id_value='customer_ID')

        # Filtering the data for month 12
        month_12_data = fact_data[fact_data['pred_period'] == 12]

        # Sorting the data by Churn_Rate in descending order
        sorted_data = month_12_data.sort_values(by='Churn_Rate', ascending=False)

        # Calculating the number of customers to select (10% of total customers)
        total_customers = len(sorted_data)
        top_percentage = int(0.1 * total_customers)

        # Selecting the top 10% of customers with the highest churn rate
        top_churn_customers = sorted_data.head(top_percentage)

        if top_churn_customers.empty:
            return {"message": "No customers found"}

        # Merging with DimCustomer table based on customer_ID and Customer_ID
        dim_handler = dim_customer_handler
        dim_data = dim_handler.from_sql_to_pandas(chunksize=1000, id_value='Customer_ID')
        
        merged_data = pd.merge(top_churn_customers, dim_data, how='left', left_on='customer_ID', right_on='Customer_ID')

        return merged_data.to_dict(orient='records')
    except Exception as e:
        logger.error(f"Failed to get top churn customers: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get top churn customers: {str(e)}")


@app.get("/get_top_clv_customers")
async def get_top_clv_customers(top_percentage: int = Query(..., description="Percentage of customers to select (e.g., 20 for top 20%)", ge=1, le=100)):
    return await get_clv_customers_internal(top_percentage, True)

@app.get("/get_bottom_clv_customers")
async def get_bottom_clv_customers(bottom_percentage: int = Query(..., description="Percentage of customers to select (e.g., 20 for bottom 20%)", ge=1, le=100)):
    return await get_clv_customers_internal(bottom_percentage, False)

async def get_clv_customers_internal(selected_percentage: int, is_top: bool):
    try:
        handler = fact_predictions_handler

        # Calling the from_sql_to_pandas function to get the data for FactPredictions
        fact_data = handler.from_sql_to_pandas(chunksize=1000, id_value='customer_ID')

        # Filtering the data for month 12
        month_12_data = fact_data[fact_data['pred_period'] == 12]

        if month_12_data.empty:
            return {"message": "No data available for pred_period = 12"}

        # Sorting the month 12 data by CLV in descending order
        sorted_data = month_12_data.sort_values(by='CLV', ascending=False)

        # Calculating the number of customers to select
        total_customers = len(sorted_data)
        selected_count = int(selected_percentage / 100 * total_customers)

        # Selecting either the top or bottom percentage of customers based on the parameter
        selected_customers = sorted_data.head(selected_count) if is_top else sorted_data.tail(selected_count)

        if selected_customers.empty:
            return {"message": "No customers found"}

        # Merging with DimCustomer table based on customer_ID and Customer_ID
        dim_handler = dim_customer_handler
        dim_data = dim_handler.from_sql_to_pandas(chunksize=1000, id_value='Customer_ID')
        
        merged_data = pd.merge(selected_customers, dim_data, how='left', left_on='customer_ID', right_on='Customer_ID')

        return {"selected_customers": merged_data.to_dict(orient='records')}
    except Exception as e:
        logger.error(f"Failed to get CLV customers: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get CLV customers: {str(e)}")


