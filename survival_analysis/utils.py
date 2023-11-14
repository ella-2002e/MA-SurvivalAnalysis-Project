import pandas as pd

""""
THIS IS A MODULE FOR UTILITY FUNCTIONS
"""

def format_dataframe(df):
    """
    Converts categorical variables in a DataFrame to binary columns using one-hot encoding and makes sure that numeric variables are of correct type.

    Parameters:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The DataFrame with categorical variables converted to binary columns.
    """
    # Identify string variables
    string_variables = df.select_dtypes(include=['object']).columns

    #Exclude columns where all values can be converted to numeric
    numeric_variables = df.apply(pd.to_numeric, errors='coerce').notna().all()
    string_variables = string_variables.difference(numeric_variables[numeric_variables].index)
    df.reset_index(drop=True, inplace=True)
    
    # Filter DataFrame to keep only string variables
    string_df = df[string_variables]

    # Dummify the string variables
    dummies_df = pd.get_dummies(string_df, columns=string_variables, prefix=string_variables,  drop_first=True)
    dummies_df = dummies_df.astype(int)

    # Concatenate the dummified variables with the original DataFrame
    output_df = pd.concat([df, dummies_df], axis=1)

    # Convert true numeric values to appropriate numeric type
    for column in numeric_variables[numeric_variables].index:
        output_df[column] = pd.to_numeric(df[column], errors='coerce')

    # Drop the original string variables
    output_df = output_df.drop(columns=string_variables)

    return output_df

