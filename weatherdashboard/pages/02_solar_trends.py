"""
The page with the descriptive statistics allows a user of this dashboard
to get the summary statistics of the tables in the database.
"""

import streamlit as st
from weatherdashboard.functions.state import WeatherState
from weatherdashboard.functions.constants import WeatherConstants
from weatherdashboard.functions.database import WeatherDataWarehouse
from weatherdashboard.functions.queries import WeatherQueries


class SolarTrend:
    def __init__(self) -> None:
        """Initialize the class"""
        self.weather_state = WeatherState()
        self.weather_database = WeatherDataWarehouse()
        self.weather_queries = WeatherQueries()


if __name__ == "__main__":
    data_visualizations = SolarTrend()
