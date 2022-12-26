import sys
import pandas as pd

fl = sys.argv[1] 
df = pd.read_csv(fl)
print(df)
