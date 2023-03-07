import sys
import pickle

def read_pickle_file(filename):
    try:
        with open(filename, 'rb') as f:
            data = pickle.load(f)
            print(f"Successfully read pickle file: {filename}")
            return data
    except FileNotFoundError:
        print(f"Error: file {filename} not found")
    except pickle.UnpicklingError:
        print(f"Error: invalid pickle file {filename}")

filename = sys.argv[1]
print(filename)
data = read_pickle_file(filename)
if data is not None:
    print("The pickle file has been loaded in a variable called 'data'.")
