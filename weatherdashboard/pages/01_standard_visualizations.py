"""here are all data that will make up for this weather-based studies
"""
import sys
sys.path.append("/app")

import altair as alt
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static, st_folium
from branca.colormap import LinearColormap
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import json

from weatherdashboard.functions.database import WeatherDataWarehouse
from weatherdashboard.functions.queries import WeatherQueries
from weatherdashboard.functions.state import WeatherState
from weatherdashboard.functions.constants import WeatherConstants

class DataVisualizations:
    def __init__(self) -> None:
        self.bq_client = WeatherDataWarehouse().db_client
        self.state = WeatherState()
        self.queries = WeatherQueries()
        self.constants = WeatherConstants

    # temperaure and feels like
    def temperature(self, ):
        """
        """
        table = "mart_newdata"
        dep_option = st.selectbox("Select a department ", self.constants.department())
        feature_option = st.selectbox("Select a temperature feature", self.constants.temp_feature())
        temp_data = self.state.get_query_result("get_temp_data", table, dep_option)
        temp_data['date'] = pd.to_datetime(temp_data.dates)

        line_chart = (
            alt.Chart(temp_data).mark_line().encode(y=feature_option, x="date")
        )
        st.altair_chart(line_chart, use_container_width=True)


    # Precipitation and total
    def precip_total(self,):
        """
        """
        precip_data = self.state.get_query_result()


    # wind , gust and pressure
    def wind_gust_pressure(self,):
        """
        """
        wind_gust_pressure_data = self.state.get_query_result()

    def france_geo_map(self):
        """
        """
        table_name = "mart_newdata"
        date = st.selectbox("Select one of the 7 next days", self.queries.get_date())
        geo_data = self.state.get_query_result("get_solarenergy_geo_data_data", table_name, date)

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
            for row in geo_data.to_dict("records")
        ]
    }
        num_colors = 10
        cmap = cm.get_cmap('coolwarm', num_colors)
        colors = [mcolors.to_hex(cmap(i)) for i in range(num_colors)]
        colormap = LinearColormap(
                colors=colors,
                vmin=geo_data["solarenergy_kwhpm2"].min(),
                vmax=geo_data["solarenergy_kwhpm2"].max(),
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
        st.write("Choropleth map of France Solar Energy (kWh/m²)")
        folium_static(m)


if __name__ == "__main__":

    st.title("Weather Data visualizations")
    data_visualization = DataVisualizations()
    data_visualization.temperature()
    data_visualization.france_geo_map()
