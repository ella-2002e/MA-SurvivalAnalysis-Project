from fastapi import FastAPI, HTTPException
import sqlite3
import logging
from ..logger import CustomFormatter
import os
from pydantic import BaseModel
from typing import Any

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

# Defining a function to open a connection to our SQLite database
def get_db():
    db = sqlite3.connect('sa_db.db')
    return db

@app.get("/")
async def root():
    return {"message": "Initializing API for Survival Analysis project with selecting data from database, inserting data and updating data "}

@app.get("/get_data/{customer_id}")
async def get_record(customer_id: int):
    # Open a connection to the database
    with get_db() as db:
        cursor = db.cursor()
        # Executing a SQL query to fetch the data
        cursor.execute(f"SELECT * FROM DimCustomer WHERE Customer_ID = {customer_id}")
        record = cursor.fetchone()

    if record is None:
        return {"error": "Record not found"}

    # Converting the record to a dictionary 
    column_names = [description[0] for description in cursor.description]
    record_dict = dict(zip(column_names, record))
    return record_dict


# Defining a Pydantic model for the data
class CreateCustomerRequest(BaseModel):
    Customer_ID: int
    region: str
    tenure: int
    Age: int
    Marital_Status: str
    Address_ID: int
    income: int
    Education: str
    Retirement: str
    gender: str
    Voice_Included: str
    Internet_Included: str
    Forward_Included: str
    service_category: str
    churn: str

# Defining a function to open a connection to the SQLite database
def get_db():
    db = sqlite3.connect('sa_db.db')
    return db

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/create_data")
async def create_record(new_data: CreateCustomerRequest):
    try:
        # Opening a database connection using the get_db function
        db = get_db()
        cursor = db.cursor()

        # Defining the SQL query to insert data into the table
        insert_query = """
        INSERT INTO DimCustomer (
            Customer_ID, region, tenure, Age, Marital_Status, Address_ID, income,
            Education, Retirement, gender, Voice_Included, Internet_Included,
            Forward_Included, service_category, churn
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        # Executing the insert query with the data from the new_data parameter
        cursor.execute(insert_query, (
            new_data.Customer_ID, new_data.region, new_data.tenure,
            new_data.Age, new_data.Marital_Status, new_data.Address_ID,
            new_data.income, new_data.Education, new_data.Retirement,
            new_data.gender, new_data.Voice_Included, new_data.Internet_Included,
            new_data.Forward_Included, new_data.service_category, new_data.churn
        ))

        # Committing the transaction to save the data in the database
        db.commit()

        return {"message": "Record created successfully"}
    except Exception as e:
        logger.error(f"Failed to insert data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to insert data: {str(e)}")
    finally:
        # Closing the database connection in the 'finally' block
        db.close()


# Pydantic model to specify the update request
class UpdateRecordRequest(BaseModel):
    column_name: str  # The type that column gets
    new_value: Any # As it can be both integer and str, defined as Any. Later can find better solution
    customer_id: int  # The type that the customer_id is

@app.put("/update_data")
async def update_record(update_request: UpdateRecordRequest):
    try:
        # Opening a database connection using the get_db function
        db = get_db()
        cursor = db.cursor()

        # Defining the SQL query to update the specified column for the given record ID
        update_query = f"UPDATE DimCustomer SET {update_request.column_name} = ? WHERE Customer_ID = ?"

        # Executing the update query with the new value and record ID
        cursor.execute(update_query, (update_request.new_value, update_request.customer_id))

        # Committing the transaction to save the data in the database
        db.commit()

        return {"message": "Record updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update data: {str(e)}")
    finally:
        # Closing the database connection in the 'finally' block
        db.close()

