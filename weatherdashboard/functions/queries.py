import streamlit as st
import pandas as pd
import requests
from streamlit_js_eval import streamlit_js_eval
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
                SELECT dates, weekday_name, department, temp, tempmin, tempmax, feelslike, feelslikemin, feelslikemax, descriptions, weekday_name
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
                geojson,
                solarenergy_kwhpm2,
                solarradiation,
                reg_name,
                avg_solarenergy_kwhpm2,
                avg_solarradiation

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


    def get_tfptwgp(self, department):
        """
        Get some interesting features like tfptwgp as :
        Temperature, Feels like, Pecipitation, Wind, Gust and Pressure
        """

        query = f"""
                SELECT dates, department, reg_name, windspeed,
                windgust, pressure, solarenergy_kwhpm2, temp, feelslike,
                precip
                FROM `{PROJECT_ID}.{self.datasets[0]}.mart_newdata`
                WHERE department = '{department}'
                ORDER BY dates
                """
        table_result = self._run_query(query=query)
        return table_result

    def get_sunshine_data(self):
        """
        Get some interesting features like tfptwgp as :
        Temperature, Feels like, Pecipitation, Wind, Gust and Pressure
        """

        query = f"""
                SELECT dates, reg_name, department, solarenergy_kwhpm2, solarradiation
                FROM `{PROJECT_ID}.{self.datasets[0]}.mart_newdata`
                ORDER BY dates
                """
        table_result = self._run_query(query=query)
        return table_result

    def get_region_sunshine_data(self, region):
        """
        """
        query = f"""
                SELECT department, reg_name, solarenergy_kwhpm2, solarradiation
                FROM `{PROJECT_ID}.{self.datasets[0]}.mart_newdata`
                WHERE reg_name = '{region}'
                """
        table_result = self._run_query(query=query)
        return table_result

    def get_solarenergy_agg_pday(self, department):
        """
        We take into account the calculation over 8 days as recorded
        Panel area = 2.7 m²
        Panel efficiency = 21.7%
        """
        query = f"""
                SELECT department,
                AVG(solarenergy_kwhpm2) AS solarenergy_kwhpm2,
                AVG(solarenergy_kwhpm2) * 2.7 AS available_solarenergy_kwhc,
                AVG(solarenergy_kwhpm2) * 2.7 * 0.217 AS real_production_kwhpday
                FROM `{PROJECT_ID}.{self.datasets[0]}.mart_newdata`
                WHERE department= '{department}'
                GROUP BY department
                """
        table_result = self._run_query(query=query)
        return table_result

    def get_location(self):
        """
        """

        try:
            user_location = streamlit_js_eval(js_expressions="navigator.geolocation.getCurrentPosition((pos) => pos.coords)", key="geo_position")
            st.write(user_location)
            if user_location:
                latitude = user_location["latitude"]
                longitude = user_location["longitude"]
                st.write(f"lon={longitude}&lat={latitude}")
                # search now the department
                url = f"https://api-adresse.data.gouv.fr/reverse/?lon={longitude}&lat={latitude}"
                response = requests.get(url).json()

                if response.get("features"):
                    department = response["features"][0]["properties"]["context"].split(", ")[1]
                    st.write(f"📍 You are currently in **{department}** department")
                    return department

                else:
                    st.error("Can't get department.")
                    st.warning("Can't get your location. Please accept geolocation to continue.")
        except Exception as e:
            st.error(f"Error when retrieving location : {e}")



if __name__ == "__main__":
    queries = WeatherQueries()
