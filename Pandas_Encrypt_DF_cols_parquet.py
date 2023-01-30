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
    """
    Generates a new Fernet key and saves it to a binary file

    :param key_file: (str) file path for the binary key file
    """
    key = Fernet.generate_key()
    with open(key_file,'wb') as f:
        f.write(key)

def get_fernet_key(key_file=os.environ['BINARY_KEY']):
    """
    Loads the Fernet key from the binary file

    :param key_file: (str) file path for the binary key file
    :return: (bytes) Fernet key
    """
    with open(key_file,'rb') as f:
        key = f.read()
    return key

def encrypt_str(text = '', key_file=os.environ['BLACK_KEY']):
    """
    Encrypts a string using the Fernet key

    :param text: (str) text to be encrypted
    :param key_file: (str) file path for the binary key file
    :return: (str) encrypted text
    """
    if text==None:
        return None
    text = str(text)
    key = get_fernet_key(key_file=key_file)
    fernet = Fernet(key)
    encMessage = fernet.encrypt(text.encode())
    return encMessage.decode()

def decrypt_str(text, key_file=os.environ['BLACK_KEY']):
    """
    Decrypts a string using the Fernet key

    :param text: (str) encrypted text
    :param key_file: (str) file path for the binary key file
    :return: (str) decrypted text
    """
    key = get_fernet_key(key_file=key_file)
    fernet = Fernet(key)
    encMessage = text.encode()
    decMessage = fernet.decrypt(encMessage).decode()
    return decMessage

def pdcsv(fl_nm):
    """
    Reads a CSV file into a pandas dataframe

    :param fl_nm: (str) file name for the CSV file
    :return: (pandas dataframe) data from the CSV file
    """
    if fl_nm=="":
        fl_nm = input("CSV: ")
        return pd.read_csv(fl_nm)
    else:
        return pd.read_csv(fl_nm)

def pdprq(fl_nm):
    """
    Reads a Parquet file into a pandas dataframe

    :param fl_nm: (str) file name for the Parquet file
    :return: (pandas dataframe) data from the Parquet file
    """
    if fl_nm=="":
        fl_nm = input("PARQUET: ")
        return pd.read_parquet(fl_nm)
    else:
        return pd.read_parquet(fl_nm)

def encrypt_col(df, lst_cols=[]):
    """Encrypts columns in a DataFrame
    
    Parameters:
    df (pandas.DataFrame): DataFrame to encrypt
    lst_cols (list): List of columns to encrypt. If left empty, a single column will be selected through user input.
    
    Returns:
    pandas.DataFrame: The encrypted DataFrame
    """
    if lst_cols == []:
        col = input("Enter column name to encrypt: ")
        lst_cols.append(col)
    for col in lst_cols:
        df[col]= df[col].apply(lambda x: encrypt_str(x))
    return df

def decrypt_col(df, lst_cols=[]):
    """Decrypts columns in a DataFrame
    
    Parameters:
    df (pandas.DataFrame): DataFrame to decrypt
    lst_cols (list): List of columns to decrypt. If left empty, a single column will be selected through user input.
    
    Returns:
    pandas.DataFrame: The decrypted DataFrame
    """
    if lst_cols == []:
        col = input("Enter column name to decrypt: ")
        lst_cols.append(col)
    for col in lst_cols:
        df[col]= df[col].apply(lambda x: decrypt_str(x))
    return df

def save_parquet(df, file_name):
    """Saves a DataFrame as a Parquet file
    
    Parameters:
    df (pandas.DataFrame): DataFrame to save
    file_name (str): Name of the file to save the DataFrame to
    
    Returns:
    None
    """
    df.to_parquet(file_name, index=False)

try:
    file_name = sys.argv[1]
except:
    file_name = input("Enter file name: ")

df = pd.read_parquet(file_name)
df = encrypt_col(df)
save_parquet(df, file_name)
