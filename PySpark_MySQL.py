import pyspark
import pandas as pd
import pymysql
import json
import mysql.connector
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, StringType, IntegerType 
from pyspark.sql.types import ArrayType, DoubleType, BooleanType
from pyspark.sql.functions import col,array_contains
from  os import system

spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()

fileNm =  '/run/media/roberto/black-box/.syek/connections/roberto-prod.json'
with open(fileNm, 'r') as f:
    db = json.load(f)

def sql_to_parquet(custom=False):
    engine = mysql.connector.connect(host=db['host'], user=db["user"], password=db["password"])
    query = input("QUERY: ")
    tmp = pd.read_sql(query, engine)

    if custom==True:
        nm_fl = input("NAME OF THE FILE: ")
        tmp.to_parquet(nm_file)
    else:
        nm_fl = "temp.parquet"
        tmp.to_parquet(nm_file)
    return nm_fl

def spark_read_parquet(nm_file):
    return spark.read.parquet(nm_file)

def qry(custom = False):
    sql_to_parquet(custom)
    df = spark_read_parquet(nm_file)
    return df

def clean(nm_fl="temp.parquet"):
    system(f"rm -r {nm_fl}")

df = qry(custom=True)
