import sys
from time import sleep
import json
import pandas as pd

def rjson(filename=""):
    if filename == "" and len(sys.argv) != 1:
        filename = sys.argv[1]
    if filename=="" and len(sys.argv) == 1:
        filename = input("JSON: ")
    with open(filename, 'r') as f:
        return json.load(f)


data = rjson()
print("\nThe JSON is loaded as a dictionary called 'data'.")
sleep(2)
