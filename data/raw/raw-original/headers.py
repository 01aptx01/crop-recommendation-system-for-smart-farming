import pandas as pd
import glob
import os

path = '/Users/pathcharapisit/Desktop/crop/crop-recommendation-system-for-smart-farming/data/raw/**/*.csv'
files = glob.glob(path, recursive=True)

all_columns = []
for f in files:
    try:
        df = pd.read_csv(f, nrows=0)
        cols = list(df.columns)
        all_columns.append((f, cols))
    except Exception as e:
        print(f"Error reading {f}: {e}")

print("File Columns:")
for f, cols in all_columns:
    print(f"\n{os.path.basename(f)}:")
    print(cols)

# find common columns
if all_columns:
    common = set(all_columns[0][1])
    for f, cols in all_columns[1:]:
        common = common.intersection(set(cols))
    print(f"\nCommon columns across all files: {common}")
