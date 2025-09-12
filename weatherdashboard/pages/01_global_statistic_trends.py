"""here are all data that will make up for this weather-based studies
The page with the descriptive statistics allows a user
to get the summary statistics of the tables in the database.

"""
import streamlit as st
st.set_page_config(page_title="Weather Dashboard",
                 layout="wide",
                 page_icon="🌦️")

import sys
sys.path.append("/app")

import altair as alt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from weatherdashboard.functions.queries import WeatherQueries
from weatherdashboard.functions.state import WeatherState
from weatherdashboard.functions.constants import WeatherConstants



class DescriptiveStatistic:
    def __init__(self) -> None:
        self.state = WeatherState()
        self.queries = WeatherQueries()


    # temperaure and feels like
    def temperature(self, dep_option):
        """
        Show temperature stats
        """
        #feature_option = st.selectbox("Select a temperature feature", self.constants.temp_feature())
        temp_data = self.state.get_query_result("get_temp_data", dep_option)
        st.dataframe(temp_data)
        temp_data['date'] = pd.to_datetime(temp_data.dates)

        fig = go.Figure()

        # Adding lines for temperature data
        fig.add_trace(go.Scatter(x=temp_data['date'], y=temp_data['temp'], mode='lines+markers', name='Temperature', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=temp_data['date'], y=temp_data['tempmin'], mode='lines+markers', name='Temp Min', line=dict(color='green', dash='dash')))
        fig.add_trace(go.Scatter(x=temp_data['date'], y=temp_data['tempmax'], mode='lines+markers', name='Temp Max', line=dict(color='red', dash='dash')))

        # Adding lines for feels like data
        fig.add_trace(go.Scatter(x=temp_data['date'], y=temp_data['feelslike'], mode='lines+markers', name='Feels Like', line=dict(color='purple')))
        fig.add_trace(go.Scatter(x=temp_data['date'], y=temp_data['feelslikemin'], mode='lines+markers', name='Feels Like Min', line=dict(color='orange', dash='dash')))
        fig.add_trace(go.Scatter(x=temp_data['date'], y=temp_data['feelslikemax'], mode='lines+markers', name='Feels Like Max', line=dict(color='brown', dash='dash')))

        # Update the layout
        fig.update_layout(
            title="Temperature and Feels Like Over Time 🌡",
            xaxis_title="Days",
            yaxis_title="Temperature (°C)",
            template="plotly_dark",  # Optional: to give a dark theme
            showlegend=True
        )
        st.plotly_chart(fig)

    # Precipitation and total
    def wind_gust_pressure_precip_trend(self, pick_dep):
        """
        """

        data = self.state.get_query_result("get_tfptwgp", pick_dep)
        st.write("# 🔍 Data overview")
        st.dataframe(data)
        # ---- graph 1: temp and feelslike ----
        fig_temp = go.Figure()
        fig_temp.add_trace(go.Bar(x=data['dates'], y=data['temp'], name="Temperature", marker_color='gray'))
        fig_temp.add_trace(go.Bar(x=data['dates'], y=data['feelslike'], name="Feels Like", marker_color='purple'))
        fig_temp.update_layout(title=" Temperature and Feels Like  🌡️", barmode='stack', xaxis_title="dates", yaxis_title="°C")
        st.plotly_chart(fig_temp)

        # ---- graph 2 : Precipitation
        fig_precip = go.Figure()
        fig_precip.add_trace(go.Bar(x=data["dates"], y=data["precip"], name="Precipitation", marker_color='green'))
        fig_precip.update_layout(title=" Precipitation   ⛈️", barmode='group', xaxis_title="dates", yaxis_title="mm")
        st.plotly_chart(fig_precip)

        # ---- graph3 : Windspeed, windgust and pressure
        fig_windpressure = go.Figure()
        fig_windpressure.add_trace(go.Bar(x=data["dates"], y=data["windspeed"], name="Wind", marker_color='gold'))
        fig_windpressure.add_trace(go.Bar(x=data["dates"], y=data["windgust"], name="Gust", marker_color='Orange'))
        fig_windpressure.add_trace(go.Scatter(x=data["dates"], y=data["pressure"], name="Pressure", line=dict(color='white', width=2), yaxis="y2"))
        fig_windpressure.update_layout(title="Wind, Gust and Pressure trends  💨", barmode='stack', xaxis_title="dates",
                                       yaxis=dict(title="Wind and Gust (kph)", showgrid=False),
                                       yaxis2=dict(title="Pressure (mbar)", overlaying="y", side="right", showgrid=False)
                                       )
        st.plotly_chart(fig_windpressure)



if __name__ == "__main__":

    st.write("# ⛅Weather Data Visualizations")
    data_visualization = DescriptiveStatistic()
    department = WeatherConstants.department()
    dep_option = st.selectbox("Select a department", department)
    if dep_option:
        data_visualization.temperature(dep_option)
        data_visualization.wind_gust_pressure_precip_trend(dep_option)
