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

def sql_to_parquet():
    engine = mysql.connector.connect(host=db['host'], user=db["user"], password=db["password"])
    query = input("QUERY: ")
    tmp = pd.read_sql(query, engine)
    tmp.to_parquet('temp.parquet')


def spark_read_parquet():
    return spark.read.parquet("temp.parquet")

def qry():
    sql_to_parquet()
    df = spark_read_parquet()
    return df

df = qry()
