from getpass import getpass
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from cryptography.fernet import Fernet
import json
import sys


def gen_fernet_key(key_file='fernet.bin'):
    key = Fernet.generate_key()
    with open(key_file,'wb') as f:
        f.write(key) 

def get_fernet_key(key_file='fernet.bin'):
    with open(key_file,'rb') as f:
        key = f.read()
    return key

def encrypt_str(text = '', key_file='fernet.bin'):
    if text==None:
        return None
    text = str(text)
    key = get_fernet_key(key_file=key_file)
    fernet = Fernet(key)
    encMessage = fernet.encrypt(text.encode())
    return encMessage.decode()

def decrypt_str(text, key_file='fernet.bin'):
    key = get_fernet_key(key_file=key_file)
    fernet = Fernet(key)
    encMessage = text.encode()
    decMessage = fernet.decrypt(encMessage).decode()
    # if decMessage.isnumeric() == True:
    #     return int(decMessage)
    return decMessage

def encrypt_json_fernet(json_file = sys.argv[1] , key_file="/run/media/roberto/syek/fernet.bin"):
    
    with open(json_file,'r') as f:
        dct = json.load(f)
    
    for key,value in dct.items():
        dct[key] = encrypt_str(text = value, key_file=key_file)

    with open(json_file,'w') as f:
        json.dump(dct,f,indent=4)
    

def decrypt_json_fernet(json_file = sys.argv[1], key_file="/run/media/roberto/syek/fernet.bin"):

    with open(json_file,"r") as f:
        dct = json.load(f)

    for key,value in dct.items():
        dct[key] = decrypt_str(text = value, key_file=key_file)

    with open(json_file,'w') as f:
        json.dump(dct,f,indent=4)

decrypt_json_fernet()
