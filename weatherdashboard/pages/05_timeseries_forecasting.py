import streamlit as st

st.set_page_config(page_title="Weather Dashboard",
                 layout="wide",
                 page_icon="🔭")

st.markdown("# 🔭 Time Series Forecasting")

st.info(
    """
    #### 📊 Data Moved to Solar Trends Page

    The aggregated France weather data has been integrated into the **☀️ Solar Trends** page
    for a more cohesive analysis.

    Click the **☀️ Solar Trends** menu item to view:
    - Solar energy distribution patterns
    - Regional comparisons
    - Aggregated France data 🇫🇷

    #### 🚀 Coming Soon
    Advanced time series forecasting models for predicting:
    - 15-day solar energy production forecasts
    - Panel efficiency trends
    - Seasonal energy patterns
    """
)
