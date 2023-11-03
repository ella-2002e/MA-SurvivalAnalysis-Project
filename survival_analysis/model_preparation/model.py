import pandas as pd
import random

### THIS IS A PLACEHOLDER MODEL TO TEST INTERACTION WITH DB AND API.

class PseudoModel:
    def __init__(self, dataframe: pd.DataFrame):
        """
        Initialize the PseudoModel with a DataFrame.
        
        Parameters:
            dataframe (pandas.DataFrame): Input DataFrame. 
        """
        self.dataframe = dataframe

    def generate_data(self,  column: str, num_periods=12):
        """
        Generate random customer data for a given number of periods.

        Parameters:
            num_periods (int): Number of periods to generate data for (default is 12).

        Returns:
            pandas.DataFrame: DataFrame containing customer_id, period, CLV, and churn_rate.
        """
        results = []
        for _, row in self.dataframe.iterrows():
            customer_id = row[column]
            for pred_period in range(1, num_periods + 1):
                clv = random.uniform(0, 10000)  # Adjust the range as needed
                churn_rate = random.uniform(0, 1)  # Adjust the range as needed
                results.append([customer_id, pred_period, clv, churn_rate])

        result_df = pd.DataFrame(results, columns=['customer_id', 'pred_period', 'CLV', 'churn_rate'])
        return result_df

    def pseudo_model(self, column: str, num_periods=12):
        """
        Generate pseudo customer data for the specified number of periods.

        Parameters:
            num_periods (int): Number of periods to generate data for (default is 12).

        Returns:
            pandas.DataFrame: DataFrame containing customer_id, period, CLV, and churn_rate.
        """
        generated_data = self.generate_data(column, num_periods)
        return generated_data

