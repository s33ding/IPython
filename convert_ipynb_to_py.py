import nbformat
import sys

# Get the input .ipynb file from the command line
input_file = sys.argv[1]

# Read the .ipynb file
with open(input_file) as f:
    nb = nbformat.read(f, as_version=4)

# Extract the code cells from the .ipynb file
code = '\n'.join(c['source'] for c in nb['cells'] if c['cell_type'] == 'code')

# Get the base name of the input file (without the extension)
base_name = input_file.split('.ipynb')[0]

# Write the code to a .py file
with open(base_name + '.py', 'w') as f:
    f.write(code)

