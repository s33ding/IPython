import warnings
import pandas as pd
import boto3
import json
import redshift_connector
import os

warnings.filterwarnings("ignore")

with open(os.environ["REDSHIFT_CRED"], 'r') as file:
    db  = json.load(file)

conn = redshift_connector.connect(
    host = db['host'],
    database = db['database'],
    user= db['user'],
    password= db['password']
)

def qry(query=""):
    if query == "":
        query = f"""{input("QUERY: ")}"""
        return pd.read_sql(query, conn)
    else:
        return pd.read_sql(query, conn)

df = qry()
print(df)
