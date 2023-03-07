import sys
import json
import pandas as pd
import pymysql 
import mysql.connector
import os

with open(os.environ["MYSQL_CRED"], 'r') as f:
    db_ms = json.load(f)

def qry_ms(query = None):
    engine_ms = mysql.connector.connect(host=db_ms['host'], user=db_ms["user"], password=db_ms["password"])
    if query == None:
        query = input("QUERY: ")
    return pd.read_sql(query, engine_ms)

#Function to save the data frame faster.
def sv(nm="df"):
    print(f"SAVING:{nm}.parquet")
    df.to_parquet(f"{nm}.parquet")

df = qry_ms()
print(df)
