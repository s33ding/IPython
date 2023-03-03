import datetime
import os
import unicodedata
import json
import re
from pyspark.sql.functions import udf
from pyspark.sql.functions import broadcast
from pyspark.sql.types import *
import pickle

YEAR = datetime.date.today().year

with open(os.environ["lst_cities_from_brazil_ref"], 'rb') as f:
    lst_cities_from_brazil_ref= pickle.load(f)

# Read the JSON data from a file
with open(os.environ["dct_get_state_from_prefix_ref"], 'r') as file:
    dct_get_state_from_prefix_ref = json.load(file)

# Read the JSON data from a file
with open(os.environ["dct_cities_and_states_from_brazil_ref"], 'r') as file:
    dct_cities_and_states_from_brazil_ref = json.load(file)

# Read the JSON data from a file
with open(os.environ["dct_get_gender_from_name_ref"], 'r') as file:
    dct_get_gender_from_name_ref = json.load(file)

# Read the JSON data from a file
with open(os.environ["dct_cities_in_brazil_with_ambiguos_names_ref"], 'r') as file:
    dct_cities_in_brazil_with_ambiguos_names_ref = json.load(file)

lst_state_prefix = dct_get_state_from_prefix_ref.keys()
lst_cities = dct_cities_and_states_from_brazil_ref.keys()
lst_uf = dct_cities_and_states_from_brazil_ref.values()

@udf(returnType=StringType())
def check_uf(uf_val):
    if uf_val is None:
        return None
    if uf_val in lst_uf:
        return uf_val
    else: return None

@udf(returnType=BooleanType())
def check_ambiguos_name(val):
    return dct_cities_in_brazil_with_ambiguos_names_ref.get(val,None)

lst_uf = dct_cities_and_states_from_brazil_ref.values()
@udf(returnType=StringType())
def check_uf(uf_val):
    if uf_val is None:
        return None
    if uf_val in lst_uf:
        return uf_val
    else: return None

# Define the UDF
@udf(returnType=StringType())
def strip_accents(string_input):
    if string_input is None or string_input == "":
        return None
    string_input = str(string_input)
    string_cleaned = ''.join(c for c in unicodedata.normalize('NFD', string_input)if unicodedata.category(c) != 'Mn')
    return string_cleaned.strip().upper()

# Define the UDF
@udf(returnType=StringType())
def validate_cep(cep):
  if cep is None:
    return None
  cep = re.sub('[^0-9]', '', cep)
  cep = ''.join(char for char in cep if char.isalnum())
  try:
    if len(cep) != 8:
      raise ValueError
    else:
      cep = str(int(cep))
      return '{}.{}-{}'.format(cep[:2],cep[2:5],cep[5:])
  except ValueError:
      return None

@udf(returnType=StringType())
def validate_cns(cns):
    if cns is None:
        return None
    # Remove any non-numeric characters from the input string
    cns = ''.join(filter(str.isdigit, str(cns)))
    # Check if the input string has exactly 15 digits
    if len(cns) != 15:
        return None

    # Split the CNS number into three blocks
    block_1 = cns[:6]
    block_2 = cns[6:12]
    block_3 = cns[12:]

    # Calculate the verifier digits for each block
    verifier_1 = str(sum([int(digit) * weight for digit, weight in zip(block_1, reversed(range(2, 10)))]))
    verifier_2 = str(sum([int(digit) * weight for digit, weight in zip(block_2, reversed(range(2, 10)))]))
    verifier_3 = str(sum([int(digit) * weight for digit, weight in zip(block_3, reversed(range(2, 10)))]))

    # Pad the verifier digits with zeros if necessary
    verifier_1 = verifier_1[-2:].zfill(2)
    verifier_2 = verifier_2[-2:].zfill(2)
    verifier_3 = verifier_3[-2:].zfill(2)

    # Concatenate the blocks and verifier digits
    calculated_cns = block_1 + block_2 + block_3 + verifier_1 + verifier_2 + verifier_3
    # Return the input string if it's equal to the calculated CNS number, None otherwise
    cns_str = '{}.{}.{}.{}'.format(cns[:3],cns[3:7], cns[7:11], cns[11:])
    return cns_str if cns == calculated_cns else None

# Define the UDF
@udf(returnType=StringType())
def validate_cpf(numbers):
    cpf_bool = False
    numbers = re.sub('[^0-9]', '', str(numbers))
    cpf = [int(char) for char in numbers if char.isdigit()]
    if len(cpf) != 11:
        return None
    if cpf == cpf[::-1]:
        return None
    for i in range(9, 11):
        value = sum(cpf[num] * (i - num + 1) for num in range(i))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            return None
    cpf = ''.join(str(x) for x in cpf)
    return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}'

# Define the UDF
@udf(returnType=StringType())
def validate_email(email):
  if email is None:
    return None
  email = str(email).lower()
  email = ''.join(c for c in unicodedata.normalize('NFD', email)if unicodedata.category(c) != 'Mn')
  email = email.strip()
  try:
    val = re.search(r'[a-zA-Z0-9_-]+@[a-zA-Z0-9]+\.[a-zA-Z]{1,3}$', email)
    return email
  except:
    return None

# Define the UDF
@udf(returnType=StringType())
def validate_rg(rg):
    if rg is None:
        return None
    else:
        rg= ''.join(filter(str.isdigit, rg))

    if len(rg)==7:
        return f"{rg[:1]}.{rg[1:4]}.{rg[4:7]}"
    else:
        return None

@udf(returnType=DateType())
def validate_birth(data_nasc):
    try:
        if data_nasc is None:
            return None
        data_nasc = ''.join(filter(str.isdigit, str(data_nasc)))
        if len(data_nasc) != 8:
            return None
        nasc = int(data_nasc[:4])
        mes = int(data_nasc[4:6])
        dia = int(data_nasc[6:8])
        if nasc <= 0 or mes <= 0 or dia <= 0:
            return None
        elif dia > 31 or (mes in [4, 6, 9, 11] and dia > 30) or (mes == 2 and dia > 29):
            return None
        elif mes > 12:
            return None
        elif YEAR - nasc >= 18:
            return datetime.datetime(nasc, mes, dia)
        else:
            return None
    except:
        return None

@udf(returnType=IntegerType())
def calculate_age(data_nasc):
    if data_nasc is None:
        return None
    data_nasc = ''.join(filter(str.isdigit, data_nasc))
    if len(data_nasc) != 8:
        return None
    nasc = int(data_nasc[:4])
    mes = int(data_nasc[4:6])
    dia = int(data_nasc[6:8])
    hoje = date.today()
    try:
        aniversario = date(hoje.year, mes, dia)
    except ValueError:
        # caso em que o dia/mês é inválido para o ano atual (ex: 29 de fev em ano não bissexto)
        return None
    if aniversario > hoje:
        idade = hoje.year - nasc - 1
    else:
        idade = hoje.year - nasc
    return idade

def jaccard_similarity(s1, s2):
    set1 = set(s1.lower().split())
    set2 = set(s2.lower().split())
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union > 0 else 0

@udf(returnType=StringType())
def fuzzy_match_udf(cidade_val, uf_val):
    if cidade_val is None:
        return None
    else:
        best_match = max(lst_cities, key=lambda x: jaccard_similarity(cidade_val, x))
        correlation  = jaccard_similarity(cidade_val, best_match)
    for x in lst_cities_from_brazil_ref:
        lst = list(x)
        cidade_ref = lst[0]
        uf_ref = lst[1]
        ambiguos_name = lst[2]
        if cidade_ref == best_match:
            if ambiguos_name == False and uf_ref == uf_val:
                return f"{best_match};{correlation}"
            if ambiguos_name == False and correlation >= .85:
                return f"{best_match};{correlation}"
            if ambiguos_name == True and cidade_ref == best_match and uf_val==uf_ref:
                return f"{best_match};{correlation}"
    return None

@udf(returnType=StringType())
def find_uf(cidade_val, uf_val, ambiguos_name):
    if cidade_val is None:
        return None
    elif ambiguos_name == False:
        return dct_cities_and_states_from_brazil_ref.get(cidade_val)
    elif uf_val is not None or ambiguos_name == True:
        return uf_val
    else:
        return None

def prefix_br(number):
    if number[:2] == '55':
        brazil = True
        number = number[2:]
        return brazil, number
    else:
        brazil = False
        return brazil, number

def prefix_state(number):
    state = number[:2]
    brazil = False
    for x in lst_state_prefix:
        if state == str(x):
            number = number[2:]
            brazil = True
            return brazil,state, number
    state = False
    return brazil, state, number

@udf(returnType=StringType())
def transform_cellphone_number(number):
    brazil = False
    state = False
    if number is None:
        return None
    else:
        number = re.sub(r'\D', '', str(number))
    if number == "":
        return None
    brazil, number = prefix_br(number)
    brazil, state, number = prefix_state(number)
    if len(number) == 8:
        number = '9' + number
    if len(number) != 9:
        return  None
    if brazil == True:
        p1 = number[:5]
        p2 = number[5:]
        number = f"+55({state}){p1}-{p2}"
        return number
    else:
        return number

@udf(returnType=StringType())
def extract_ddd(string):
    if string is None:
        return None
    else:
        match = re.search(r"\((.*)\)", string)
    if match:
        return match.group(1)
    else:
        return None


@udf(returnType=StringType())
def extract_company_prefix(string):
    if string is None:
        return None
    else:
        string = re.sub(r'\D', '', string)
        string = string[5:7]
    try:
        return string
    except:
        return  None

@udf(returnType=StringType())
def get_uf_with_prefix(prefix_ddd):
    if prefix_ddd is None:
        return None
    else:
        return  dct_get_state_from_prefix_ref.get(prefix_ddd)

@udf(returnType=StringType())
def validate_sex(name):
    if name is None:
        return None
    else:
        return dct_get_gender_from_name_ref.get(name, None)

def s(df, col):
    result = df.select(col).where(df[col].isNotNull())
    result.show()
