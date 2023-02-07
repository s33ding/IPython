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

def creating_categories(df):

    df["quality"] = pd.cut(
            df.correlation,
            [0, 80, 85, 90, 100],
            right=True,
            labels=['BAD', 'NOT_BAD', 'GOOD','EXCELENT'])

    resume = pd.DataFrame(pd.value_counts(df["quality"]))
    resume.rename(columns={"quality":"total"},inplace=True)
    resume["%"] = (resume["total"]/resume["total"].sum())*100
    return df, resume


def best_guess(df, word):
    if word=="NONE":
        return [0, None]

    df["correlation"] = [fuzz.ratio(word,s) for s in df["tmp"].tolist()]
    df["target"] = word
    df["guess"] = df["nome"]
    res = df.sort_values("correlation",ascending=False)[["correlation","guess"]]

    return res.iloc[0].tolist()

def organizing_files(df_ref, df_tgt):
    df_ref = pd.read_parquet(df_ref)
    df_tgt = pd.read_parquet(df_tgt)
    return df_ref, df_tgt 

def df_transform(df_ref,df_tgt,col_ref,col_tgt):

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
    df.rename(columns={"tmp":"cleaned"},inplace=True)
    return df

def print_info(df, col_tgt, resume):
    print(df[[col_tgt,"guess","correlation"]])
    print(resume)
    

def big_process(
    df_ref = sys.argv[1],
    df_tgt = sys.argv[2],
    col_ref = sys.argv[3],
    col_tgt = sys.argv[4]
    ):

    df_ref, df_tgt = organizing_files(df_ref, df_tgt)
    df_ref, df_tgt = clean_first(df_ref, df_tgt, col_ref, col_tgt)
    df = df_transform(df_ref, df_tgt, col_ref, col_tgt)
    df,resume = creating_categories(df)
    print_info(df, col_tgt, resume)

    return df,resume

df,resume = big_process()
