import pandas as pd

def load_cases(path='cases.csv'):
    return pd.read_csv(path)

def save_cases(df, path='cases.csv'):
    df.to_csv(path, index=False)
