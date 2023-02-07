import os
import pandas as pd

path = os.getcwd()

all_files = [f for f in os.listdir(path) if f.endswith('.parquet')]

df = pd.DataFrame()
for file in all_files:
    current_df = pd.read_parquet(os.path.join(path, file))
    df = pd.concat([df, current_df], axis=0, ignore_index=True)

