#!/usr/bin/env python3
"""
Setup script for the Financial Forecasting Assistant.
This script generates the synthetic dataset and ensures all required directories exist.
"""
import os
from pathlib import Path

# Ensure data directory exists
DATA_DIR = Path(__file__).parent / 'data'
DATA_DIR.mkdir(exist_ok=True)

# Import after creating the data directory
from forecasting.synthetic_data import save_synthetic_data_to_excel

def main():
    """Generate synthetic data and print setup completion message."""
    print("Setting up Financial Forecasting Assistant...")
    
    # Generate and save synthetic data
    output_path = DATA_DIR / 'synthetic_cashflow.xlsx'
    print(f"Generating synthetic data at {output_path}...")
    df = save_synthetic_data_to_excel(str(output_path))
    
    print("\n✅ Setup complete!")
    print("\nTo start the app, run:")
    print("  streamlit run app.py")
    
    return df

if __name__ == "__main__":
    main()
