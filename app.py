import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime, timedelta
import os

# Import local modules
from forecasting.prophet_model import prepare_data, train_prophet_model, plot_forecast, plot_components
from forecasting.synthetic_data import generate_synthetic_cashflow, save_synthetic_data_to_excel
from utils.excel_parser import parse_excel, detect_date_column, detect_numeric_columns

# Page config
st.set_page_config(
    page_title="Financial Forecasting Assistant",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stAlert {
        border-radius: 10px;
    }
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    </style>
""", unsafe_allow_html=True)

# App title and description
st.title("📊 Financial Forecasting Assistant")
st.markdown("""
Welcome to the Financial Forecasting Assistant! Upload your time series data in Excel format 
and get forecasts powered by Meta's Prophet algorithm.
""")

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'forecast' not in st.session_state:
    st.session_state.forecast = None
if 'model' not in st.session_state:
    st.session_state.model = None
if 'date_col' not in st.session_state:
    st.session_state.date_col = None
if 'value_col' not in st.session_state:
    st.session_state.value_col = None

# Sidebar for file upload and settings
with st.sidebar:
    st.header("📤 Data Input")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload Excel file", 
        type=["xlsx", "xls"],
        help="Upload an Excel file with time series data"
    )
    
    # Demo data toggle
    use_demo_data = st.checkbox(
        "Use demo data", 
        value=uploaded_file is None,
        help="Use synthetic demo data if no file is uploaded"
    )
    
    # If no file uploaded and demo data is selected, generate synthetic data
    if use_demo_data and st.session_state.df is None:
        st.session_state.df = generate_synthetic_cashflow()
        st.session_state.date_col = 'ds'
        st.session_state.value_col = 'y'
    
    # If file is uploaded, parse it
    elif uploaded_file is not None:
        try:
            df, metadata = parse_excel(uploaded_file.getvalue())
            st.session_state.df = df
            
            # Auto-detect date and value columns
            date_col = detect_date_column(df)
            numeric_cols = detect_numeric_columns(df, exclude_columns=[date_col] if date_col else [])
            
            # Column selectors
            if date_col:
                st.session_state.date_col = st.selectbox(
                    "Select date column", 
                    options=df.columns, 
                    index=df.columns.get_loc(date_col)
                )
            else:
                st.session_state.date_col = st.selectbox(
                    "Select date column", 
                    options=df.columns
                )
                
            if numeric_cols:
                st.session_state.value_col = st.selectbox(
                    "Select value column", 
                    options=numeric_cols,
                    index=0
                )
            else:
                st.session_state.value_col = st.selectbox(
                    "Select value column", 
                    options=df.columns
                )
                
        except Exception as e:
            st.error(f"Error parsing file: {str(e)}")
    
    # Forecast button
    run_forecast = st.button("Run Forecast", use_container_width=True)
    
    # Add some space
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    This app uses Meta's Prophet library for time series forecasting.
    
    **How to use:**
    1. Upload an Excel file with time series data
    2. Select date and value columns
    3. Click 'Run Forecast'
    4. View and download results
    """)

# Main content area
if st.session_state.df is not None:
    # Show data preview
    st.subheader("📋 Data Preview")
    st.dataframe(st.session_state.df.head(), use_container_width=True)
    
    # Run forecast when button is clicked
    if run_forecast and st.session_state.date_col and st.session_state.value_col:
        with st.spinner("Training model and generating forecast..."):
            try:
                # Prepare data for Prophet
                df_clean = prepare_data(
                    st.session_state.df, 
                    st.session_state.date_col, 
                    st.session_state.value_col
                )
                
                # Train model and get forecast
                st.session_state.model, st.session_state.forecast = train_prophet_model(df_clean)
                
                # Show success message
                st.success("Forecast generated successfully!")
                
            except Exception as e:
                st.error(f"Error generating forecast: {str(e)}")
    
    # Show forecast results if available
    if st.session_state.forecast is not None:
        st.subheader("📈 Forecast Results")
        
        # Create tabs for different visualizations
        tab1, tab2, tab3 = st.tabs(["Forecast", "Components", "Raw Data"])
        
        with tab1:
            # Plot forecast
            fig = plot_forecast(
                st.session_state.model, 
                st.session_state.forecast, 
                df_clean
            )
            st.pyplot(fig)
        
        with tab2:
            # Plot components
            fig_components = plot_components(st.session_state.model, st.session_state.forecast)
            st.pyplot(fig_components)
        
        with tab3:
            # Show forecast data
            st.dataframe(st.session_state.forecast, use_container_width=True)
            
            # Add download button for forecast data
            csv = st.session_state.forecast.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="forecast_results.csv">Download Forecast Data (CSV)</a>'
            st.markdown(href, unsafe_allow_html=True)

# If no data is loaded yet
else:
    st.info("👈 Please upload an Excel file or enable demo data to get started.")
    
    # Show example of expected data format
    with st.expander("ℹ️ Expected Data Format"):
        st.markdown("""
        Your Excel file should contain at least two columns:
        - A date column (e.g., 'Date', 'ds')
        - A numeric value column (e.g., 'Sales', 'Revenue', 'y')
        
        Example:
        """)
        example_df = pd.DataFrame({
            'Date': pd.date_range(start='2023-01-01', periods=5, freq='W'),
            'Value': [100, 120, 130, 115, 140]
        })
        st.dataframe(example_df)

# Add footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; font-size: 0.9em;">
    <p>Financial Forecasting Assistant v0.1 | Built with ❤️ using Streamlit and Prophet</p>
</div>
""", unsafe_allow_html=True)
