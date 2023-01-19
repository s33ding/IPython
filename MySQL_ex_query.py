import sys
import json
import pandas as pd
import pymysql 
import mysql.connector
import os

with open(os.environ["MYSQL_CRED"], 'r') as f:
    db_mysql = json.load(f)

engine_mysql = mysql.connector.connect(
        host=db_mysql['host'], 
        user=db_mysql["user"], 
        password=db_mysql["password"])

fl = sys.argv[1] 
with open(fl, "r") as f:
    qry = f.read()

df = pd.read_sql(qry, engine_mysql)
print(df)
