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

_GEOLOCATION_JS_EXPRESSION = """new Promise((resolve) => {
    if (!navigator.geolocation) {
        resolve({error: "Geolocation is not supported by this browser"});
        return;
    }
    navigator.geolocation.getCurrentPosition(
        (position) => resolve({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
        }),
        (error) => resolve({error: error.message}),
        {enableHighAccuracy: true, timeout: 10000, maximumAge: 60000}
    );
})"""


class WeatherQueries:
    # Reference panel area and efficiency used by the API for solar energy production estimates
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

    @staticmethod
    def _extract_department_from_reverse_geocode(payload):
        """Return department from the reverse geocoding payload when available."""
        if not payload or not payload.get("features"):
            return None

        properties = payload["features"][0].get("properties", {})
        departments = {
            department.casefold(): department
            for department in WeatherConstants.department()
        }

        department_name = properties.get("department")
        if isinstance(department_name, str):
            match = departments.get(department_name.strip().casefold())
            if match:
                return match

        context = properties.get("context")
        if context:
            parts = [part.strip() for part in context.split(",") if part and part.strip()]
            for part in parts:
                match = departments.get(part.casefold())
                if match:
                    return match

        return None

    def get_location(self):
        """
        Automatically Get User Location
        """
        try:
            user_location = streamlit_js_eval(
                js_expressions=_GEOLOCATION_JS_EXPRESSION,
                key="geo_position",
            )

            if not user_location:
                st.warning(
                    "Can't get your location. Please accept geolocation to continue."
                )
                return None

            if not isinstance(user_location, dict):
                st.warning("The browser returned an invalid location.")
                return None

            user_location = user_location.get("value", user_location)
            if not isinstance(user_location, dict):
                st.warning("The browser returned an invalid location.")
                return None

            if user_location.get("error"):
                st.warning(
                    f"Can't get your location: {user_location['error']}. "
                    "Please allow location access to continue."
                )
                return None

            coords = user_location.get("coords", user_location)
            if not isinstance(coords, dict):
                st.warning("The browser returned invalid coordinates.")
                return None

            latitude = coords.get("latitude")
            longitude = coords.get("longitude")

            if latitude is None or longitude is None:
                st.warning(
                    "Can't get your location. Please accept geolocation to continue."
                )
                return None

            url = "https://api-adresse.data.gouv.fr/reverse/"
            response = requests.get(
                url,
                params={"lon": longitude, "lat": latitude},
                timeout=10,
            )
            response.raise_for_status()
            payload = response.json()

            department = self._extract_department_from_reverse_geocode(payload)
            if department:
                st.write(f"📍 You are currently in **{department}** department")
                return department

            st.error("Can't get department.")
            return None

        except requests.exceptions.RequestException as exc:
            st.error(f"Error when retrieving location : {exc}")
            return None

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
