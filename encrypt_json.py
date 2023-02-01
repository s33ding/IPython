import os
import sys
import json
from cryptography.fernet import Fernet

def gen_fernet_key(key_file=os.environ['BINARY_KEY']):
    """
    Generates a new Fernet encryption key and saves it to a file.
    :param key_file: filepath to save the generated key.
    :type key_file: str
    :return: None
    """
    key = Fernet.generate_key()
    with open(key_file, 'wb') as f:
        f.write(key) 

def get_fernet_key(key_file=os.environ['BINARY_KEY']):
    """
    Retrieves the Fernet encryption key from a file.
    :param key_file: filepath to retrieve the key from.
    :type key_file: str
    :return: Fernet key
    :rtype: bytes
    """
    with open(key_file, 'rb') as f:
        key = f.read()
    return key

def encrypt_str(text = '', key_file=os.environ['BINARY_KEY']):
    """
    Encrypts a string using Fernet encryption.
    :param text: string to encrypt
    :type text: str
    :param key_file: filepath to retrieve the Fernet key from.
    :type key_file: str
    :return: encrypted message
    :rtype: str
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
    Decrypts a string encrypted using Fernet encryption.
    :param text: encrypted string to decrypt
    :type text: str
    :param key_file: filepath to retrieve the Fernet key from.
    :type key_file: str
    :return: decrypted message
    :rtype: str
    """
    key = get_fernet_key(key_file=key_file)
    fernet = Fernet(key)
    encMessage = text.encode()
    decMessage = fernet.decrypt(encMessage).decode()
    return decMessage

def encrypt_json_fernet(json_file = sys.argv[1] , key_file=os.environ["BLACK_KEY"]):
    """
    Encrypts values of a JSON file using Fernet encryption.
    :param json_file: filepath to the JSON file
    :type json_file: str
    :param key_file: filepath to retrieve the Fernet key from.
    :type key_file: str
    :return: None
    """
    with open(json_file,'r') as f:
        dct = json.load(f)
    
    for key,value in dct.items():
        dct[key] = encrypt_str(text = value,

