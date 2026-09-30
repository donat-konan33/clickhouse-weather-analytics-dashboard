"""
Solar Energy Trends Analysis Page
Provides insights into solar radiation and energy distribution across France
"""

import streamlit as st
st.set_page_config(page_title="Solar Energy Dashboard",
                 layout="wide",
                 page_icon="☀️")

import sys
sys.path.append("/app")

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from functions.queries import WeatherQueries
from functions.state import WeatherState
from functions.constants import WeatherConstants


class SolarTrend:
    def __init__(self, selected_date=None):
        """Initialize the class"""
        self.state = WeatherState()
        self.queries = WeatherQueries()
        self.constants = WeatherConstants()
        self.selected_date = selected_date

        if self.selected_date:
            self.geo_data = self.state.get_query_result("get_solarenergy_geo_data_data", self.selected_date)
        else:
            self.geo_data = None

    def display_geographic_data(self):
        """Display geographic solar energy data for selected date"""
        if self.geo_data is not None and len(self.geo_data) > 0:
            st.markdown("#### 📍 Solar Energy by Department")

            col1, col2, col3 = st.columns(3)
            with col1:
                avg_energy = self.geo_data['solarenergy_kwhpm2'].mean()
                st.metric("📊 Average", f"{avg_energy:.2f} kWh/m²")
            with col2:
                max_energy = self.geo_data['solarenergy_kwhpm2'].max()
                st.metric("⬆️ Maximum", f"{max_energy:.2f} kWh/m²")
            with col3:
                min_energy = self.geo_data['solarenergy_kwhpm2'].min()
                st.metric("⬇️ Minimum", f"{min_energy:.2f} kWh/m²")

            display_df = self.geo_data[['department', 'solarenergy_kwhpm2']].sort_values('solarenergy_kwhpm2', ascending=False).copy()
            display_df.columns = ['Department', 'Solar Energy (kWh/m²)']
            st.dataframe(display_df, use_container_width=True, height=300)
        else:
            st.warning("No geographic data available for the selected date")

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
    st.markdown("""
    <style>
    .solar-title {
        font-size: 40px;
        font-weight: bold;
        background: linear-gradient(135deg, #f39c12 0%, #e74c3c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    </style>
    <p class="solar-title">☀️ Solar Energy Forecast</p>
    """, unsafe_allow_html=True)

    st.markdown("Analyze solar radiation patterns and energy distribution across France")

    st.markdown("---")
    st.markdown("### 📅 Select Analysis Date")

    dates = WeatherQueries().get_date()
    selected_date = st.selectbox(
        "Choose a date to view solar energy distribution by department",
        dates,
        help="This will update the geographic data table below"
    )

    data_visualizations = SolarTrend(selected_date=selected_date)

    st.markdown("---")
    data_visualizations.display_geographic_data()

    st.markdown("---")
    st.markdown("### 📊 Distribution Analysis")

    st.subheader("🗓️ Solar Energy Over Time (All 7 Days)")
    data_visualizations.solar_energy_distribution_by_date()

    st.markdown("---")
    st.subheader("🗺️ Solar Energy by Region")
    data_visualizations.solar_energy_distribution_by_region()

    st.markdown("---")
    st.subheader("🇫🇷 Complete Dataset - All of France")
    data_visualizations.france_aggregated_data()
