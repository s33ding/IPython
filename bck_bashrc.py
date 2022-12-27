from os import system

path_file = '~/.bashrc' 
path_bck = '~/Fedora/config/.bashrc'

system(f'cp {path_file} {path_bck}')

