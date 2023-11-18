# MA-SurvivalAnalysis-Project

Unlock survival analysis, churn prediction, and CLV estimation with our Python package. Tailor your insights and make data-driven decisions.

## Getting Started

Follow these simple steps to get started with our package:

### Step 1: Database Preparation

1. Run `schema_builder.py` to create the necessary database. An Entity Relationship Diagram (ERD) of the database can be found in the `survival_analysis/database_preparation/ERD.jpg` file.

![Database ERD](survival_analysis/docs/ERD.jpg)

### Step 2: Adding Data

2. Run `sql_interaction.py` to populate the 'DimCustomers' table in the database with your data. Ensure that the column names in your CSV file match the column names in the database.

### Step 3: Running Model and Adding Data To DB

3. Run `model_runner.py` to predict Churn Rate and Customer Lifetime Value (CLV) using Accelerated failure time (AFT) model for the customers and populate the 'FactPredictions' table in the database with the results. Ensure that the column names in your CSV file match the column names in the database.

### Step 4: Testing with Swagger, it contains put methods and endpoints (API part)

Run `run.py` to see initially a message in port, add /docs to see put methods and two get endpoints besides message.
Port should look something like this: http://127.0.0.1:8000/docs#/ . You can run `run.py` by executing python run.py in your terminal in venv. 

## The API contains:

### 1. Two get methods: get_top_churn_clv_customers & get_top_clv_customers 
- First endpoint /get_top_churn_clv_customers accepts pred_period and number of percentage for sorting customers initially by churn_rate and then by clv. It returns top x% customers based on churn_rate & CLV.
- Second endpoint /get_top_clv_customers accepts pred_period and number of percentage for sorting customers by CLV. It returns top x% customers based on CLV.

### 2. Two put methods: populate_fact_push_notification & populate_fact_email

These two methods are created to populate the DB with the results of actions taken in response to the two get methods mentioned above.
There are two csv files email_data.csv and notifications_data.csv in Raw Data folder that contain sample generated data with structure that matches tables of the database.

- First put method allows to choose a csv file to add in FactPushNotification table. Use that method with notifications_data.csv to populate the FactPushNotification table in the DB. Note that, customer_id-s are taken from endpoint: http://127.0.0.1:8000/get_top_churn_clv_customers?pred_period=12&top_percentage=10 

- Similarly, use email_data.csv to populate FactEmail table with second put method. Note that, email_data customer_id-s are taken from endpoint: http://127.0.0.1:8000/get_top_clv_customers?top_percentage=20&pred_period=5