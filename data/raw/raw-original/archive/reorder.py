import pandas as pd

file_path = '/Users/pathcharapisit/Desktop/crop/crop-recommendation-system-for-smart-farming/data/raw/archive/crop_yield.csv'
print("Loading data...")
df = pd.read_csv(file_path)

# Rename columns to match other files
print("Renaming columns...")
df.rename(columns={
    'avg_temp_c': 'temperature',
    'total_rainfall_mm': 'rainfall',
    'avg_humidity_percent': 'humidity'
}, inplace=True)

# Define common columns in the standard order
common_cols = ['label', 'n', 'p', 'k', 'ph', 'temperature', 'rainfall', 'humidity']

# Get remaining columns
remaining_cols = [col for col in df.columns if col not in common_cols]

# Reorder
new_order = common_cols + remaining_cols
print("New column order:", new_order)
df = df[new_order]

# Save
print("Saving data...")
df.to_csv(file_path, index=False)
print("Done.")
