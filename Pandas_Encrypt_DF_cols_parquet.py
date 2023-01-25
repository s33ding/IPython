from getpass import getpass
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from cryptography.fernet import Fernet
import json
import sys
import os
import pandas as pd

def gen_fernet_key(key_file=os.environ['BINARY_KEY']):
    key = Fernet.generate_key()
    with open(key_file,'wb') as f:
        f.write(key) 

def get_fernet_key(key_file=os.environ['BINARY_KEY']):
    with open(key_file,'rb') as f:
        key = f.read()
    return key

def encrypt_str(text = '', key_file=os.environ['BLACK_KEY']):
    if text==None:
        return None
    text = str(text)
    key = get_fernet_key(key_file=key_file)
    fernet = Fernet(key)
    encMessage = fernet.encrypt(text.encode())
    return encMessage.decode()

def decrypt_str(text, key_file=os.environ['BLACK_KEY']):
    key = get_fernet_key(key_file=key_file)
    fernet = Fernet(key)
    encMessage = text.encode()
    decMessage = fernet.decrypt(encMessage).decode()
    # if decMessage.isnumeric() == True:
    #     return int(decMessage)
    return decMessage

def pdcsv(fl_nm):
    if fl_nm=="":
        fl_nm = input("CSV: ") 
        return pd.read_csv(fl_nm)
    else:
        return pd.read_csv(fl_nm)

def pdprq(fl_nm):
    if fl_nm=="":
        fl_nm = input("PARQUET: ") 
        return pd.read_parquet(fl_nm)
    else:
        return pd.read_parquet(fl_nm)

def encrypty_col(df, lst_cols=[]):
    lst_cols = []
    if lst_cols == []:
        col = input("COL:")
        lst_cols.append(col)
    for x in lst_cols:
        df[x]= df[x].apply(lambda x: encrypt_str(x))
    return df  

def decrypty_col(df, lst_cols=[]):
    lst_cols = []
    if lst_cols == []:
        col = input("COL:")
        lst_cols.append(col)
    for x in lst_cols:
        df[x]= df[x].apply(lambda x: decrypt_str(x))
    return df

def sv_parquet(df,fl_nm):
    df.to_parquet(fl_nm, index=False)

try:
    fl_nm=sys.argv[1] 
except:
    fl_nm=input("FILE: ")

df = pdprq(fl_nm)
df = encrypty_col(df)
sv_parquet(df,fl_nm)

print(df)
