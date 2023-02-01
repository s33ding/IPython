import sys
import pandas as pd

def pdcsv(fl_nm):
    if fl_nm=="":
        fl_nm = input("CSV: ")
        return pd.read_csv(fl_nm)
    else:
        return pd.read_csv(fl_nm)

#Function to save the data frame faster.
def sv(nm="df"):
    print(f"SAVING:{nm}.parquet")
    df.to_parquet(f"{nm}.parquet")

fl_nm = sys.argv[1] 
df = pdcsv(fl_nm)
print(df)
