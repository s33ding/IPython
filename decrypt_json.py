import json
import sys
import os

# Utility functions for encrypting/decrypting text or a JSON file using the Fernet library.
# Fernet guarantees that a message encrypted using it cannot be further manipulated or read without the key.

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
from cryptography.fernet import Fernet

def gen_fernet_key(key_file=os.environ['BINARY_KEY']):
    """
    Generates a Fernet key and saves it to the specified file.
    :param key_file: file to save the key to (defaults to BINARY_KEY environment variable)
    """
    key = Fernet.generate_key()
    with open(key_file,'wb') as f:
        f.write(key) 

def get_fernet_key(key_file=os.environ['BINARY_KEY']):
    """
    Retrieves the Fernet key from the specified file.
    :param key_file: file to retrieve the key from (defaults to BINARY_KEY environment variable)
    :return: the Fernet key
    """
    with open(key_file,'rb') as f:
        key = f.read()
    return key

def encrypt_str(text = '', key_file=os.environ['BINARY_KEY']):
    """
    Encrypts a string using Fernet.
    :param text: string to encrypt
    :param key_file: file to retrieve the Fernet key from (defaults to BINARY_KEY environment variable)
    :return: encrypted string
    """
    if text==None:
        return None
    text = str(text)
    key = get_fernet_key(key_file=key_file)
    fernet = Fernet(key)
    encMessage = fernet.encrypt(text.encode())
    return encMessage.decode()

def decrypt_str(text, key_file=os.environ['BINARY_KEY']):
    """
    Decrypts a string using Fernet.
    :param text: string to decrypt
    :param key_file: file to retrieve the Fernet key from (defaults to BINARY_KEY environment variable)
    :return: decrypted string
    """
    key = get_fernet_key(key_file=key_file)
    fernet = Fernet(key)
    encMessage = text.encode()
    decMessage = fernet.decrypt(encMessage).decode()
    return decMessage

def encrypt_json_fernet(json_file = sys.argv[1] , key_file=os.environ["BLACK_KEY"]):
    """
    Encrypts values in a JSON file using Fernet.
    :param json_file: file to encrypt
    :param key_file: file to retrieve the Fernet key from (defaults to BLACK_KEY environment variable)
    """
    with open(json_file,'r') as f:
        dct = json.load(f)
    
    for key,value in dct.items():
        dct[key] = encrypt_str(text = value, key_file=key_file)
    with open(json_file,'w') as f:
        json.dump(dct,f,indent=4)
    

def decrypt_json_fernet(json_file = sys.argv[1], key_file=os.environ["BLACK_KEY"]):
    with open(json_file,"r") as f:
        dct = json.load(f)

    for key,value in dct.items():
        dct[key] = decrypt_str(text = value, key_file=key_file)

    with open(json_file,'w') as f:
        json.dump(dct,f,indent=4)

decrypt_json_fernet()

