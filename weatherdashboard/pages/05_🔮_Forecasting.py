import streamlit as st

st.set_page_config(page_title="Weather Forecasting",
                 layout="wide",
                 page_icon="🔮")

import sys
sys.path.append("/app")

st.markdown("# 🔮 Time Series Forecasting")

st.info(
    """
    #### 🚀 Coming Soon: Advanced Forecasting Models

    This page will provide predictive analytics for weather and energy data:
    - **Solar Energy Forecasts**: 15-day production predictions and efficiency trends
    - **Weather Predictions**: Temperature and precipitation trends
    - **Seasonal Analysis**: Long-term energy patterns

    #### 📍 Explore Other Pages
    In the meantime, check out the available dashboards:
    - **📈 Weather Statistics**: Detailed meteorological data and trends
    - **📊 Analytics**: Interactive maps and weather patterns by department/region
    - **☀️ Solar Energy**: Regional solar distribution and geographic analysis
    - **⚡ Home Energy Planner**: Calculate energy autonomy from solar availability
    """
)
