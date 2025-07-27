# Financial Forecasting Assistant

A Streamlit-based web application for financial time series forecasting using Meta's Prophet library. This tool is designed for finance professionals who need to generate quick and accurate forecasts from their time series data.

## Features

- **Easy Data Upload**: Upload Excel files with your time series data
- **Automatic Column Detection**: Automatically detects date and numeric columns
- **Interactive Visualizations**: View forecasts with confidence intervals
- **Component Analysis**: Break down forecasts into trend, seasonality, and noise
- **Demo Mode**: Try the app with synthetic data before uploading your own
- **Export Results**: Download forecast results as CSV

## 🚀 Quick Start (Local Development)

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/financial-forecaster.git
   cd financial-forecaster
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app locally:
   ```bash
   streamlit run app.py
   ```

## ☁️ Deployment to Streamlit Cloud

Deploy your own instance of this app in just a few clicks:

[![Deploy to Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=yourusername/financial-forecaster)

Or follow these steps:

1. Push your code to a GitHub repository
2. Go to [Streamlit Cloud](https://share.streamlit.io/)
3. Click "New app"
4. Select your repository and branch
5. Set the main file to `app.py`
6. Click "Deploy!"

## 🎯 Usage

1. **Upload Data**: Click "Browse files" to upload an Excel file with your time series data
2. **Column Selection**: The app will try to automatically detect date and value columns
3. **Run Forecast**: Click "Run Forecast" to generate predictions
4. **Explore Results**: View the forecast plot, components, and download the results

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to `http://localhost:8501`

3. Either:
   - Upload your own Excel file with time series data, or
   - Use the built-in demo data

4. Select the appropriate date and value columns

5. Click "Run Forecast" to generate predictions

6. View the forecast and components, and download the results if needed

## Data Format

Your Excel file should contain at least two columns:
- A date column (will be automatically detected if possible)
- A numeric value column to forecast

Example:

| Date       | Revenue |
|------------|---------|
| 2023-01-01 | 10000   |
| 2023-01-08 | 10500   |
| 2023-01-15 | 9800    |

## How It Works

This application uses Facebook's [Prophet](https://facebook.github.io/prophet/) library for time series forecasting. Prophet is designed for business time series data that typically have strong seasonal effects and several seasons of historical data.

Key features of the forecasting model:
- Handles missing data and outliers
- Supports multiple seasonality (daily, weekly, yearly)
- Provides uncertainty intervals
- Robust to changes in the time series

## Customization

You can customize the forecasting by modifying the `train_prophet_model` function in `forecasting/prophet_model.py`. Some parameters you might want to adjust:

- `yearly_seasonality`: Fit yearly seasonality
- `weekly_seasonality`: Fit weekly seasonality
- `seasonality_mode`: 'additive' or 'multiplicative'
- `changepoint_prior_scale`: Adjusts trend flexibility
- `seasonality_prior_scale`: Adjusts strength of seasonality

## Troubleshooting

### Common Issues

1. **Date format not recognized**: 
   - Ensure your date column is in a standard date format
   - Try formatting the column as a date in Excel before saving

2. **No numeric columns found**:
   - Make sure your value column contains only numeric values
   - Check for non-numeric characters or text in your data

3. **Forecast looks unrealistic**:
   - The model works best with at least one year of historical data
   - Check for outliers that might be affecting the forecast

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Prophet](https://facebook.github.io/prophet/) - Forecasting library by Facebook
- [Streamlit](https://streamlit.io/) - For the web interface
- [Pandas](https://pandas.pydata.org/) - For data manipulation
- [Matplotlib](https://matplotlib.org/) - For visualization
