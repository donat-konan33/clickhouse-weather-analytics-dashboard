"""
Solar Energy Trends Analysis Page
Provides insights into solar radiation and energy distribution across France
"""

import streamlit as st
st.set_page_config(page_title="Solar Energy",
                 layout="wide",
                 page_icon="☀️")

import sys
sys.path.append("/app")

import pandas as pd
import json
import folium
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import folium_static
from branca.colormap import LinearColormap
import matplotlib.cm as cm
import matplotlib.colors as mcolors

from weatherdashboard.functions.queries import WeatherQueries
from weatherdashboard.functions.state import WeatherState
from weatherdashboard.functions.constants import WeatherConstants


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

    def france_dep_choropleth(self):
        """Display choropleth map of solar energy by department"""
        if self.geo_data is None or len(self.geo_data) == 0:
            st.warning("No geographic data available for this date")
            return

        geojson_data = {
            "type": "FeatureCollection",
            "features": [
                {"type": "Feature",
                 "geometry": json.loads(row["geojson"]),
                 "properties": {
                     "department": row["department"],
                     "solarenergy_kwhpm2": row["solarenergy_kwhpm2"],
                     "solarradiation": row.get("solarradiation", 0)
                 }
                 }
                for row in self.geo_data.to_dict("records")
            ]
        }

        num_colors = 30
        cmap = cm.get_cmap('YlOrRd', num_colors)
        colors = [mcolors.to_hex(cmap(i)) for i in range(num_colors)]
        colormap = LinearColormap(
            colors=colors,
            vmin=self.geo_data["solarenergy_kwhpm2"].min(),
            vmax=self.geo_data["solarenergy_kwhpm2"].max(),
        )

        m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)
        folium.GeoJson(
            geojson_data,
            style_function=lambda feature: {
                "fillColor": colormap(feature["properties"]["solarenergy_kwhpm2"]),
                "color": "black",
                "weight": 1,
                "fillOpacity": 0.7,
            },
            tooltip=folium.GeoJsonTooltip(
                fields=["department", "solarenergy_kwhpm2"],
                aliases=["Department", "Solar Energy (kWh/m²)"],
                localize=True,
            ),
        ).add_to(m)

        colormap.add_to(m)
        st.markdown("**Solar Energy Distribution by Department (kWh/m²)**")
        folium_static(m, width=1200, height=600)

    def france_reg_choropleth(self):
        """Display choropleth map of solar energy by region"""
        if self.geo_data is None or len(self.geo_data) == 0:
            st.warning("No geographic data available for this date")
            return

        geojson_data = {
            "type": "FeatureCollection",
            "features": [
                {"type": "Feature",
                 "geometry": json.loads(row["geojson"]),
                 "properties": {
                     "department": row["department"],
                     "reg_name": row.get('reg_name', 'N/A'),
                     "avg_solarenergy_kwhpm2": row.get("avg_solarenergy_kwhpm2", row["solarenergy_kwhpm2"]),
                 }
                 }
                for row in self.geo_data.to_dict("records")
            ]
        }

        num_colors = 30
        cmap = cm.get_cmap('YlOrRd', num_colors)
        colors = [mcolors.to_hex(cmap(i)) for i in range(num_colors)]

        avg_values = [f.get("properties", {}).get("avg_solarenergy_kwhpm2", 0)
                     for f in geojson_data["features"]]
        vmin = min(avg_values) if avg_values else 0
        vmax = max(avg_values) if avg_values else 1

        colormap = LinearColormap(
            colors=colors,
            vmin=vmin,
            vmax=vmax,
        )

        m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)
        folium.GeoJson(
            geojson_data,
            style_function=lambda feature: {
                "fillColor": colormap(feature["properties"]["avg_solarenergy_kwhpm2"]),
                "color": "black",
                "weight": 1,
                "fillOpacity": 0.7,
            },
            tooltip=folium.GeoJsonTooltip(
                fields=["reg_name", "avg_solarenergy_kwhpm2"],
                aliases=["Region", "Avg Solar Energy (kWh/m²)"],
                localize=True,
            ),
        ).add_to(m)

        colormap.add_to(m)
        st.markdown("**Solar Energy Distribution by Region (kWh/m²)**")
        folium_static(m, width=1200, height=600)

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
    <p class="solar-title">☀️ Solar Energy</p>
    """, unsafe_allow_html=True)

    st.markdown("Analyze solar radiation patterns and energy distribution across France")

    st.markdown("---")
    st.markdown("### 📅 Select Analysis Date")

    dates = WeatherQueries().get_date()
    selected_date = st.selectbox(
        "Choose a date to view solar energy distribution",
        dates,
        help="This will update all maps and data tables below"
    )

    data_visualizations = SolarTrend(selected_date=selected_date)

    st.markdown("---")
    data_visualizations.display_geographic_data()

    st.markdown("---")
    st.markdown("### 🗺️ Geographic Maps")

    col1, col2 = st.columns(2)
    with col1:
        show_dept_map = st.checkbox("📍 Show Department Map", value=True)
    with col2:
        show_region_map = st.checkbox("🗺️ Show Region Map", value=True)

    if show_dept_map:
        st.markdown("---")
        data_visualizations.france_dep_choropleth()

        if st.checkbox("📋 Show Department Data Table", key="dept_table"):
            dept_data = data_visualizations.geo_data[['department', 'solarenergy_kwhpm2']].sort_values('solarenergy_kwhpm2', ascending=False).copy()
            dept_data.columns = ['Department', 'Solar Energy (kWh/m²)']
            st.dataframe(dept_data, use_container_width=True, height=400)

    if show_region_map:
        st.markdown("---")
        data_visualizations.france_reg_choropleth()

        if st.checkbox("📋 Show Region Data Table", key="region_table"):
            if data_visualizations.geo_data is not None:
                region_data = data_visualizations.geo_data.drop_duplicates(subset=['reg_name']).copy()
                region_data = region_data[['reg_name', 'avg_solarenergy_kwhpm2']].sort_values('avg_solarenergy_kwhpm2', ascending=False)
                region_data.columns = ['Region', 'Solar Energy (kWh/m²)']
                st.dataframe(region_data, use_container_width=True, height=400)

    st.markdown("---")
    st.markdown("### 📊 Distribution Analysis")

    st.subheader("🗓️ Solar Energy Over Time (All 7 Days)")
    data_visualizations.solar_energy_distribution_by_date()

    st.markdown("---")
    st.subheader("🗺️ Solar Energy by Region (All Dates)")
    data_visualizations.solar_energy_distribution_by_region()
