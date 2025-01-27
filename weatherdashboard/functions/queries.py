import pandas as pd
import streamlit as st
from weatherdashboard.functions.database import WeatherDatabase


class WeatherQueries:
    def __init__(self) -> None:
        self.conn = WeatherDatabase().db_connection

    # # Perform query.
    # # Uses st.experimental_memo to only rerun when the query changes or after 10 min.
    @st.cache_data(ttl=600)
    def _run_query(_self, query):
        """
        Base utility method queries a database using pandas and returning a dataframe

        Parameters
        ----------
        query: Str
            SQL query as a f-string

        Returns
        -------
        races: pandas.DataFrame
            Dataframe containing the result of the query

        """

        return pd.read_sql_query(query, _self.conn)

    # add all methods here to test


if __name__ == "__main__":
    queries = WeatherQueries()
