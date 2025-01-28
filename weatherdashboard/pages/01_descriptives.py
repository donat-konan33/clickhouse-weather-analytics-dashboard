"""
The page with the descriptive statistics allows a user of this dashboard
to get the summary statistics of the tables in the database.
"""

import streamlit as st
from weatherdashboard.functions.state import WeatherState
from weatherdashboard.functions.constants import WeatherConstants
from weatherdashboard.functions.database import WeatherDataWarehouse
from weatherdashboard.functions.queries import WeatherQueries


class DescriptiveStatistics:
    def __init__(self) -> None:
        """Initialize the class"""
        self.weather_state = WeatherState()
        self.weather_database = WeatherDataWarehouse()
        self.weather_queries = WeatherQueries()

    def select_table(self):
        """Select the weather feature to explore"""
        with st.sidebar:
            st.subheader("Select weather feature to explore")
            self.selected_table = st.selectbox("feature name", WeatherConstants.feature())  or "default_value"

    def summary_statistics(self):
        """st.write summary statistics of the selected dable"""
        st.title("Descriptive statistics")

        if self.selected_table in st.session_state:
            st.info(f"Retrieve the {self.selected_table} table from state...")

            table_results = self.weather_state.get_data_from_state(self.selected_table)

        else:
            st.info(f"Retrieve the {self.selected_table} table from the database...")

            table_results = self.weather_queries.retrieve_table(self.selected_table)

            st.info(f"Saving the {self.selected_table} table to state...")

            self.weather_state.store_in_state(self.selected_table, table_results)

        # TODO: describe the table_results data

        st.write(table_results.describe())


if __name__ == "__main__":
    data_visualizations = DescriptiveStatistics()
    data_visualizations.select_table()
    data_visualizations.summary_statistics()
