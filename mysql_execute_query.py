import sys
import json
import pandas as pd
import pymysql 
import mysql.connector
import os

with open(os.environ["MYSQL_CRED"], 'r') as f:
    db_ms = json.load(f)

engine_ms = mysql.connector.connect(
        host=db_ms['host'], 
        user=db_ms["user"], 
        password=db_ms["password"])

fl = sys.argv[1] 
with open(fl, "r") as f:
    qry = f.read()

df = pd.read_sql(qry, engine_ms)
print(df)
