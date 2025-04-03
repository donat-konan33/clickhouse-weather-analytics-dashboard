import streamlit as st
from weatherdashboard.functions.queries import WeatherQueries
import pandas as pd

class WeatherState:
    def __init__(self) -> None:
        """Initialize the cache class"""
        self.queries = WeatherQueries()

    def generate_unique_key(self, method_name, *args):
        """Generate a unique cache key
        Args:
            method_name (str): Th name of the method
            *args: arguments passed to the method

             Returns:
             str : a unique cache key
        """
        if args:
            args_str = "_".join(str(arg) for arg in args)
            return f"{method_name}_{args_str}"
        return method_name

    def store_in_state(self, key, value):
        """Store data in the cache

        Args:
            key (str): The key to store the data under
            value (str): The value to store
        """
        st.session_state[key] = value

    def get_data_from_state(self, key):
        """Get data from the cache if it exists

        Args:
            key (str): The key to get the data from

        Returns:
            pd.DataFrame: The data from the cache
        """
        if key not in st.session_state:
            self.store_in_state(key, None)
        return st.session_state[key]

    def get_query_result(self, weatherquery_method_to_call:str, *args):
        """Get query result from state or the database. Store in state if new

        Args:
            weatherquery_method_to_call (str): The query to run

        Returns:
            pd.DataFrame: The results of the query
        """
        try:
            key = self.generate_unique_key(weatherquery_method_to_call, *args)

            if key in st.session_state:
                st.info("Retrieving data from state...")
                return self.get_data_from_state(key)
            else:
                st.info("Retrieving data from GOOGLE BIGQUERY database...")
                results = getattr(self.queries, weatherquery_method_to_call)(*args) # dynamic method call
                self.store_in_state(weatherquery_method_to_call, results)
                return results
        except Exception as e:
            st.error(f"An error occurred while executing the query: {e}")
            return pd.DataFrame()
