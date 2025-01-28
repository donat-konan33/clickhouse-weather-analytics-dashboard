import pandas as pd
import streamlit as st
from weatherdashboard.functions.database import WeatherDatabase
from weatherdashboard.functions.constants import WeatherConstants
import os

PROJECT_ID = os.environ.get("PROJECT_ID")

class WeatherQueries:
    def __init__(self) -> None:
        self.bq_client = WeatherDatabase().db_client
        self.datasets = WeatherConstants.dataset()

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
        table : pandas.DataFrame
            Dataframe containing the result of the query

        """

        return pd.read_sql_query(query, _self.bq_client)

    def get_mart_table(self, table_name):
        """
        Get a table from the mart dataset

        """
        query = f"""
                SELECT *
                FROM `{PROJECT_ID}.{self.datasets[3]}.{table_name}`
                """
        table_result = self._run_query(query=query)

        return table_result



if __name__ == "__main__":
    queries = WeatherQueries()
