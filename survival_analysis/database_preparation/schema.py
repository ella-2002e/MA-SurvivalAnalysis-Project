"""
Module: schema.py

This module contains Python code for defining and creating a database schema using SQLAlchemy. 
It defines four tables: 'DimCustomer', 'FactPredictions' 'FactPushNotification' and 'FactEmail'.

It also configures a custom logger for informational messages regarding the schema creation.

"""

import logging
import os
from ..logger import CustomFormatter

# Initialize and configure the logger
logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

from sqlalchemy import create_engine, Column, Integer, String, Float, DATE, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Define and configure the database engine (Change the connection URL as needed)
engine = create_engine('sqlite:///sa_db.db')

# Create a base class for declarative class definitions
Base = declarative_base()

class Customer(Base):
    """
    Class: Customer

    This class defines the 'DimCustomer' table, which represents customer information.

    Attributes:
    - Customer_ID (int): Primary key for the customer.
    - Age (int): Customer's age.
    - Tenure (int): Customer's tenure with the company.
    - Gender (str): Customer's gender.
    - Income (int): Customer's income.
    - Marital_Status (str): Customer's marital status.
    - Address_ID (int): Customer's address identifier.
    - Education (str): Customer's education level.
    - Retirement (str): Customer's retirement status.
    - Churn (str): Customer's churn status.
    - Region (str): Customer's region.
    - Service_Category (str): Service category.
    - Voice_Included (str): Voice service inclusion status.
    - Internet_Included (str): Internet service inclusion status.
    - Forward_Included (str): Forwarding service inclusion status.
    """
    __tablename__ = "DimCustomer"

    Customer_ID = Column(Integer, primary_key=True)
    Age = Column(Integer)
    Tenure = Column(Integer)
    Gender = Column(String(10))
    Income = Column(Integer)
    Marital_Status = Column(String(15))
    Address_ID = Column(Integer)
    Education = Column(String(45))
    Retirement = Column(String(3))
    Churn = Column(String(3))
    Region = Column(String(15))
    Service_Category = Column(String(15))
    Voice_Included = Column(String(3))
    Internet_Included = Column(String(3))
    Forward_Included = Column(String(3))

class FactPredictions(Base):
    """
    Class: FactPredictions

    This class defines the 'FactPredictions' table, which stores predictive information related to customers.

    Attributes:
    - pred_period (int): Primary key representing the prediction period.
    - customer_ID (int): Foreign key referencing the 'DimCustomer' table.
    - CLV (float): Customer Lifetime Value.
    - Churn_Rate (float): Churn rate.
    - customer (relationship): Establishes a relationship with the 'DimCustomer' table.

    """
    __tablename__ = "FactPredictions"

    pred_period = Column(Integer, primary_key=True)
    customer_ID = Column(Integer, ForeignKey('DimCustomer.Customer_ID'), primary_key=True)
    CLV = Column(Float)
    Churn_Rate = Column(Float)
    customer = relationship("DimCustomer")

class FactPushNotification(Base):
    """
    Class: FactPushNotification

    This class defines the 'FactPushNotification' table, which stores information about the push notifications sent to customers.

    Attributes:
    - sent_date (DateTime): Primary key representing the date the push notification was sent.
    - customer_ID (int): Foreign key referencing the 'DimCustomer' table.
    - success (int): A binary column representing wether the push notification was sent successfully or not.
    - customer (relationship): Establishes a relationship with the 'DimCustomer' table.

    """
    __tablename__ = "FactPushNotification"

    sent_date = Column(DateTime, primary_key=True)
    customer_ID = Column(Integer, ForeignKey('DimCustomer.Customer_ID'), primary_key=True)
    success = Column(Integer)
    customer = relationship("DimCustomer")

class FactEmail(Base):
    """
    Class: FactEmail

    This class defines the 'FactEmail' table, which stores information about the emails sent to customers.

    Attributes:
    - sent_date (DateTime): Primary key representing the date the push notification was sent.
    - customer_ID (int): Foreign key referencing the 'DimCustomer' table.
    - success (int): A binary column representing wether the push notification was sent successfully or not.
    - customer (relationship): Establishes a relationship with the 'DimCustomer' table.

    """
    __tablename__ = "FactEmail"

    sent_date = Column(DateTime, primary_key=True)
    customer_ID = Column(Integer, ForeignKey('DimCustomer.Customer_ID'), primary_key=True)
    success = Column(Integer)
    customer = relationship("DimCustomer")


# Create the tables defined in the schema
Base.metadata.create_all(engine)

# Log a message indicating that the schema has been created
logger.info("Schema Has Been Created")
