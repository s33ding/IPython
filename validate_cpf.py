#source-> https://pt.stackoverflow.com/questions/64608/como-validar-e-calcular-o-d%C3%ADgito-de-controle-de-um-cpf

import re

def validate_cpf(cpf=""):

    cpf = re.sub("\D","",cpf)
    cpf = [int(d) for d in cpf if d.isdigit()]

    if len(cpf) != 11 or len(set(cpf)) == 1:
        return ""

    my_sum = sum(a*b for a, b in zip(cpf[0:9], range(10, 1, -1)))
    expected_val = (my_sum * 10 % 11) % 10
    if cpf[9] != expected_val:
        return ""

    # Validação do segundo dígito verificador:
    my_sum = sum(a*b for a, b in zip(cpf[0:10], range(11, 1, -1)))
    expected_val = (my_sum * 10 % 11) % 10
    if cpf[10] != expected_val:
        return ""

    else:
        cpf = "".join([str(s) for s in cpf])
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"
    
cpf = input("CPF: ")
res = validate_cpf(cpf)
print(res)
