
from datetime import datetime

moment = datetime.now()
path = '~/Documents/notes/'
text = input('text: ')
name = input('name: ').replace(' ', '_')
name = name + "{:_%y%m%d_%H%M%p}".format(moment)

with open(f'{path}{name}.txt', 'w') as f:
    f.write(text)
