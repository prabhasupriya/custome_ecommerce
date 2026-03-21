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
    def __init__(self, input_path='data/raw/online_retail_II.xlsx'):
        self.input_path = input_path
        self.df = None
        self.cleaning_stats = {
            'original_rows': 0,
            'rows_after_cleaning': 0,
            'rows_removed': 0,
            'steps_applied': []
        }

    def load_data(self):
        logging.info("Loading raw dataset...")
        # Using openpyxl as identified in your VS Code error
        self.df = pd.read_excel(self.input_path, engine='openpyxl')
        # Standardizing column names for the 2009-2010 dataset
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
        self.df.to_csv('data/processed/cleaned_transactions.csv', index=False)
        self.cleaning_stats['rows_after_cleaning'] = len(self.df)
        with open('data/processed/cleaning_statistics.json', 'w') as f:
            json.dump(self.cleaning_stats, f, indent=4)
        print(f"Final Retention Rate: {(len(self.df)/self.cleaning_stats['original_rows']*100):.2f}%")

    def run_pipeline(self):
        self.load_data().remove_missing_customer_ids().handle_cancelled_invoices() \
            .handle_negative_quantities().handle_zero_prices().handle_missing_descriptions() \
            .remove_outliers().remove_duplicates().add_derived_columns().convert_data_types().save_cleaned_data()
        return self.df

if __name__ == "__main__":
    cleaner = DataCleaner()
    cleaner.run_pipeline()