import pandas as pd
import streamlit as st
from weatherdashboard.functions.database import WeatherDataWarehouse
from weatherdashboard.functions.constants import WeatherConstants
import os

PROJECT_ID = os.environ.get("PROJECT_ID")

class WeatherQueries:
    def __init__(self) -> None:
        self.bq_client = WeatherDataWarehouse().db_client
        self.datasets = WeatherConstants.dataset()

    # # Perform query.
    # # Uses st.experimental_memo to only rerun when the query changes or after 10 min.
    @st.cache_data(ttl=3600)
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
        bq_result_object = _self.bq_client.query(query)
        return bq_result_object.to_dataframe()

    def get_data(self, table_name):
        """
        Get a table from the mart dataset
        """
        query = f"""
                SELECT *
                FROM `{PROJECT_ID}.{self.datasets[0]}.{table_name}`
                """
        table_result = self._run_query(query=query)
        return table_result

    def get_temp_data(self, table_name, department):
        """
        Get temperature data like temp, fileslikemin, fileslikemax and feelslike
        """
        query = f"""
                SELECT dates, weekday_name, department, temp, tempmin, tempmax, feelslike, feelslikemin, feelslikemax
                FROM `{PROJECT_ID}.{self.datasets[0]}.{table_name}` where department='{department}' order by dates
                """
        table_result = self._run_query(query=query)
        return table_result


    def get_solarenergy_geo_data_data(self, table_name, date):
        """
        """
        query = f"""
        SELECT
                dates, weekday_name, department, geo_point_2d,
                ST_AsGeoJSON(geo_shape) AS geojson,
                solarenergy_kwhpm2,
                solarradiation
        FROM `{PROJECT_ID}.{self.datasets[0]}.{table_name}` where dates = '{date}'
        """
        table_result = self._run_query(query=query)
        return table_result


    def get_date(self):
        """
        """
        query = f"""
        SELECT distinct(dates) AS dates
        FROM `{PROJECT_ID}.{self.datasets[0]}.mart_newdata`
        ORDER BY dates
        """
        table_result = self._run_query(query=query)
        table_result['date'] = table_result.dates.astype("str")
        return table_result.date

if __name__ == "__main__":
    queries = WeatherQueries()
