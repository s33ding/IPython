import warnings
import pandas as pd
import json
import redshift_connector
import os

warnings.filterwarnings("ignore")

with open(os.environ["REDSHIFT_CRED"], 'r') as file:
    db_mysql  = json.load(file)

engine_rs = redshift_connector.connect(
    host = db_mysql['host'],
    database = db_mysql['database'],
    user= db_mysql['user'],
    password= db_mysql['password']
)

def qry_rs(query=""):
    if query == "":
        query = f"""{input("QUERY: ")}"""
        return pd.read_sql(query, engine_rs)
    else:
        return pd.read_sql(query, engine_rs)

df = qry_rs()
print(df)
