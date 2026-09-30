"""
Solar Energy Trends Analysis Page
Provides insights into solar radiation and energy distribution across France
"""

import streamlit as st
st.set_page_config(page_title="Weather Dashboard",
                 layout="wide",
                 page_icon="🌤️")

import sys
sys.path.append("/app")

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from functions.queries import WeatherQueries
from functions.state import WeatherState
from functions.constants import WeatherConstants



class SolarTrend:
    def __init__(self) -> None:
        """Initialize the class"""
        self.state = WeatherState()
        self.queries = WeatherQueries()
        self.constants = WeatherConstants()

        self.table_name = "mart_newdata"
        self.date = st.selectbox("Select a date to analyze solar trends", self.queries.get_date())
        self.geo_data = self.state.get_query_result("get_solarenergy_geo_data_data", self.date)


    def solar_energy_distribution_by_date(self):
        """Display solar energy distribution across dates"""
        data = self.state.get_query_result("get_sunshine_data")
        fig = px.violin(data, y="solarenergy_kwhpm2", box=True, points='all',
                       hover_data=data.columns, color="dates",
                       labels={"solarenergy_kwhpm2": "Solar Energy (kWh/m²)", "dates": "Date"},
                       title="Solar Energy Distribution Over Next 7 Days")
        st.plotly_chart(fig, use_container_width=True)

    def solar_energy_distribution_by_region(self):
        """Display solar energy distribution by region"""
        data = self.state.get_query_result("get_sunshine_data")
        fig = px.violin(data, y="solarenergy_kwhpm2", box=True, points='all',
                       hover_data=data.columns, color="reg_name",
                       labels={"solarenergy_kwhpm2": "Solar Energy (kWh/m²)", "reg_name": "Region"},
                       title="Solar Energy Distribution by Region")
        st.plotly_chart(fig, use_container_width=True)

    def france_aggregated_data(self):
        """Display aggregated solar data for entire France"""
        try:
            data = self.state.get_query_result("get_entire_data")
            st.dataframe(data, use_container_width=True)
            return data
        except Exception as e:
            st.error(f"Unable to load aggregated France data: {e}")
            return None


if __name__ == "__main__":
    st.markdown("# ☀️ Solar Energy Trends")
    st.markdown("### Solar Radiation Analysis Across France")

    data_visualizations = SolarTrend()

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("##### Raw Solar Energy Data")
    with col2:
        show_dataframe = st.checkbox("Show raw data")

    if show_dataframe:
        st.dataframe(data_visualizations.geo_data, use_container_width=True)

    st.markdown("---")
    st.subheader("📊 Solar Energy Distribution Over Time")
    data_visualizations.solar_energy_distribution_by_date()

    st.markdown("---")
    st.subheader("🗺️ Solar Energy Distribution by Region")
    data_visualizations.solar_energy_distribution_by_region()

    st.markdown("---")
    st.subheader("🇫🇷 Data Aggregated for France")
    data_visualizations.france_aggregated_data()
