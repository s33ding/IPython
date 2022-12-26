import pyspark
import sys
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, StringType, IntegerType 
from pyspark.sql.types import ArrayType, DoubleType, BooleanType
from pyspark.sql.functions import col,array_contains

spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()

def psr():
    csv_nm = input("CSV: ")
    return spark.read.csv(csv_nm, header=True)

csv_fl = sys.argv[1]

df = spark.read.csv(csv_fl, header=True)
df.show(1)
