import sys
import json
import pandas as pd
import pymysql 
import mysql.connector
import sqlalchemy as sqla

fileNm =  '/run/media/roberto/black-box/.syek/connections/roberto-prod.json'

with open(fileNm, 'r') as f:
    db = json.load(f)

engine = mysql.connector.connect(host=db['host'], user=db["user"], password=db["password"])

qry = input("query: ")
df = pd.read_sql(qry, engine)

#Function to save the data frame faster.
def sv(nm="df"):
    df.to_csv(f"{nm}.csv")

print(df)
