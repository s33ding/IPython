import os 

path_file = '~/.bashrc' 
path_bck = os.environ['BASHRC_BCK']

os.system(f'cp {path_file} {path_bck}')
