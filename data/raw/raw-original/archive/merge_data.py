import pandas as pd
import os

# Set paths
base_dir = '/Users/pathcharapisit/Desktop/crop/crop-recommendation-system-for-smart-farming/data/raw/archive'
yield_path = os.path.join(base_dir, 'crop_yield.csv')
soil_path = os.path.join(base_dir, 'state_soil_data.csv')
weather_path = os.path.join(base_dir, 'state_weather_data_1997_2020.csv')

# Load data
print("Loading data...")
yield_df = pd.read_csv(yield_path)
soil_df = pd.read_csv(soil_path)
weather_df = pd.read_csv(weather_path)

# Strip whitespace from state names to ensure proper matching
yield_df['state'] = yield_df['state'].str.strip()
soil_df['state'] = soil_df['state'].str.strip()
weather_df['state'] = weather_df['state'].str.strip()

# Merge soil data (on 'state')
print("Merging soil data...")
merged_df = yield_df.merge(soil_df, on='state', how='left')

# Merge weather data (on 'state' and 'year')
print("Merging weather data...")
merged_df = merged_df.merge(weather_df, on=['state', 'year'], how='left')

# Save back to crop_yield.csv
print("Saving merged data...")
merged_df.to_csv(yield_path, index=False)

print("Merge complete.")
