# Survival Analysis Package

## Overview

The **Survival Analysis** package is a Python toolkit for analyzing and predicting customer churn and lifetime value using survival analysis techniques. This package encompasses several modules that cover database schema creation, SQL interactions, predictive modeling, and utility functions for data preprocessing.

## Installation 

```python
pip install survival-analysis
```
You can access our package via PyPi using this link:
https://pypi.org/project/survival-analysis/0.0.1/

## Documentation

Detailed information about our package can be found at 
https://anna-shaljyan.github.io/mkdocs-survival-analysis/?fbclid=IwAR2Kxzv_bs3WhMpGeU9jP0lKwvQ-sGPK_EG4ualMhqPFglEX9Nhoo8bE8N0

## Modules

### 1. `schema.py`

#### Module Description:

This module, `schema.py`, contains Python code for defining and creating a database schema using SQLAlchemy. It defines tables such as 'DimCustomer', 'FactPredictions', 'FactPushNotification', and 'FactEmail' for storing customer information, predictive data, push notification details, and email information, respectively.

```python
from survival_analysis import schema
```

The obtained databse has the below structure:
![Database ERD](survival_analysis/docs/ERD.jpg)

### 2. sql_interactions.py

#### Module Description:

The sql_interactions module provides a Python class named SqlHandler for interacting with SQLite databases. This class allows various operations such as connecting, inserting data, retrieving data, truncating tables, dropping tables, updating tables, and more.

```python
from survival_analysis import sql_interactions
```

### 3. model_AFT.py

#### Module Description:

The model_AFT module implements an Accelerated Failure Time (AFT) model for predicting customer churn and lifetime value. It includes classes for different AFT models, a model selector for choosing the best model based on AIC, and methods for fitting the model and generating predictions.

```python
from survival_analysis import model_AFT
```

### 4. utils.py

#### Module Description:

The utils module contains utility functions, including format_dataframe, which converts categorical variables to binary columns using one-hot encoding and ensures correct data types for numeric variables.

```python
from survival_analysis import utils
```
## Example Usage

An example demonstrating the use of this package can be found at https://github.com/ella-2002e/MA-SurvivalAnalysis-Project/blob/main/Example.ipynb

# API

The API extends our Survival Analysis project with functionality to select data from the database and insert data. The API now includes several endpoints that help identify top customers with the highest churn rate, customers with the highest/lowest CLV, etc.

## Usage 

Run `run.py` to see initially a message in port, add /docs to see put methods and two get endpoints besides message.
Port should look something like this: http://127.0.0.1:8000/docs#/ . You can run `run.py` by executing python run.py in your terminal in venv. 

## ENDPOINTS

### GET

#### 1. get_top_churn_clv_customers 
- Accepts pred_period and number of percentage for sorting customers initially by churn_rate and then by clv. It returns top x% customers based on churn_rate & CLV.

#### 2. get_top_clv_customers
- Accepts pred_period and number of percentage for sorting customers by CLV. It returns top x% customers based on CLV.

### PUT

These below PUT methods are created to populate the DB with the results of actions taken in response to the two GET methods mentioned above.
There are two csv files email_data.csv and notifications_data.csv in Raw Data folder that contain sample generated data with structure that matches tables of the database.

#### 1. populate_fact_push_notification

 - Allows to choose a csv file to add in FactPushNotification table. Use that method with notifications_data.csv to populate the FactPushNotification table in the DB. Note that, customer_id-s are taken from endpoint: http://127.0.0.1:8000/get_top_churn_clv_customers?pred_period=12&top_percentage=10 

#### 2. populate_fact_email

- Similarly, use email_data.csv to populate FactEmail table with second put method. Note that, email_data customer_id-s are taken from endpoint: http://127.0.0.1:8000/get_top_clv_customers?top_percentage=20&pred_period=5


## License
This package is provided under the MIT License. Feel free to use and modify it in your projects.