from prophet import Prophet
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from typing import Tuple, Dict, Any

def prepare_data(df: pd.DataFrame, date_col: str, value_col: str) -> pd.DataFrame:
    """
    Prepare data for Prophet forecasting.
    
    Args:
        df (pd.DataFrame): Input DataFrame with time series data
        date_col (str): Name of the date column
        value_col (str): Name of the value column
        
    Returns:
        pd.DataFrame: DataFrame with columns 'ds' and 'y'
    """
    # Ensure required columns exist
    if date_col not in df.columns or value_col not in df.columns:
        raise ValueError(f"Required columns not found. Available columns: {df.columns.tolist()}")
    
    # Convert to datetime and numeric, handle missing values
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df[value_col] = pd.to_numeric(df[value_col], errors='coerce')
    
    # Drop rows with missing values
    df = df.dropna(subset=[date_col, value_col])
    
    # Sort by date
    df = df.sort_values(by=date_col)
    
    # Rename columns for Prophet
    df = df.rename(columns={
        date_col: 'ds',
        value_col: 'y'
    })
    
    return df[['ds', 'y']]

def train_prophet_model(df: pd.DataFrame) -> Tuple[Prophet, pd.DataFrame]:
    """
    Train a Prophet model on the given time series data.
    
    Args:
        df (pd.DataFrame): DataFrame with 'ds' (datetime) and 'y' (value) columns
        
    Returns:
        tuple: (fitted Prophet model, forecast DataFrame)
    """
    # Initialize and fit model
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        seasonality_mode='multiplicative',
        changepoint_prior_scale=0.05,
        seasonality_prior_scale=10.0
    )
    
    model.fit(df)
    
    # Create future dataframe for 52 weeks (1 year) forecast
    future = model.make_future_dataframe(periods=52, freq='W')
    
    # Make forecast
    forecast = model.predict(future)
    
    return model, forecast

def plot_forecast(model, forecast: pd.DataFrame, df: pd.DataFrame = None) -> plt.Figure:
    """
    Plot the forecast results.
    
    Args:
        model: Fitted Prophet model
        forecast (pd.DataFrame): Forecast DataFrame from model.predict()
        df (pd.DataFrame, optional): Original data points
        
    Returns:
        matplotlib.figure.Figure: The figure object
    """
    fig = model.plot(forecast, uncertainty=True)
    
    # Add original data points if provided
    if df is not None:
        plt.scatter(df['ds'], df['y'], color='black', s=10, label='Actual')
    
    plt.title('Forecast')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Format x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    return fig

def plot_components(model, forecast: pd.DataFrame) -> plt.Figure:
    """
    Plot forecast components.
    
    Args:
        model: Fitted Prophet model
        forecast (pd.DataFrame): Forecast DataFrame from model.predict()
        
    Returns:
        matplotlib.figure.Figure: The figure object
    """
    return model.plot_components(forecast)
