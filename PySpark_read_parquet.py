import pyspark
import sys
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, StringType, IntegerType 
from pyspark.sql.types import ArrayType, DoubleType, BooleanType
from pyspark.sql.functions import col,array_contains

spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()

def psprq(parquet_nm=""):
    if parquet_nm == "":
        parquet_nm = input("PARQUET: ")
        return spark.read.parquet(parquet_nm)
    else:
        return spark.read.parquet(parquet_nm)


parquet_nm = sys.argv[1]
print(parquet_nm)
df = psprq(parquet_nm)
df.show(1)
