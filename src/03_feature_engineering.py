import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

class FeatureEngineer:
    def __init__(self, 
                 transactions_path='data/processed/cleaned_transactions.csv',
                 training_cutoff='2010-06-01'):
        self.transactions = pd.read_csv(transactions_path, parse_dates=['InvoiceDate'])
        # Ensure CustomerID is integer
        self.transactions['CustomerID'] = self.transactions['CustomerID'].astype(int)
        
        # Calculate TotalPrice if missing
        if 'TotalPrice' not in self.transactions.columns:
            self.transactions['TotalPrice'] = self.transactions['UnitPrice'] * self.transactions['Quantity']
            
        self.training_cutoff = pd.to_datetime(training_cutoff)
        self.observation_end = self.transactions['InvoiceDate'].max()
        
        print(f"Loaded {len(self.transactions)} transactions")
        print(f"Training cutoff: {self.training_cutoff}")
        print(f"Observation end: {self.observation_end}")

    def split_data_by_time(self):
        print("\nSplitting data into training and observation periods...")
        self.training_data = self.transactions[self.transactions['InvoiceDate'] <= self.training_cutoff].copy()
        self.observation_data = self.transactions[self.transactions['InvoiceDate'] > self.training_cutoff].copy()
        print(f"Training transactions: {len(self.training_data)}")
        print(f"Observation transactions: {len(self.observation_data)}")
        return self

    def create_target_variable(self):
        print("\nCreating target variable (Churn)...")
        training_customers = set(self.training_data['CustomerID'].unique())
        observation_customers = set(self.observation_data['CustomerID'].unique())
        
        self.customer_features = pd.DataFrame({'CustomerID': list(training_customers)})
        # Logic: 1 if in training but NOT in observation
        self.customer_features['Churn'] = self.customer_features['CustomerID'].apply(
            lambda x: 1 if x not in observation_customers else 0
        )
        churn_rate = self.customer_features['Churn'].mean() * 100
        print(f"Churn rate: {churn_rate:.2f}%")
        return self

    def create_rfm_features(self):
        print("\nCreating RFM features...")
        df = self.training_data
        rfm = df.groupby('CustomerID').agg({
            'InvoiceDate': lambda x: (self.training_cutoff - x.max()).days, # Recency
            'InvoiceNo': 'nunique', # Frequency
            'TotalPrice': ['sum', 'mean'], # Monetary
            'StockCode': 'nunique', # Unique Products
            'Quantity': 'sum' # Total Items
        }).reset_index()
        rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'TotalSpent', 'AvgOrderValue', 'UniqueProducts', 'TotalItems']
        self.customer_features = self.customer_features.merge(rfm, on='CustomerID', how='left')
        return self

    def create_behavioral_features(self):
        print("\nCreating behavioral features...")
        df = self.training_data
        
        # 1. AvgDaysBetweenPurchases using diff()
        df_sorted = df.sort_values(['CustomerID', 'InvoiceDate'])
        df_sorted['Diff'] = df_sorted.groupby('CustomerID')['InvoiceDate'].diff().dt.days
        intervals = df_sorted.groupby('CustomerID')['Diff'].mean().reset_index()
        intervals.columns = ['CustomerID', 'AvgDaysBetweenPurchases']
        
        # 2. Basket Stats
        basket = df.groupby(['CustomerID', 'InvoiceNo'])['Quantity'].sum().reset_index()
        b_stats = basket.groupby('CustomerID')['Quantity'].agg(['mean', 'std', 'max']).reset_index()
        b_stats.columns = ['CustomerID', 'AvgBasketSize', 'StdBasketSize', 'MaxBasketSize']
        
        # 3. Time Prefs
        df['DayOfWeek'] = df['InvoiceDate'].dt.dayofweek
        df['Hour'] = df['InvoiceDate'].dt.hour
        time_prefs = df.groupby('CustomerID').agg({
            'DayOfWeek': lambda x: x.mode().iloc[0],
            'Hour': lambda x: x.mode().iloc[0],
            'Country': 'nunique'
        }).reset_index()
        time_prefs.columns = ['CustomerID', 'PreferredDay', 'PreferredHour', 'CountryDiversity']
        
        self.customer_features = self.customer_features.merge(intervals, on='CustomerID', how='left') \
                                     .merge(b_stats, on='CustomerID', how='left') \
                                     .merge(time_prefs, on='CustomerID', how='left')
        return self

    def create_temporal_features(self):
        print("\nCreating temporal features...")
        df = self.training_data
        lt = df.groupby('CustomerID')['InvoiceDate'].agg(['min', 'max']).reset_index()
        lt['CustomerLifetimeDays'] = (lt['max'] - lt['min']).dt.days
        
        self.customer_features = self.customer_features.merge(lt[['CustomerID', 'CustomerLifetimeDays']], on='CustomerID', how='left')
        self.customer_features['PurchaseVelocity'] = self.customer_features['Frequency'] / (self.customer_features['CustomerLifetimeDays'] + 1)
        
        for days in [30, 60, 90]:
            cutoff = self.training_cutoff - timedelta(days=days)
            recent = df[df['InvoiceDate'] > cutoff].groupby('CustomerID')['InvoiceNo'].nunique().reset_index()
            col = f'Purchases_Last{days}Days'
            recent.columns = ['CustomerID', col]
            self.customer_features = self.customer_features.merge(recent, on='CustomerID', how='left').fillna({col: 0})
        return self

    def create_product_features(self):
        print("\nCreating product features...")
        df = self.training_data
        # Diversity: unique / total
        div = df.groupby('CustomerID').agg({'StockCode': [lambda x: len(set(x))/len(x), 'nunique']}).reset_index()
        div.columns = ['CustomerID', 'ProductDiversityScore', 'TotalUniqueProducts']
        
        price = df.groupby('CustomerID')['UnitPrice'].agg(['mean', 'std', 'min', 'max']).reset_index()
        price.columns = ['CustomerID', 'AvgPricePreference', 'StdPricePreference', 'MinPrice', 'MaxPrice']
        
        qty_avg = df.groupby(['CustomerID', 'InvoiceNo'])['Quantity'].sum().reset_index().groupby('CustomerID')['Quantity'].mean().reset_index()
        qty_avg.columns = ['CustomerID', 'AvgQuantityPerOrder']
        
        self.customer_features = self.customer_features.merge(div, on='CustomerID', how='left') \
                                     .merge(price, on='CustomerID', how='left') \
                                     .merge(qty_avg, on='CustomerID', how='left')
        return self

    def create_customer_value_segment(self):
        print("\nCreating customer value segments...")
        # RecencyScore (Quartiles, inverse)
        self.customer_features['RecencyScore'] = pd.qcut(self.customer_features['Recency'].rank(method='first'), q=4, labels=[4,3,2,1]).astype(int)
        # FrequencyScore
        self.customer_features['FrequencyScore'] = pd.qcut(self.customer_features['Frequency'].rank(method='first'), q=4, labels=[1,2,3,4]).astype(int)
        # MonetaryScore
        self.customer_features['MonetaryScore'] = pd.qcut(self.customer_features['TotalSpent'].rank(method='first'), q=4, labels=[1,2,3,4]).astype(int)
        
        self.customer_features['RFM_Score'] = self.customer_features['RecencyScore'] + self.customer_features['FrequencyScore'] + self.customer_features['MonetaryScore']
        
        def get_seg(s):
            if s >= 10: return 'Champions'
            if s >= 8: return 'Loyal'
            if s >= 6: return 'Potential'
            if s >= 4: return 'At Risk'
            return 'Lost'
        self.customer_features['CustomerSegment'] = self.customer_features['RFM_Score'].apply(get_seg)
        return self

    def handle_missing_values(self):
        print("\nHandling missing values...")
        numeric_cols = self.customer_features.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if col not in ['CustomerID', 'Churn']:
                self.customer_features[col] = self.customer_features[col].fillna(self.customer_features[col].median())
        return self

    def save_features(self):
        path = 'data/processed/'
        if not os.path.exists(path): os.makedirs(path)
        self.customer_features.to_csv(f'{path}customer_features.csv', index=False)
        
        info = {
            'total_customers': len(self.customer_features),
            'total_features': len(self.customer_features.columns) - 2,
            'churn_rate': float(self.customer_features['Churn'].mean()),
            'feature_list': list(self.customer_features.columns),
            'feature_categories': {
                'rfm': ['Recency', 'Frequency', 'TotalSpent', 'AvgOrderValue', 'UniqueProducts', 'TotalItems'],
                'behavioral': ['AvgDaysBetweenPurchases', 'AvgBasketSize', 'StdBasketSize', 'MaxBasketSize', 'PreferredDay', 'PreferredHour', 'CountryDiversity'],
                'temporal': ['CustomerLifetimeDays', 'PurchaseVelocity', 'Purchases_Last30Days', 'Purchases_Last60Days', 'Purchases_Last90Days'],
                'product': ['ProductDiversityScore', 'AvgPricePreference', 'StdPricePreference', 'MinPrice', 'MaxPrice', 'AvgQuantityPerOrder'],
                'segmentation': ['RecencyScore', 'FrequencyScore', 'MonetaryScore', 'RFM_Score', 'CustomerSegment']
            }
        }
        with open(f'{path}feature_info.json', 'w') as f:
            json.dump(info, f, indent=4)
        print(f"✅ Pipeline Complete. Features: {info['total_features']}, Churn: {info['churn_rate']*100:.2f}%")
        return self

    def run_pipeline(self):
        return (self.split_data_by_time().create_target_variable().create_rfm_features()
                .create_behavioral_features().create_temporal_features().create_product_features()
                .create_customer_value_segment().handle_missing_values().save_features().customer_features)

if __name__ == "__main__":
    engineer = FeatureEngineer(training_cutoff='2010-06-01')
    engineer.run_pipeline()