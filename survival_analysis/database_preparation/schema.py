
import logging
import os

import logging
from ..logger import CustomFormatter

logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)


from sqlalchemy import create_engine,Column,Integer,String,Float, DATE, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

#engine=create_engine('mysql+mysqlconnector://root:anechka2002@127.0.0.1:3306/sa_db')

#connection = engine.connect()

engine=create_engine('sqlite:///sa_db.db')

Base= declarative_base()

class Customer(Base):
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

'''
class Region(Base):
    __tablename__ = "DimRegion"

    Region_ID = Column(Integer, primary_key=True)
    Region = Column(String(15))


class Category(Base):
    __tablename__ = "DimServiceCategory"

    Service_Category_ID = Column(Integer, primary_key=True)
    Service_Category = Column(String(15))
'''

class FactPredictions(Base):
    __tablename__ = "FactPredictions"

    pred_period = Column(Integer, primary_key=True)
    customer_ID = Column(Integer, ForeignKey('DimCustomer.Customer_ID'), primary_key=True)
    CLV = Column(Float)
    Churn_Rate = Column(Float)
    customer = relationship("DimCustomer")


Base.metadata.create_all(engine)

logger.info("Schema Has Been Created")