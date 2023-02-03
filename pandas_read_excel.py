import sys
import pandas as pd

def pdex(fl_nm):
    if fl_nm=="":
        fl_nm = input("EXCEL: ")
        return pd.read_excel(fl_nm)
    else:
        return pd.read_excel(fl_nm)

#Function to save the data frame faster.
def sv(nm="df"):
    print(f"SAVING:{nm}.parquet")
    df.to_parquet(f"{nm}.parquet")

fl_nm = sys.argv[1] 
df = pdex(fl_nm)
print(df)
