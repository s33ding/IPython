import redshift_connector
import sys
import pyspark
import pandas as pd
import json
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, StringType, IntegerType 
from pyspark.sql.types import ArrayType, DoubleType, BooleanType
from pyspark.sql.functions import col,array_contains
import os

spark = SparkSession.builder.appName('s33ding').getOrCreate()

fileNm =  os.environ["REDSHIFT_CRED"]
with open(fileNm, 'r') as f:
    db = json.load(f)

def sql_to_parquet(query):
    engine = redshift_connector.connect(
    host = db['host'],
    database = db['database'],
    user= db['user'],
    password= db['password'])

    if query == "":
        query = input("QUERY: ")
        tmp = pd.read_sql(query, engine)
    else: 
        tmp = pd.read_sql(query, engine)

    nm_fl = input("NAME OF THE FILE(YOU CAN LEAVE IT EMPTY): ")
    if nm_fl != "":
        tmp.to_parquet(nm_fl)
    else:
        nm_fl = "temp.parquet"
        tmp.to_parquet(nm_fl)
    return nm_fl

def spark_read_parquet(nm_fl):
    return spark.read.parquet(nm_fl)

def qry(query=""):
    nm_fl = sql_to_parquet(query)
    df = spark_read_parquet(nm_fl)
    return df

def clean(nm_fl="temp.parquet"):
    os.system(f"rm -r {nm_fl}")

df = qry()
print(df)
