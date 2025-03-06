"""
This page gives information to sunshine
"""

import streamlit as st
st.set_page_config(page_title="Weather Dashboard",
                 layout="wide",
                 page_icon="🌦️")

import sys
sys.path.append("/app")

import altair as alt
import pandas as pd
import folium
import json
from streamlit_folium import folium_static, st_folium
from branca.colormap import LinearColormap
import matplotlib.cm as cm
import matplotlib.colors as mcolors

import plotly.express as px
import plotly.graph_objects as go

from weatherdashboard.functions.queries import WeatherQueries
from weatherdashboard.functions.state import WeatherState
from weatherdashboard.functions.constants import WeatherConstants


class SolarTrend:
    def __init__(self) -> None:
        """Initialize the class"""
        self.state = WeatherState()
        self.queries = WeatherQueries()
        self.constants = WeatherConstants()

        self.table_name = "mart_newdata"
        self.date = st.selectbox("Select one of the 7 next days", self.queries.get_date())
        self.geo_data = self.state.get_query_result("get_solarenergy_geo_data_data", self.table_name, self.date)

    def france_dep_map(self):
        """
        """
        geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {"type": "Feature",
             "geometry": json.loads(row["geojson"]),
             "properties": {"department": row["department"],
                            "solarenergy_kwhpm2": row["solarenergy_kwhpm2"],
                            "solaradiation": row["solarradiation"]
                            }
             }
            for row in self.geo_data.to_dict("records")
        ]
    }
        num_colors = 30
        cmap = cm.get_cmap('coolwarm', num_colors)
        colors = [mcolors.to_hex(cmap(i)) for i in range(num_colors)]
        colormap = LinearColormap(
                colors=colors,
                vmin=self.geo_data["solarenergy_kwhpm2"].min(),
                vmax=self.geo_data["solarenergy_kwhpm2"].max(),
        )
        m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)  # zoom on France centre
        folium.GeoJson(
            geojson_data,
            style_function=lambda feature: {
                "fillColor": colormap(feature["properties"]["solarenergy_kwhpm2"]),
                "color": "black",  # boundary color
                "weight": 1,
                "fillOpacity": 0.7,
            },
            tooltip=folium.GeoJsonTooltip(
                fields=["department", "solarenergy_kwhpm2", 'solaradiation'],  # properties to display
                aliases=["Department |", "Solar Energy (kWh/m²) |", "Solar Radiation (W/m²) |"],  # fields name
                localize=True,
            ),
        ).add_to(m)

        # add color scale
        colormap.add_to(m)
        st.write("Choropleth map of Solar Energy by department (kWh/m²)")
        folium_static(m)


    def france_reg_map(self):
        """
        """

        geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {"type": "Feature",
             "geometry": json.loads(row["geojson"]),
             "properties": {"department": row["department"],
                            "reg_name": row['reg_name'],
                            "avg_solarenergy_kwhpm2": row["avg_solarenergy_kwhpm2"],
                            "avg_solarradiation": row["avg_solarradiation"]
                            }
             }
            for row in self.geo_data.to_dict("records")
        ]
    }
        num_colors = 30
        cmap = cm.get_cmap('coolwarm', num_colors)
        colors = [mcolors.to_hex(cmap(i)) for i in range(num_colors)]
        colormap = LinearColormap(
                colors=colors,
                vmin=self.geo_data["avg_solarenergy_kwhpm2"].min(),
                vmax=self.geo_data["avg_solarenergy_kwhpm2"].max(),
        )
        m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)  # zoom on France centre
        folium.GeoJson(
            geojson_data,
            style_function=lambda feature: {
                "fillColor": colormap(feature["properties"]["avg_solarenergy_kwhpm2"]),
                "color": "black",  # boundary color
                "weight": 1,
                "fillOpacity": 0.7,
            },
            tooltip=folium.GeoJsonTooltip(
                fields=["reg_name", "avg_solarenergy_kwhpm2", 'avg_solarradiation'],  # properties to display
                aliases=["Region |", "Solar Energy (kWh/m²) |", "Solar Radiation (W/m²) |"],  # fields name
                localize=True,
            ),
        ).add_to(m)

        # add color scale
        colormap.add_to(m)
        st.write("Choropleth map of Solar Energy by region (kWh/m²)")
        folium_static(m)


    def violin_plot(self,):
        """
        """
        data = self.state.get_query_result("get_sunshine_data")
        fig = px.violin(data, y="solarenergy_kwhpm2", box=True, points='all', hover_data=data.columns, color="dates")
        st.plotly_chart(fig)



    def viloin_plot_by_region(self):
        """
        """
        #pick_reg = st.selectbox("Select a region", self.constants.region())
        data = self.state.get_query_result("get_sunshine_data")
        fig = px.violin(data, y="solarenergy_kwhpm2", box=True, points='all', hover_data=data.columns, color="reg_name")
        st.plotly_chart(fig)



if __name__ == "__main__":
    st.write("# 🌞Sunshine Data")
    data_visualizations = SolarTrend()
    st.dataframe(data_visualizations.geo_data)

    col1, col2 = st.columns([2, 2])
    with st.subheader("Choropleth Map of Solar Energy of (France Metro)"):
        with col1:
            with st.container(border=True):
                data_visualizations.france_dep_map()

        with col2:
            with st.container(border=True):
                data_visualizations.france_reg_map()


    st.subheader("Violin Plot")
    data_visualizations.violin_plot()

    st.subheader("Violin Plot by region")
    data_visualizations.viloin_plot_by_region()
