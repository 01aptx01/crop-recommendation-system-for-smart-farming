import pandas as pd
import os
import glob
from ydata_profiling import ProfileReport
import warnings
warnings.filterwarnings('ignore')

data_dir = '/Users/pathcharapisit/Desktop/crop/crop-recommendation-system-for-smart-farming/data/raw/pre-combine'
files = glob.glob(os.path.join(data_dir, '*.csv'))
output_dir = os.path.join(data_dir, 'yprofile_reports')
os.makedirs(output_dir, exist_ok=True)

print(f"Found {len(files)} CSV files. Starting EDA generation...")

for f in files:
    file_name = os.path.basename(f)
    print(f"Generating profile for {file_name}...")
    try:
        df = pd.read_csv(f)
        profile = ProfileReport(df, title=f"{file_name} Profiling Report", explorative=True)
        output_path = os.path.join(output_dir, file_name.replace('.csv', '_report.html'))
        profile.to_file(output_path)
        print(f"-> Saved report to {output_path}")
    except Exception as e:
        print(f"-> Error generating profile for {file_name}: {e}")

print("All profiles generated successfully.")
