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

class DataVisualizations:
    def __init__(self) -> None:
        self.bq_client = WeatherDataWarehouse().db_client
        self.state = WeatherState()
        self.queries = WeatherQueries()

    # temperaure and feels like


    def temp_feels(self, ):
        """
        """

        pass

    # Precipitation and total
    def precip_total():
        """
        """

        pass


    # wind , gust and pressure
    def wind_gust_pressure():
        """
        """

        pass

    def france_map():
        """
        """

        pass




if __name__ == "__main__":

    bq_client = WeatherDataWarehouse().db_client
    st.title("Weather Data visualizations")
