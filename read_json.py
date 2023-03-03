import sys
from time import sleep
import json
import pandas as pd

#Function to save the data frame faster.
def sv(nm="df"):
    print(f"SAVING:{nm}.parquet")
    df.to_parquet(f"{nm}.parquet")

def rjson(filename=""):
    if filename=="":
        filename = input("JSON: ")
    with open(filename, 'r') as f:
        return json.load(f)

filename = sys.argv[1]

data = rjson(filename)
print("\nThe JSON is loaded as a dictionary called 'data'.")
sleep(2)
