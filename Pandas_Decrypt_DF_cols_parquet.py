# The following code performs data encryption and decryption operations on columns of a dataframe in Python.
# It uses the Fernet module from cryptography library to encrypt and decrypt data using symmetric encryption.
# Fernet ensures that the data remains confidential and also ensures that the original data cannot be altered.

# Importing necessary libraries
from getpass import getpass
from cryptography.fernet import Fernet
import json
import sys
import os
import pandas as pd

# Function to generate Fernet key and store it in binary file
def gen_fernet_key(key_file=os.environ['BINARY_KEY']):
    key = Fernet.generate_key()
    with open(key_file,'wb') as f:
        f.write(key)

# Function to retrieve the Fernet key from binary file
def get_fernet_key(key_file=os.environ['BINARY_KEY']):
    with open(key_file,'rb') as f:
        key = f.read()
    return key

# Function to encrypt a string using Fernet
def encrypt_str(text = '', key_file=os.environ['BLACK_KEY']):
    key = get_fernet_key(key_file=key_file)
    fernet = Fernet(key)
    encMessage = fernet.encrypt(text.encode())
    return encMessage.decode()

# Function to decrypt a string using Fernet
def decrypt_str(text, key_file=os.environ['BLACK_KEY']):
    key = get_fernet_key(key_file=key_file)
    fernet = Fernet(key)
    try:
        encMessage = text.encode()
        decMessage = fernet.decrypt(encMessage).decode()
        return decMessage
    except:
        return None

# Function to read a csv file into a pandas dataframe
def pdcsv(fl_nm):
    if fl_nm=="":
        fl_nm = input("CSV: ")
        return pd.read_csv(fl_nm)
    else:
        return pd.read_csv(fl_nm)

# Function to read a parquet file into a pandas dataframe
def pdprq(fl_nm):
    if fl_nm=="":
        fl_nm = input("PARQUET: ")
    else:
        return pd.read_parquet(fl_nm)

# Function to encrypt columns of a dataframe using Fernet encryption
def encrypty_col(df, lst_cols=[]):
    lst_cols = []
    if lst_cols == []:
        col = input("COLUMN_NAME:")
        lst_cols.append(col)
    for x in lst_cols:
        df[x]= df[x].apply(lambda x: encrypt_str(x))
    return df

# Function to decrypt columns of a dataframe using Fernet encryption
def decrypty_col(df, lst_cols=[]):
    lst_cols = []
    if lst_cols == []:
        col

def decrypty_col(df, lst_cols=[]):
    lst_cols = []
    if lst_cols == []:
        col = input("COLUMN_NAME:")
        lst_cols.append(col)
    for x in lst_cols:
        df[x]= df[x].apply(lambda x: decrypt_str(x))
    return df, lst_cols  

def sv_prq(df,fl_nm):
    df.to_parquet(fl_nm, index=False)

try:
    fl_nm=sys.argv[1] 
except:
    fl_nm=input("FILE: ")

df = pdprq(fl_nm)
df, lst_cols = decrypty_col(df)

sv_prq(df,fl_nm)

print(df[lst_cols])
