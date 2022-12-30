import sys
import json
import pandas as pd
import pymysql 
import mysql.connector
import os

fileNm = os.environ["MYSQL_CRED"]
with open(fileNm, 'r') as f:
    db = json.load(f)

engine = mysql.connector.connect(host=db['host'], user=db["user"], password=db["password"])

fl = sys.argv[1] 
with open(fl, "r") as f:
    qry = f.read()

df = pd.read_sql(qry, engine)
print(df)
