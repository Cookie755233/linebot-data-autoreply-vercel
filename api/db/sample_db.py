import pandas as pd
import os

def fetch_db():
    return pd.read_csv(os.path.join(
        os.path.dirname(__file__), 'sample_data.csv'))