import pandas as pd
import os
import logging
from ..logger import CustomFormatter
from lifelines import WeibullFitter, ExponentialFitter, LogNormalFitter, LogLogisticFitter, LogNormalAFTFitter


# Initialize and configure the logger
logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)


class AFTModelSelector:
    """
    A class for selecting the best AFT (Accelerated Failure Time) model among Weibull, Exponential,
    Log-Normal, and Log-Logistic models based on AIC, and generating churn rate and customer lifetime value (CLV) 
    predictions for a specified number of time periods.

    Parameters:
    - data (pd.DataFrame): The input DataFrame containing survival data.
    - primary_col(str): The column name in the DataFrame representing the primary key.
    - duration_col (str): The column name in the DataFrame representing the duration or time-to-event.
    - event_col (str): The column name in the DataFrame representing the event indicator.

    Attributes:
    - data (pd.DataFrame): The input DataFrame containing survival data.
    - primary(str): The column name in the DataFrame representing the primary key.
    - duration_col (str): The column name in the DataFrame representing the duration or time-to-event.
    - event_col (str): The column name in the DataFrame representing the event indicator.
    - aft_model (lifelines.Fitter): The selected AFT model based on AIC.
    - predictions_df (pd.DataFrame): DataFrame containing churn and CLV predictions for a specified number of time periods.
    """
    
    def __init__(self, data: pd.DataFrame , primary_col:str,  duration_col : str, event_col: str):
        self.data = data
        self.primary = primary_col
        self.duration_col = duration_col
        self.event_col = event_col
        self.aft_model = None
        self.predictions_df = None

            
            
    def select_best_model(self):
        """
        Selects the best AFT model among Weibull, Exponential, Log-Normal, and Log-Logistic models based on AIC.
        Stores the selected model in the 'aft_model' attribute.
        """
        models = {
            'Weibull': WeibullFitter(),
            'Exponential': ExponentialFitter(),
            'LogNormal': LogNormalAFTFitter(),
            'LogLogistic': LogLogisticFitter(),
        }

        best_aic = float('inf')
        best_model = None

        # Handle zero values in the duration column
        self.data[self.duration_col] = self.data[self.duration_col].replace(0, 0.0001)

        for model_name, model in models.items():
            if model_name == 'LogNormal':
                model.fit(self.data, duration_col= self.duration_col, event_col= self.event_col)
            else:
                model.fit(durations = self.data[self.duration_col], event_observed =self.data[self.event_col])
                
            aic = model.AIC_
            logger.info(f"{model_name} AIC: {aic}")
    
            if aic < best_aic:
                best_aic = aic
                best_model = model_name

        logger.warning(f"\nBest Model: {best_model} with AIC: {best_aic}")
        self.aft_model = models[best_model]


    def fit_and_predict(self, n_time_periods: int):
        """
        Fits the selected AFT model and generates churn predictions for a specified number of time periods.
        Stores the predictions in the 'predictions_df' attribute.

        Parameters:
        - n_time_periods (int): The number of time periods for which predictions should be generated.
            
        Returns:
        - str: A message indicating the model ran successfully. 
        """
        if self.aft_model is None:
            logger.warning("Please run select_best_model() first.")
            return

        # Handle zero values in the duration column
        self.data[self.duration_col] = self.data[self.duration_col].replace(0, 0.0001)

        predictions_df_list = []

        for time_period in range(1, n_time_periods + 1):
            customer_data = pd.DataFrame({
                'customer_id': self.data[self.primary],
                'pred_period': time_period
            })

            # Generate survival predictions 
            predictions = self.aft_model.predict_survival_function(self.data, times=[time_period])

            #obtaining churn predictions
            churn = round(1 - predictions, 5)
            # Convert predictions to a DataFrame
            predictions_df = pd.DataFrame(churn.T.values, columns=['churn_rate'])

            # Concatenate customer_id and time_period with predictions DataFrame
            result_df = pd.concat([customer_data, predictions_df], axis=1)

            # Append to the list
            predictions_df_list.append(result_df)

        # Concatenate all predictions into a single DataFrame
        self.predictions_df = pd.concat(predictions_df_list, ignore_index=True)
        logger.info("The AFT model was run successfully.")

    def calculate_clv(self, MM=1300, r=0.1):
        """
        Calculates Customer Lifetime Value (CLV) for each customer in 'predictions_df' attribute 
        and updates the dataframe to include CLV predictions.

        Parameters:
        - MM (float): A constant representing the monetary value.
        - r (float): The periodic interest rate for discounting.
                
        Returns:
        - str: A message indicating the 'predictions_df' attribute was updated successfully. 
        """
        
        predictions_dfs = []  # List to store individual CLV prediction DataFrames
        if self.predictions_df is None:
            logger.warning("Please run fit_and_predict() first.")
            return
        
        #Making the data long format
        data_clv = self.predictions_df.pivot(index='customer_id', columns='pred_period', values='churn_rate')
        #Calculating the Survival Rates from Churn Rates 
        data_clv = 1 - data_clv

        # Iterating over an increasing number of columns
        for i in range(1, len(data_clv.columns) + 1):
            # Selecting the first i columns
            subset_data = data_clv.iloc[:, :i]
    
            # Calculating CLV 
            data_clv1 = subset_data.copy()
            sequence = list(range(1, len(data_clv1.columns) + 1))

            for num in sequence:
                data_clv1.iloc[:, num - 1] /= (1 + r/12) ** (num - 1)

            data_clv1['CLV'] = MM * data_clv1.sum(axis=1)
            
            predictions_dfs.append(data_clv1['CLV'])

        clv_prediction = pd.concat(predictions_dfs, axis=1)
        clv_prediction.columns = range(1, len(predictions_dfs) + 1)

        #returning to original data format and saving the predictions
        clv_prediction = clv_prediction.reset_index()
        clv_prediction = pd.melt(clv_prediction, id_vars=['customer_id'], var_name='pred_period', value_name='CLV')

        #Combining the results and updating the predictions dataframe
        self.predictions_df = pd.merge(self.predictions_df, clv_prediction, on=['customer_id','pred_period'], how='left')
        logger.info("The CLV predictions were added successfully.")
        


    # def calculate_clv(self, MM=1300, r=0.1):
    #     """
    #     Calculate Customer Lifetime Value (CLV) for each customer in the predictions DataFrame.

    #     Parameters:
    #         - MM (float): A constant representing the monetary value.
    #         - r (float): The periodic interest rate for discounting.

    #     Returns:
    #         - pd.Series: Series containing CLV values for each customer.
    #     """
    #     if self.predictions_df is None:
    #         logger.warning("Please run fit_and_predict() first.")
    #         return
        
    #     #Preparing data for calculating CLV
    #     data_clv = self.predictions_df.pivot(index='customer_id', columns='pred_period', values='churn_rate')
    #     #Calculating again the Survival rates from Churn rates df
    #     data_clv = 1 - data_clv

    #     #Calculating clv
    #     sequence = list(range(1, len(data_clv.columns) + 1))

    #     # Iterating over each column in data_clv
    #     for num in sequence:
    #         # Discount the values in the column based on time-value-of-money calculation
    #         data_clv.iloc[:, num - 1] /= (1 + r/12) ** (num - 1)

    #     # Calculate CLV for each row
    #     data_clv['CLV'] = MM * data_clv.sum(axis=1)
    #     self.clv_prediction = data_clv



