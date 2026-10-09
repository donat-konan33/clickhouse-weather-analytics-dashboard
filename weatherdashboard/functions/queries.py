import os
import pandas as pd
import requests
import streamlit as st
from streamlit_js_eval import streamlit_js_eval

from .constants import WeatherConstants
from .api_client import APIClient

API_URL = st.secrets.get("api").get("BASE_URL")
API_KEY = st.secrets.get("api").get("API_KEY")

api_client = APIClient(base_url=API_URL, api_key=API_KEY)

class WeatherQueries:
    REFERENCE_PANEL_AREA_M2 = 2.7
    REFERENCE_PANEL_EFFICIENCY_PERCENT = 21.7

    def __init__(self) -> None:
        self.api_client = api_client
        self.datasets = WeatherConstants.dataset()
        self.features = WeatherConstants.features()

    def get_data(self) -> pd.DataFrame:
        """
        Get a table from the mart dataset
        """
        endpoint = "/get_data"
        result_table = self.api_client.get(endpoint)
        return pd.DataFrame(result_table)

    def get_temp_data(self, department) -> pd.DataFrame:
        """
        Get temperature data like temp, fileslikemin, fileslikemax and feelslike
        """
        endpoint = "/get_temp_data"
        params = {"department": department}
        result_table = self.api_client.get(endpoint, params=params)
        return pd.DataFrame(result_table)

    def get_solarenergy_geo_data_data(self, date) -> pd.DataFrame:
        """
        Get Solar energy data for all studied location by date
        """
        endpoint = "/solar_geo_data"
        params = {"date": date}
        result_table = self.api_client.get(endpoint, params=params)
        return pd.DataFrame(result_table)

    def get_date(self):
        """
        To get studied date window
        """
        endpoint = "/date"
        return self.api_client.get(endpoint)

    def get_tfptwgp(self, department):
        """
        Get some interesting features named tfptwgp as :
        Temperature, Feels like, Precipitation, Wind, Gust and Pressure
        """
        endpoint = "/common_features"
        params = {"department": department}
        result_table = self.api_client.get(endpoint, params=params)
        return pd.DataFrame(result_table)

    def get_sunshine_data(self):
        """
        Get some interesting features like tfptwgp as :
        Temperature, Feels like, Pecipitation, Wind, Gust and Pressure
        """
        endpoint = "/get_sunshine_data"
        result_table = self.api_client.get(endpoint)
        return pd.DataFrame(result_table)

    def get_region_sunshine_data(self, region):
        """
        Get region solar features
        """
        endpoint = "/get_region_sunshine_data"
        params = {"region": region}
        result_table = self.api_client.get(endpoint, params=params)
        return pd.DataFrame(result_table)

    def get_solarenergy_agg_pday(self, department):
        """
        Fetch solar production, calculated by the API for a reference panel
        area of 2.7 m² and a maximum efficiency of 21.7%.
        """
        endpoint = "/get_solarenergy_agg_pday"
        params = {"department": department}
        return self.api_client.get(endpoint, params=params)

    def get_location(self):
        """
        Automatically Get User LOcation
        """
        try:
            user_location = streamlit_js_eval(
                js_expressions="navigator.geolocation.getCurrentPosition((pos) => pos.coords)",
                key="geo_position",
            )
            st.write(user_location)
            if user_location:
                latitude = user_location["latitude"]
                longitude = user_location["longitude"]
                st.write(f"lon={longitude}&lat={latitude}")
                # search now the department
                url = f"https://api-adresse.data.gouv.fr/reverse/?lon={longitude}&lat={latitude}"
                response = self.api_client.get(url)

                if response.get("features"):
                    department = response["features"][0]["properties"]["context"].split(
                        ", "
                    )[1]
                    st.write(f"📍 You are currently in **{department}** department")
                    return department

                else:
                    st.error("Can't get department.")
                    st.warning(
                        "Can't get your location. Please accept geolocation to continue."
                    )
        except Exception as e:
            st.error(f"Error when retrieving location : {e}")

    def get_entire_department_data(self, department) -> pd.DataFrame:
        """Get local entire data for a department"""
        endpoint = "/get_entire_department_data"
        params = {"department": department}
        result_table = self.api_client.get(endpoint, params=params)
        return pd.DataFrame(result_table)

    def get_entire_region_data(self, region):
        """
        Get local entire data for a region
        """
        endpoint = "/get_entire_region_data"
        params = {"region": region}
        result_table = self.api_client.get(endpoint, params=params)
        return pd.DataFrame(result_table)

    def get_entire_data(self):
        """
        Get global entire data for france so far: Useful for Machine Learning
        Model development for forecasting
        """
        endpoint = "/get_ml_data"
        result_table = self.api_client.get(endpoint)
        return pd.DataFrame(result_table)

    def get_analytics_stats(self, level="department", period="today", top=True):
        """
        Get some analytics stats
        """
        endpoint = "/analytics/stats"
        params = {
            "level": level,
            "period": period,
            "top": top
        }
        return self.api_client.get(endpoint, params=params)

    def get_region_temp_min_max():
        return

    def get_region_shine_min_max():
        return

    def get_dept_temp_min_max():
        return

    def get_dept_shine_min_max():
        return


if __name__ == "__main__":
    queries = WeatherQueries()
