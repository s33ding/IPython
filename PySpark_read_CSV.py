import pyspark
import sys
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, StringType, IntegerType 
from pyspark.sql.types import ArrayType, DoubleType, BooleanType
from pyspark.sql.functions import col,array_contains

spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()

def qry():
    engine = mysql.connector.connect(host=db['host'], user=db["user"], password=db["password"])
    query = input("query: ")
    pandasDF =  pd.read_sql(query, engine)
    df = spark.createDataFrame(pandasDF)
    return df

def psr():
    csv_nm = input("CSV: ")
    return spark.read.csv(csv_nm, header=True)

csv_fl = sys.argv[1]

df = spark.read.csv(csv_fl, header=True)
df.show(1)
