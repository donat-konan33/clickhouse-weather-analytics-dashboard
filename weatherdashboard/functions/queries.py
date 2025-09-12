import streamlit as st
import pandas as pd
import requests
from streamlit_js_eval import streamlit_js_eval
from weatherdashboard.functions.constants import WeatherConstants
import os

API_HOST = os.environ.get("API_HOST")
BASE_URL = f"http://{API_HOST}:8005" # eventually local for test

class WeatherQueries:
    def __init__(self) -> None:
        self.datasets = WeatherConstants.dataset()

    def get_data(self) -> pd.DataFrame:
        """
        Get a table from the mart dataset
        """
        endpoint = "/get_data"
        result_table = requests.get(BASE_URL + endpoint).json()
        return pd.DataFrame(result_table)

    def get_temp_data(self, department) -> pd.DataFrame:
        """
        Get temperature data like temp, fileslikemin, fileslikemax and feelslike
        """
        endpoint = "/get_temp_data"
        params = {"department": department}
        result_table = requests.get(BASE_URL + endpoint, params=params).json()
        return pd.DataFrame(result_table)


    def get_solarenergy_geo_data_data(self, date) -> pd.DataFrame:
        """
        Get Solar energy data for all studied location by date
        """
        endpoint = "/solar_geo_data"
        params = {"date": date}
        result_table = requests.get(BASE_URL + endpoint, params=params).json()
        return pd.DataFrame(result_table)


    def get_date(self):
        """
        To get studied date window
        """
        endpoint = "/date"
        return requests.get(BASE_URL + endpoint).json()


    def get_tfptwgp(self, department):
        """
        Get some interesting features like tfptwgp as :
        Temperature, Feels like, Pecipitation, Wind, Gust and Pressure
        """
        endpoint = "/common_features"
        params = {"department" : department}
        result_table = requests.get(BASE_URL + endpoint, params=params).json()
        return pd.DataFrame(result_table)

    def get_sunshine_data(self):
        """
        Get some interesting features like tfptwgp as :
        Temperature, Feels like, Pecipitation, Wind, Gust and Pressure
        """
        endpoint = "/get_sunshine_data"
        result_table = requests.get(BASE_URL + endpoint).json()
        return pd.DataFrame(result_table)

    def get_region_sunshine_data(self, region):
        """
        Get region solar features
        """
        endpoint = "/get_region_sunshine_data"
        params = {"region": region}
        result_table = requests.get(BASE_URL + endpoint, params=params)
        return pd.DataFrame(result_table)

    def get_solarenergy_agg_pday(self, department):
        """
        We take into account the calculation over 8 days as recorded
        Panel area = 2.7 m²
        Panel efficiency = 21.7%
        """
        endpoint = "/get_solarenergy_agg_pday"
        params = {"department": department}
        return requests.get(BASE_URL + endpoint, params=params).json()

    def get_location(self):
        """
        Automatically Get User LOcation
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


    def get_entire_department_data(self, department) -> pd.DataFrame:
        """Get local entire data for a department"""
        endpoint = "/get_entire_department_data"
        params = {"department": department}
        result_table = requests.get(BASE_URL + endpoint, params=params)
        return pd.DataFrame(result_table)


    def get_entire_region_data(self, region):
        """
        Get local entire data for a region
        """
        endpoint = "/get_entire_region_data"
        params = {"region": region}
        result_table = requests.get(BASE_URL + endpoint, params=params)
        return pd.DataFrame(result_table)

    def get_entire_data(self):
        """
        Get global entire data for france so far: Useful for Machine Learning
        Model development for forecasting
        """
        endpoint = "/get_ml_data"
        result_table = requests.get(BASE_URL + endpoint)
        return pd.DataFrame(result_table)


if __name__ == "__main__":
    queries = WeatherQueries()
