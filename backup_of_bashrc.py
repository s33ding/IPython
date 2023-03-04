import os 

path_file = '~/.bashrc' 
path_bck = os.environ['BASHRC_BCK']

os.system(f'cp {path_file} {path_bck}')
os.system(f'cd $ADM/config/.bashrc')
os.system(f"git add .;git commit -m 'saving'; git push")

