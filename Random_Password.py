import random 
import sys 
import string

def random_case(s):
    res = random.choice([0,1])
    if res == 0:
        return s
    else: return s.lower()

def random_password(n):
    n = int(n)
    lst_letters = [random_case(x) for x in string.ascii_uppercase] 
    lst_special_chars = "\/@".split()
    lst_digits = [str(x) for x in string.digits]
    lst = lst_letters + lst_digits + lst_special_chars + lst_special_chars
    return "".join([random.choice(lst) for x in range(n)])

res = random_password(sys.argv[1])
print(res)

