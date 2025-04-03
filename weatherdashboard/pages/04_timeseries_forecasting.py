import streamlit as st
st.set_page_config(page_title="Weather Dashboard",
                 layout="wide",
                 page_icon="🔭")
import sys
sys.path.append("/app")
from weatherdashboard.functions.queries import WeatherQueries
from weatherdashboard.functions.state import WeatherState
from weatherdashboard.functions.constants import WeatherConstants


class Forecast:
    def __init__(self):
        self.state = WeatherState()
        self.queries = WeatherQueries()
        self.constants = WeatherConstants()

    @classmethod
    def forecast(cls):
        """
        """
        pass

    def department_data(self, department):
        """
        """
        data = self.state.get_query_result("get_entire_department_data", department)
        st.dataframe(data)
        pass

    def region_data(self, region):
        """
        """
        data = self.state.get_query_result("get_entire_region_data", region)
        st.dataframe(data)
        pass

    def global_data(self):
        """
        """
        data = self.state.get_query_result("get_entire_data")
        st.dataframe(data)
        pass


if __name__ == "__main__":
    st.write("# Weather data to use for training a time series model 🔭")
    dep_options = WeatherConstants().department()
    reg_options =  WeatherConstants().region()
    selected_department = st.selectbox("Select a department", dep_options)
    forecast = Forecast()
    forecast.department_data(selected_department)
    selected_region = st.selectbox("Select a region", reg_options)
    forecast.region_data(selected_region)
    st.markdown("#### Data aggregated for France 🇫🇷")
    forecast.global_data()
    st.markdown("---")
    st.markdown("### Data description")
    st.markdown("---")
    st.markdown("As you can see, the data is not very accurate(not still sufficient to help training time series model), but it is a good start.")
    st.markdown("Our goal today is to forecast the 15 next days relevant variables (i.e Efficiency of Panel)... based on Exogenous variables (i.e Temperature, Wind, Pressure, solarradition, cloudcover, etc...) that surround a photovoltaic panel in real life.")
