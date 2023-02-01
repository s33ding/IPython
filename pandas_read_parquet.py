import sys
import pandas as pd

def pdprq(fl_nm=""):

    try:
        fl_nm = sys.argv[1] 
    except:
        pass

    if fl_nm=="":
        fl_nm = input("PARQUET: ")
        return pd.read_parquet(fl_nm)
    else:
        return pd.read_parquet(fl_nm)

df = pdprq()
print(df)
