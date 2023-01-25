# %%
import sys
import pandas as pd
import json
import unicodedata
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

pd.options.mode.chained_assignment = None

def strip_accents(string_input):
    string_input = str(string_input)
    string_cleaned = ''.join(c for c in unicodedata.normalize('NFD', string_input)if unicodedata.category(c) != 'Mn')
    return string_cleaned.strip().upper()

def clean_first(df_ref, df_tgt, col_ref, col_tgt):
    df_ref['tmp'] = df_ref[col_ref].apply(lambda x: strip_accents(x))
    df_tgt['tmp'] = df_tgt[col_tgt].apply(lambda x: strip_accents(x))
    return df_ref, df_tgt

def best_guess(df, word):
    if word=="NONE":
        return [0, None]
    df["correlation"] = [fuzz.ratio(word,s) for s in df["tmp"].tolist()]
    df["target"] = word
    df["guess"] = df["tmp"] 
    res = df.sort_values("correlation",ascending=False)[["correlation","guess"]]
    return res.iloc[0].tolist()

def pdprq(fl_nm=""):
    if fl_nm=="":
        fl_nm = input("PARQUET: ")
        return pd.read_parquet(fl_nm)
    else:
        return pd.read_parquet(fl_nm)

try: 
    df_ref = pd.read_parquet(sys.argv[1])
    fl_nm = sys.argv[2]
    df_tgt = pd.read_parquet(sys.argv[2])
    col_ref = sys.argv[3]
    col_tgt = sys.argv[4]
    for i,v in enumerate(["file_ref","file_target","column_ref","column_tgt"]):
        print(f"{v} =  {sys.argv[i+1]}")
except: 
    print("--FILE_REF--")
    df_ref = pdprq()
    print("--FILE_TARGET--")
    df_tgt = pdprq()
    col_ref = input("column_ref:")
    col_tgt = input("column_target:")

df_ref, df_tgt = clean_first(df_ref, df_tgt, col_ref, col_tgt)

df_tgt["guess"] = None
df_tgt["correlation"] = None

n = df_tgt.shape[0]
for i,val in enumerate(df_tgt["tmp"]):
   correlation, guess = best_guess(df=df_ref, word=val)
   df_tgt["correlation"].iloc[i] = correlation 
   df_tgt["guess"].iloc[i] = guess
   if i % 100==0:
       print(f"{i}/{n} --- {round((i*100)/n)}%")

df = df_tgt.sort_values("correlation",ascending=False)
df.drop(columns="tmp",inplace=True)
df.to_parquet(fl_nm, index=False)
print(df)
