import pandas as pd
import glob
import os

path = '/Users/pathcharapisit/Desktop/crop/crop-recommendation-system-for-smart-farming/data/raw/**/*.csv'
files = glob.glob(path, recursive=True)

# standard mapping
mapping = {
    'nitrogen': 'n',
    'phosphorus': 'p',
    'phosphorous': 'p',
    'potassium': 'k',
    'temparature': 'temperature',
    'temp': 'temperature',
    'ph_value': 'ph',
    'soil_ph': 'ph',
    'crop type': 'label',
    'crop_type': 'label',
    'crop_label': 'label',
    'crop': 'label'
}

all_dfs = {}
for f in files:
    if 'data_dictionary' in f:
        continue
    try:
        df = pd.read_csv(f)
        # normalize column names
        new_cols = []
        for c in df.columns:
            c_low = str(c).lower().strip()
            new_c = mapping.get(c_low, c_low)
            new_cols.append(new_c)
        df.columns = new_cols
        all_dfs[f] = df
    except Exception as e:
        print(f"Error reading {f}: {e}")

# Find columns that appear in the datasets
col_counts = {}
for f, df in all_dfs.items():
    for c in df.columns:
        col_counts[c] = col_counts.get(c, 0) + 1

# Let's say common columns are those appearing in at least 3 files, excluding 'label'
common_cols = [c for c, count in col_counts.items() if count >= 3 and c != 'label']
# Sort common columns by frequency
common_cols.sort(key=lambda x: col_counts[x], reverse=True)

print("Label column and then common columns to be placed in front:")
print(['label'] + common_cols)

# Reorder columns
for f, df in all_dfs.items():
    cols = list(df.columns)
    
    first_cols = []
    if 'label' in cols:
        first_cols.append('label')
    
    # then common cols that are present in this df
    for cc in common_cols:
        if cc in cols:
            first_cols.append(cc)
            
    # then the rest
    rest_cols = [c for c in cols if c not in first_cols]
    
    new_order = first_cols + rest_cols
    df = df[new_order]
    
    # Save back to file
    df.to_csv(f, index=False)
    print(f"Processed {os.path.basename(f)} - Columns: {new_order[:10]}...")

