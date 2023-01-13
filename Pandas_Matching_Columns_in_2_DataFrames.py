# %%
import sys
import pandas as pd
import json
import myKit 
import unicodedata
from difflib import SequenceMatcher as sm

def strip_accents(string_input):
    """
    This function remove the accent of string so it can be more ease to make comparison 
    between between different strings, useful information

    ARGS: 
        string(str): The string that you wanna transform, it can be a value in a row or head column.
    RETURNS:
        string_cleaned(str): The sheet's name that will be used to create the DataFrame
    """
    string_input = str(string_input)
    string_cleaned = ''.join(c for c in unicodedata.normalize('NFD', string_input)if unicodedata.category(c) != 'Mn')
    return string_cleaned.strip().upper()

def clean_first(df_ref, df_tgt, col_ref, col_tgt):
    df_ref['tmp'] = df_ref[col_ref].apply(lambda x: strip_accents(x))
    df_tgt['tmp'] = df_tgt[col_tgt].apply(lambda x: strip_accents(x))
    return df_ref, df_tgt

def best_guess(df, col,target):
    df["correlation"] = [sm(a=s,b=target) for s in df[col].tolist()]
    df["target"] = target
    df["correlation"] = [x.ratio() for x in df["correlation"]]
    df["guess"] = df["tmp"] 
    return df.sort_values("correlation",ascending=False)[["correlation","guess"]].iloc[0].tolist()


def pdcsv(fl_nm):
    if fl_nm=="":
        fl_nm = input("CSV: ")
        return pd.read_csv(fl_nm)
    else:
        return pd.read_csv(fl_nm)

fl_ref = sys.argv[1]
fl_tgt = sys.argv[2]
col_ref = sys.argv[3]
col_tgt = sys.argv[4]

df_ref = pd.read_csv(fl_ref)
df_tgt = pd.read_csv(fl_tgt)

df_ref, df_tgt = clean_first(df_ref, df_tgt, col_ref, col_tgt)

df_tgt["guess"] = None
df_tgt["correlation"] = None
for i,val in enumerate(df_tgt["tmp"]):
   correlation, guess = best_guess(df=df_ref, col=col_ref, target=val)
   df_tgt["correlation"] = correlation 
   df_tgt["guess"] = guess
