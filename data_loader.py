"""
data_loader.py - helper to load the cases CSV.
"""
import pandas as pd

def load_cases(path='cases.csv'):
    df = pd.read_csv(path)
    return df
