import pandas as pd
import numpy as np
from datetime import datetime
import json
import logging
import os

# Setup logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='logs/data_cleaning.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DataCleaner:
    """
    A pipeline class to clean raw retail data. 
    Handles missing values, cancelled orders, outliers, and type conversion.
    """
    def __init__(self, input_path='data/raw/online_retail_II.csv'):
        # Note: Changed to .csv as per your previous terminal output
        self.input_path = input_path
        self.df = None
        self.cleaning_stats = {
            'original_rows': 0,
            'rows_after_cleaning': 0,
            'rows_removed': 0,
            'retention_rate': 0,
            'steps_applied': []
        }

    def load_data(self):
        logging.info(f"Loading raw dataset from {self.input_path}...")
        # Check if file is Excel or CSV to avoid errors
        if self.input_path.endswith('.xlsx'):
            self.df = pd.read_excel(self.input_path, engine='openpyxl')
        else:
            self.df = pd.read_csv(self.input_path)
            
        # Standardizing column names
        column_mapping = {
            'Invoice': 'InvoiceNo',
            'Customer ID': 'CustomerID',
            'Price': 'UnitPrice'
        }
        self.df.rename(columns=column_mapping, inplace=True)
        self.cleaning_stats['original_rows'] = len(self.df)
        return self

    def remove_missing_customer_ids(self):
        initial = len(self.df)
        self.df = self.df.dropna(subset=['CustomerID'])
        self.cleaning_stats['steps_applied'].append({'step': 'remove_missing_customer_ids', 'removed': initial - len(self.df)})
        return self

    def handle_cancelled_invoices(self):
        initial = len(self.df)
        # Convert to string to safely check for 'C'
        self.df = self.df[~self.df['InvoiceNo'].astype(str).str.startswith('C')]
        self.cleaning_stats['steps_applied'].append({'step': 'handle_cancelled_invoices', 'removed': initial - len(self.df)})
        return self

    def handle_negative_quantities(self):
        initial = len(self.df)
        self.df = self.df[self.df['Quantity'] > 0]
        self.cleaning_stats['steps_applied'].append({'step': 'handle_negative_quantities', 'removed': initial - len(self.df)})
        return self

    def handle_zero_prices(self):
        initial = len(self.df)
        self.df = self.df[self.df['UnitPrice'] > 0]
        self.cleaning_stats['steps_applied'].append({'step': 'handle_zero_prices', 'removed': initial - len(self.df)})
        return self

    def handle_missing_descriptions(self):
        initial = len(self.df)
        self.df = self.df.dropna(subset=['Description'])
        self.cleaning_stats['steps_applied'].append({'step': 'handle_missing_descriptions', 'removed': initial - len(self.df)})
        return self

    def remove_outliers(self):
        initial = len(self.df)
        # IQR for Quantity
        Q1_q, Q3_q = self.df['Quantity'].quantile([0.25, 0.75])
        IQR_q = Q3_q - Q1_q
        self.df = self.df[(self.df['Quantity'] >= Q1_q - 1.5*IQR_q) & (self.df['Quantity'] <= Q3_q + 1.5*IQR_q)]
        
        # IQR for Price
        Q1_p, Q3_p = self.df['UnitPrice'].quantile([0.25, 0.75])
        IQR_p = Q3_p - Q1_p
        self.df = self.df[(self.df['UnitPrice'] >= Q1_p - 1.5*IQR_p) & (self.df['UnitPrice'] <= Q3_p + 1.5*IQR_p)]
        
        self.cleaning_stats['steps_applied'].append({'step': 'remove_outliers', 'removed': initial - len(self.df)})
        return self

    def remove_duplicates(self):
        initial = len(self.df)
        self.df = self.df.drop_duplicates()
        self.cleaning_stats['steps_applied'].append({'step': 'remove_duplicates', 'removed': initial - len(self.df)})
        return self

    def add_derived_columns(self):
        self.df['InvoiceDate'] = pd.to_datetime(self.df['InvoiceDate'])
        self.df['TotalPrice'] = self.df['Quantity'] * self.df['UnitPrice']
        self.df['Year'] = self.df['InvoiceDate'].dt.year
        self.df['Month'] = self.df['InvoiceDate'].dt.month
        self.df['DayOfWeek'] = self.df['InvoiceDate'].dt.dayofweek
        self.df['Hour'] = self.df['InvoiceDate'].dt.hour
        return self

    def convert_data_types(self):
        self.df['CustomerID'] = self.df['CustomerID'].astype(int)
        self.df['Country'] = self.df['Country'].astype('category')
        return self

    def save_cleaned_data(self):
        os.makedirs('data/processed', exist_ok=True)
        
        # Save CSV
        self.df.to_csv('data/processed/cleaned_transactions.csv', index=False)
        
        # Final Stats Calculation
        final_rows = len(self.df)
        original_rows = self.cleaning_stats['original_rows']
        
        self.cleaning_stats['rows_after_cleaning'] = final_rows
        self.cleaning_stats['rows_removed'] = original_rows - final_rows
        self.cleaning_stats['retention_rate'] = round(final_rows / original_rows, 4)
        
        # Save JSON Artifact
        with open('data/processed/cleaning_statistics.json', 'w') as f:
            json.dump(self.cleaning_stats, f, indent=4)
            
        print(f"--- Cleaning Complete ---")
        print(f"Rows Removed: {self.cleaning_stats['rows_removed']}")
        print(f"Final Retention Rate: {(self.cleaning_stats['retention_rate']*100):.2f}%")

    def run_pipeline(self):
        """Executes all cleaning steps in sequence."""
        self.load_data()
        self.remove_missing_customer_ids()
        self.handle_cancelled_invoices()
        self.handle_negative_quantities()
        self.handle_zero_prices()
        self.handle_missing_descriptions()
        self.remove_outliers()
        self.remove_duplicates()
        self.add_derived_columns()
        self.convert_data_types()
        self.save_cleaned_data()
        return self.df

if __name__ == "__main__":
    # Ensure this points to your actual raw file (csv or xlsx)
    RAW_DATA_PATH = 'data/raw/online_retail_II.xlsx' 
    
    cleaner = DataCleaner(input_path=RAW_DATA_PATH)
    cleaner.run_pipeline()