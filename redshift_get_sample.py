# Import required modules
import warnings
import pandas as pd
import json
import redshift_connector
import os

# Suppress warnings
warnings.filterwarnings("ignore")

# Load Redshift credentials from environment variable
with open(os.environ["REDSHIFT_CRED"], 'r') as file:
    db_mysql  = json.load(file)

# Connect to Redshift engine
engine_rs = redshift_connector.connect(
    host=db_mysql['host'],
    database=db_mysql['database'],
    user=db_mysql['user'],
    password=db_mysql['password']
)

# Function to select a database to query
def select_database():
    # Prompt user to select a database
    print("Choose a database:")
    print("1. ", os.environ.get("RS_DB1", "Database 1"))
    print("2. ", os.environ.get("RS_DB2", "Database 2"))
    choice = input("Enter 1 or 2: ")
    
    # Select database based on user input
    if choice == "1":
        selected_db = os.environ.get("RS_DB1", "Database 1")
    elif choice == "2":
        selected_db = os.environ.get("RS_DB2", "Database 2")
    else:
        print("Invalid choice. Please enter 1 or 2.")
        select_database()
    return selected_db

# Function to generate a sample query
def qry_sample(query=""):
    prefix = os.environ.get("RS_PREFIX", "")
    suffix = " limit 300"
    db_name = select_database()
    tbl_name = input("TABLE: ")
    try:
        query = f"SELECT * FROM {prefix}{db_name}_{tbl_name} {suffix}"
        print(query)
        return query
    except:
        return "ERRO"

# Function to execute a query on Redshift
def qry_rs(query=""):
    if query == "":
        query = f"{input('QUERY: ')}"
        return pd.read_sql(query, engine_rs)
    else:
        return pd.read_sql(query, engine_rs)

# Generate a sample query
myQuery = qry_sample()

# Execute the query on Redshift
df = qry_rs(myQuery)

# Print the results
print(df)

