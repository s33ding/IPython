import sys
import json
import pandas as pd
import pymysql 
import mysql.connector
import os

fileNm =  os.environ["MySQL_CRED"]
with open(fileNm, 'r') as f:
    db = json.load(f)

def qry():
    engine = mysql.connector.connect(host=db['host'], user=db["user"], password=db["password"])
    query = input("query: ")
    return pd.read_sql(query, engine)

#Function to save the data frame faster.
def sv(nm="df"):
    df.to_csv(f"{nm}.csv")

df = qry()
print(df)
