import sys
import pandas as pd


def pdprq(fl_nm=""):
    if fl_nm=="":
        fl_nm = input("PARQUET: ")
        return pd.read_parquet(fl_nm)
    else:
        return pd.read_parquet(fl_nm)

def create_samples(df_source,n_samples=1, sample_size=200):
    for x in range(1, n_samples+1):
        tmp = df_source.sample(n=sample_size)
        tmp.to_parquet(f"sample_{x}.parquet",index =False)
        
for i,v in enumerate(["FILE","NUMBER_OF_SAMPLES","SAMPLE_SIZE"]):
    try:
        print(f"{v} = {sys.argv[i+1]}")
    except:
        pass

FILE = sys.argv[1]
NUMBER_OF_SAMPLES = int(sys.argv[2])
SAMPLE_SIZE = int(sys.argv[3])

df = pdprq(fl_nm=FILE)
create_samples(df_source=df, n_samples=NUMBER_OF_SAMPLES, sample_size=SAMPLE_SIZE)
