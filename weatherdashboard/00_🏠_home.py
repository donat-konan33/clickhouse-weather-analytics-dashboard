import requests
import streamlit as st
st.set_page_config(page_title="Solar Energy Dashboard",
                 layout="wide",
                 page_icon="☀️")
import sys
sys.path.append("/app")
from functions.queries import WeatherQueries
from functions.state import WeatherState
from functions.constants import WeatherConstants
import numpy as np
from functions.api_client import APIClient

API_URL = st.secrets.get("api").get("BASE_URL", "http://localhost:8005")
API_KEY = st.secrets.get("api").get("API_KEY")

api_client = APIClient(base_url=API_URL, api_key=API_KEY)

class SolarEnergyDashboard:
    def __init__(self) -> None:
        self.state = WeatherState()
        self.department = WeatherQueries().get_location()
        self.constants = WeatherConstants().department()

        if not self.department:
            st.info("📍 Enable location access for personalized data")

    def get_data(self, department):
        """
        Get common data for department
        """
        data = self.state.get_query_result("get_temp_data", department)

        info_dict = dict(
            weekdayname=data.loc[0, "weekday_name"],
            descriptions=data.loc[0, "descriptions"],
            temperature=data.loc[0, "temp"],
            feelslike=data.loc[0, "feelslike"],
            tempmin=data.loc[0, "tempmin"],
            tempmax=data.loc[0, "tempmax"],
            department=data.loc[0, "department"],
        )

        return info_dict

    def display_info(self, info_dict):
        """Display weather information card"""
        html_content = f"""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    padding: 25px; border-radius: 10px; color: white; text-align: center;">
            <h2 style="margin: 10px 0; font-size: 3em; font-weight: bold;">{info_dict['temperature']}°C</h2>
            <h3 style="margin: 5px 0; font-size: 1.5em;">{info_dict['weekdayname']}</h3>
            <p style="margin: 5px 0; font-size: 1.2em; font-weight: bold;">📍 {info_dict['department']}</p>
            <hr style="border: 1px solid rgba(255,255,255,0.3); margin: 15px 0;">
            <p style="margin: 5px 0;">Range: {info_dict['tempmin']}° to {info_dict['tempmax']}°</p>
            <p style="margin: 5px 0;">Feels like: {info_dict['feelslike']}°</p>
            <p style="margin: 10px 0; font-style: italic;">{info_dict['descriptions']}</p>
        </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)


    def introduction_page(self):
        """Display attractive introduction page"""

        st.markdown("""
        <style>
        .title-font {
            font-size: 80px;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .subtitle {
            font-size: 28px;
            color: #666;
            font-weight: 500;
            margin-top: -20px;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown('<p class="title-font">☀️ Solar Energy Forecast</p>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Empower Your Renewable Energy Decisions</p>', unsafe_allow_html=True)

        col1, col2 = st.columns([3, 2], gap="large")

        with col1:
            st.markdown("""
            ### 🎯 Your All-in-One Solar Energy Platform

            Welcome to your personal solar energy advisor. This dashboard helps you understand weather patterns
            and solar radiation to optimize your photovoltaic panel usage and energy consumption.

            #### 📋 What You Can Do:

            **📊 Global Statistics**
            - Track temperature trends throughout the week
            - Monitor weather patterns across French departments
            - Understand local climate conditions

            **☀️ Solar Trends Analysis**
            - Interactive visualizations of solar energy distribution
            - Regional comparisons and forecasts
            - Daily and weekly solar radiation patterns

            **⚡ Smart Energy Consumption**
            - Calculate appliance autonomy with your solar panels
            - Select from 6 common household appliances
            - Predict energy independence days

            **🔮 Time Series Forecasting**
            - Advanced predictions of solar energy production
            - Machine learning models for better planning
            - 15-day energy outlook
            """)

        with col2:
            place = np.random.choice(self.constants)
            try:
                if self.department:
                    info_dict = self.get_data(self.department)
                else:
                    info_dict = self.get_data(place if place else "Paris")

                st.markdown("### 🌡️ Today's Weather")
                self.display_info(info_dict)

            except Exception as e:
                st.warning("⚠️ Weather data currently unavailable")

if __name__ == "__main__":
    try:
        api_client.health_check()
    except requests.exceptions.RequestException:
        st.error("🔌 Unable to connect to API.")
        st.stop()

    dashboard = SolarEnergyDashboard()
    dashboard.introduction_page()
