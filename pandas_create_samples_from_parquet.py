import sys
import pandas as pd


def pdprq(fl_nm=""):
    if fl_nm=="":
        fl_nm = input("PARQUET: ")
        return pd.read_parquet(fl_nm)
    else:
        return pd.read_parquet(fl_nm)

def create_samples(df_source,n_samples=1, sample_size=200):
    lst_nm = []
    for x in range(1, n_samples+1):
        tmp = df_source.sample(n=sample_size)
        tmp.to_parquet(f"sample_{x}.parquet",index =False)
        lst_nm.append(f"sample_{x}")
    return lst_nm

try:
    FILE = sys.argv[1]
    NUMBER_OF_SAMPLES = int(sys.argv[2])
    SAMPLE_SIZE = int(sys.argv[3])
    df = pdprq(fl_nm=FILE)
    for i,v in enumerate(["FILE","NUMBER_OF_SAMPLES","SAMPLE_SIZE"]):
        print(f"{v} = {sys.argv[i+1]}")

except:
    df = pdprq()
    NUMBER_OF_SAMPLES = int(input("NUMBER_OF_SAMPLES: ")) 
    SAMPLE_SIZE = int(input("SAMPLE_SIZE: "))        

lst_nm = create_samples(df_source=df, n_samples=NUMBER_OF_SAMPLES, sample_size=SAMPLE_SIZE)
