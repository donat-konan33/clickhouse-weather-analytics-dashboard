"""here are all data that will make up for this weather-based studies
"""
import sys
sys.path.append("/app")

import altair as alt
import streamlit as st
import pandas as pd
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

        line_chart = (
            alt.Chart(temp_data).mark_line().encode(y=feature_option, x="dates")
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

        geo_data = self.state.get_query_result()




if __name__ == "__main__":

    st.title("Weather Data visualizations")
    data_visualization = DataVisualizations()

    data_visualization.temperature()
