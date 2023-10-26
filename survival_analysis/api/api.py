from fastapi import FastAPI
import sqlite3
import logging
from ..logger import CustomFormatter
import os

app = FastAPI()


    # Just en example
import os 
    
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

# Define a function to open a connection to the SQLite database
def get_db():
    db = sqlite3.connect('sa_db.db')
    return db

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/get_data/{customer_id}")
async def get_record(customer_id: int):
    # Open a connection to the database
    with get_db() as db:
        cursor = db.cursor()
        # Execute a SQL query to fetch the data
        cursor.execute(f"SELECT * FROM DimCustomer WHERE Customer_ID = {customer_id}")
        record = cursor.fetchone()

    if record is None:
        return {"error": "Record not found"}

    # Convert the record to a dictionary (assuming you have column names)
    column_names = [description[0] for description in cursor.description]
    record_dict = dict(zip(column_names, record))
    return record_dict

