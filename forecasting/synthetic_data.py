import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_synthetic_cashflow():
    """
    Generate synthetic weekly cashflow data with trend and seasonality.
    
    Returns:
        pd.DataFrame: DataFrame with 'ds' (datetime) and 'y' (value) columns
    """
    # Generate weekly dates for 10 years
    end_date = datetime.now().replace(month=12, day=31)
    start_date = (end_date - timedelta(weeks=520)).replace(month=1, day=1)
    dates = pd.date_range(start=start_date, end=end_date, freq='W-MON')
    
    # Generate synthetic data with trend and seasonality
    n_weeks = len(dates)
    trend = np.linspace(10000, 50000, n_weeks)
    seasonality = 5000 * np.sin(2 * np.pi * dates.dayofyear / 365.25)
    noise = np.random.normal(0, 2000, size=n_weeks)
    
    # Combine components
    y = trend + seasonality + noise
    
    # Ensure no negative values
    y = np.maximum(y, 1000)
    
    return pd.DataFrame({
        'ds': dates,
        'y': y
    })

def save_synthetic_data_to_excel(filepath='data/synthetic_cashflow.xlsx'):
    """
    Generate and save synthetic data to an Excel file.
    
    Args:
        filepath (str): Path to save the Excel file
    """
    df = generate_synthetic_cashflow()
    df.to_excel(filepath, index=False)
    return df

if __name__ == "__main__":
    # Generate and save synthetic data when run directly
    import os
    os.makedirs('../data', exist_ok=True)
    save_synthetic_data_to_excel('../data/synthetic_cashflow.xlsx')
