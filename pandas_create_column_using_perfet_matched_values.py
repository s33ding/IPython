# This script imports the pandas library and system library
import pandas as pd
import sys

def match_and_create_column(
    df_main = pd.read_parquet(sys.argv[1]), # Read in the first parquet file from command line argument
    df2 = pd.read_parquet(sys.argv[2]), # Read in the second parquet file from command line argument
    col_ref_df_main = sys.argv[3], # Read in the column reference for the first dataframe from command line argument
    col_ref_df2 =  sys.argv[4], # Read in the column reference for the second dataframe from command line argument
    lst_cols = sys.argv[5:] if len(sys.argv) > 4 else [] # Read in the desired columns to be added to the first dataframe from command line argument
):
    """
    Function to match and create new columns in the first dataframe

    df_main : pandas DataFrame
        The first dataframe to be updated
    df2 : pandas DataFrame
        The second dataframe to be used for matching and updating the first dataframe
    col_ref_df_main : str
        The column reference from the first dataframe
    col_ref_df2 : str
        The column reference from the second dataframe
    lst_cols : List
        The list of desired columns to be added to the first dataframe

    Returns
    -------
    df_main : pandas DataFrame
        The first dataframe with the new columns added
    """
    # Print the input variables to check if they are as expected
    print(f"df_main: {df_main}")
    print(f"df2: {df2}")
    print(f"col_ref_df_main: {col_ref_df_main}")
    print(f"col_ref_df2: {col_ref_df2}")
    print(f"lst_cols: {lst_cols}")

    # Loop through the list of desired columns
    for new_col in lst_cols:
        # Create a new column in the first dataframe
        df_main[new_col] = None
        # Loop through the values in the column reference of the first dataframe
        for i, v in enumerate(df_main[col_ref_df_main]):
            # Find the value in the column of interest in the second dataframe
            val = df2.loc[ df2[col_ref_df2] == v, new_col ].iloc[0]
            # Add the value to the new column in the first dataframe
            df_main[ new_col ].iloc[i] = val
    # Return the updated first dataframe
    return df_main

# Call the function to match and create new columns
df = match_and_create_column()
# Write the updated first dataframe to a parquet file
df.to_parquet(sys.argv[1])
