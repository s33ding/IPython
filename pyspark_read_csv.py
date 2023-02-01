import pyspark
import sys
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, StringType, IntegerType 
from pyspark.sql.types import ArrayType, DoubleType, BooleanType
from pyspark.sql.functions import col,array_contains

spark = SparkSession.builder.appName('s33ding').getOrCreate()

def qry():
    engine = mysql.connector.connect(host=db['host'], user=db["user"], password=db["password"])
    query = input("query: ")
    pandasDF =  pd.read_sql(query, engine)
    df = spark.createDataFrame(pandasDF)
    return df

def pscsv(fl_nm=""):
    if fl_nm=="":
        fl_nm = input("CSV: ")
        return spark.read.csv(fl_nm, header=True)
    else:
        return spark.read.csv(fl_nm, header=True)

csv_fl = sys.argv[1]

df = pscsv(fl_nm)
df.show(1)
