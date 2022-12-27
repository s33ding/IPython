import warnings
import pandas as pd
import boto3
import json
import redshift_connector

warnings.filterwarnings("ignore")

with open('/run/media/roberto/black-box/.syek/connections/RedShift.json', 'r') as file:
    db  = json.load(file)

conn = redshift_connector.connect(
    host = db['host'],
    database = db['database'],
    user= db['user'],
    password= db['password']
)

qry = input("QUERY: ")

df = pd.read_sql(qry, conn)
print(df)
