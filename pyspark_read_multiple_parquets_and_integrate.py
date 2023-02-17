import sys
import os
from pyspark.sql import SparkSession

# Start a Spark session
spark = SparkSession.builder.appName("Parquet Integration").getOrCreate()

def read_multiple_parquets_and_integrate(directory_path='.'):
    # Get the directory path from sys.argv if provided
    if len(sys.argv) > 1:
        directory_path = sys.argv[1]
        if "/" != directory_path[-1]:
            directory_path = directory_path + "/"
        print(f"directory_path:{directory_path}")
        # Get a list of all the parquet files in the directory
        parquet_files = [f"{directory_path}{f}" for f in os.listdir(directory_path) if f.endswith('.parquet')]
    # Get the directory path from sys.argv if provided
    else:
        if "/" != directory_path[-1]:
            directory_path = directory_path + "/"
        print(f"directory_path:{directory_path}")
        # Get a list of all the parquet files in the directory
        parquet_files = [f"{directory_path}{f}" for f in os.listdir(directory_path) if f.endswith('.parquet')]
    # Read all the parquet files in the directory into a single PySpark DataFrame
    df = spark.read.parquet(*parquet_files)
    return df

df = read_multiple_parquets_and_integrate()
df.show(5)
