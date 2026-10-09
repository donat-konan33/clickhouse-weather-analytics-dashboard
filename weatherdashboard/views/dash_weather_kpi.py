"""
This page gives information to sunshine
"""

import pandas as pd
import streamlit as st

import sys
sys.path.append("/app")

import json

import folium
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import plotly.express as px
from branca.colormap import LinearColormap

from functions.constants import WeatherConstants
from functions.queries import WeatherQueries
from functions.state import WeatherState
from typing import List

class WeatherTrend:
    def __init__(self, date=List[str]) -> None:
        """Initialize the class"""
        self.state = WeatherState()
        self.queries = WeatherQueries()
        self.constants = WeatherConstants()

        self.table_name = "mart_newdata"
        self.date = date
        self.geo_data = self.state.get_query_result(
            "get_solarenergy_geo_data_data", self.date
        )

    def france_dep_map(self):
        """ """
        geojson_data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": json.loads(row["geojson"]),
                    "properties": {
                        "department": row["department"],
                        "solarenergy_kwhpm2": row["solarenergy_kwhpm2"],
                        "solaradiation": row["solarradiation"],
                    },
                }
                for row in self.geo_data.to_dict("records")
            ],
        }
        num_colors = 30
        cmap = cm.get_cmap("coolwarm", num_colors)
        colors = [mcolors.to_hex(cmap(i)) for i in range(num_colors)]
        colormap = LinearColormap(
            colors=colors,
            vmin=self.geo_data["solarenergy_kwhpm2"].min(),
            vmax=self.geo_data["solarenergy_kwhpm2"].max(),
        )
        m = folium.Map(
            location=[46.603354, 1.888334], zoom_start=6, width='100%', height='100%', control_scale=True,
        )  # zoom on France centre
        folium.GeoJson(
            geojson_data,
            style_function=lambda feature: {
                "fillColor": colormap(feature["properties"]["solarenergy_kwhpm2"]),
                "color": "black",  # boundary color
                "weight": 1,
                "fillOpacity": 0.7,
            },
            tooltip=folium.GeoJsonTooltip(
                fields=[
                    "department",
                    "solarenergy_kwhpm2",
                    "solaradiation",
                ],  # properties to display
                aliases=[
                    "Department |",
                    "Solar Energy (kWh/m²) |",
                    "Solar Radiation (W/m²) |",
                ],  # fields name
                localize=True,
            ),
        ).add_to(m)

        # add color scale
        colormap.add_to(m)
        #st.write("Choropleth map of Solar Energy by department (kWh/m²)")
        return m # folium_static(m)

    def france_reg_map(self):
        """ """

        geojson_data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": json.loads(row["geojson"]),
                    "properties": {
                        "department": row["department"],
                        "reg_name": row["reg_name"],
                        "avg_solarenergy_kwhpm2": row["avg_solarenergy_kwhpm2"],
                        "avg_solarradiation": row["avg_solarradiation"],
                    },
                }
                for row in self.geo_data.to_dict("records")
            ],
        }
        num_colors = 30
        cmap = cm.get_cmap("coolwarm", num_colors)
        colors = [mcolors.to_hex(cmap(i)) for i in range(num_colors)]
        colormap = LinearColormap(
            colors=colors,
            vmin=self.geo_data["avg_solarenergy_kwhpm2"].min(),
            vmax=self.geo_data["avg_solarenergy_kwhpm2"].max(),
        )
        m = folium.Map(
            location=[46.603354, 1.888334], zoom_start=6, control_scale=True,
                use_container_width=True
        )  # zoom on France centre
        folium.GeoJson(
            geojson_data,
            style_function=lambda feature: {
                "fillColor": colormap(feature["properties"]["avg_solarenergy_kwhpm2"]),
                "color": "black",  # boundary color
                "weight": 1,
                "fillOpacity": 0.7,
            },
            tooltip=folium.GeoJsonTooltip(
                fields=[
                    "reg_name",
                    "avg_solarenergy_kwhpm2",
                    "avg_solarradiation",
                ],  # properties to display
                aliases=[
                    "Region |",
                    "Solar Energy (kWh/m²) |",
                    "Solar Radiation (W/m²) |",
                ],  # fields name
                localize=True,
            ),
        ).add_to(m)

        # add color scale
        colormap.add_to(m)
        #st.write("Choropleth map of Solar Energy by region (kWh/m²)")
        return m # folium_static(m)

    def violin_plot(
        self,
    ):
        """ """
        data = self.state.get_query_result("get_sunshine_data")
        fig = px.violin(
            data,
            y="solarenergy_kwhpm2",
            box=True,
            points="all",
            hover_data=data.columns,
            color="dates",
            labels={
            "solarenergy_kwhpm2": "Énergie solaire (kWh/m²)",
            "dates": "Dates",
            "color": "Dates",  # optionnel, pour la légende
        }
        )
        fig.update_layout(
            title="Distribution de l'énergie solaire par date",
            yaxis_title="Énergie solaire (kWh/m²)",
            xaxis_title="Dates"
        )
        return fig

    def violin_plot_by_region(self):
        """ """
        # pick_reg = st.selectbox("Select a region", self.constants.region())
        data = self.state.get_query_result("get_sunshine_data")
        fig = px.violin(
            data,
            y="solarenergy_kwhpm2",
            box=True,
            points="all",
            hover_data=data.columns,
            color="reg_name",
            labels={
            "solarenergy_kwhpm2": "Énergie solaire (kWh/m²)",
            "reg_name": "Région",
            "color": "Région",  # optionnel, pour la légende
        }
        )
        fig.update_layout(
            title="Distribution de l'énergie solaire par région",
            yaxis_title="Énergie solaire (kWh/m²)",
            xaxis_title="Région"
        )
        return fig

def fig(date):
    st.write("🌞 Données énergétiques")
    data_visualizations = WeatherTrend(date=date)

    data_visualizations.france_dep_map()
    data_visualizations.france_reg_map()
    data_visualizations.violin_plot()
    data_visualizations.violin_plot_by_region()

    return {
        "m_department_map": data_visualizations.france_dep_map(), # for folium_static
        "m_region_map": data_visualizations.france_reg_map(),
        "fig_violin_plot": data_visualizations.violin_plot(),
        "fig_violin_plot_by_region": data_visualizations.violin_plot_by_region()
    }

class WeatherKPI:
    def __init__(self) -> None:
        """Initialize the class"""
        self.state = WeatherState()
        self.queries = WeatherQueries()

    def get_weather_kpi(self, level: str="department", period:str="today", top:bool=True):
        """ """
        data = self.state.get_query_result(
            "get_analytics_stats", level, period, top
        )
        return data

def kpi(level: str="department", period:str="today", top:bool=True):
    """ """
    data_visualizations = WeatherKPI()
    data = data_visualizations.get_weather_kpi(level, period, top)
    return pd.DataFrame(data)


if __name__ == "__main__":
    kpi()
