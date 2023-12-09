# Survival Analysis Package

## Overview

The **Survival Analysis** package is a Python toolkit for analyzing and predicting customer churn and lifetime value using survival analysis techniques. This package encompasses several modules that cover database schema creation, SQL interactions, predictive modeling, and utility functions for data preprocessing.

## Installation 

```python
pip install survival_analysis
```
## Modules

### 1. `schema.py`

#### Module Description:

This module, `schema.py`, contains Python code for defining and creating a database schema using SQLAlchemy. It defines tables such as 'DimCustomer', 'FactPredictions', 'FactPushNotification', and 'FactEmail' for storing customer information, predictive data, push notification details, and email information, respectively.

```python
from survival_analysis import schema
```

