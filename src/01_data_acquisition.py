import pandas as pd
import requests
import os
from datetime import datetime

def download_dataset():
    # URL for the Online Retail II dataset (2009-2011)
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00502/online_retail_II.xlsx"
    
    os.makedirs('data/raw', exist_ok=True)
    target_path = 'data/raw/online_retail_II.xlsx'
    
    if not os.path.exists(target_path):
        print(f"Downloading dataset from UCI... this may take 2-3 minutes.")
        response = requests.get(url)
        if response.status_status == 200:
            with open(target_path, 'wb') as f:
                f.write(response.content)
            print(f"Dataset downloaded: {datetime.now()}")
        else:
            print("Download failed. Please check your internet connection.")
            return False
    else:
        print("Dataset already exists locally.")
    return True

def load_raw_data():
    # We load the first sheet (2009-2010) as per standard project start
    df = pd.read_excel('data/raw/online_retail_II.xlsx', engine='openpyxl')
    return df

def generate_data_profile(df):
    profile_path = 'data/raw/data_profile.txt'
    with open(profile_path, 'w') as f:
        f.write("=== DATA PROFILE SUMMARY ===\n")
        f.write(f"Rows: {df.shape[0]}\n")
        f.write(f"Columns: {df.shape[1]}\n\n")
        f.write("Column Names & Types:\n")
        f.write(df.dtypes.to_string())
        f.write("\n\nMemory Usage:\n")
        f.write(str(df.memory_usage(deep=True).sum() / 1024**2) + " MB\n\n")
        f.write("First 5 Rows:\n")
        f.write(df.head().to_string())
    print(f" Data profile saved to {profile_path}")

if __name__ == "__main__":
    if download_dataset():
        df = load_raw_data()
        generate_data_profile(df)