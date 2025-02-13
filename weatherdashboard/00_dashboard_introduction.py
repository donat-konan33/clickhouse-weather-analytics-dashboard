import streamlit as st
st.set_page_config(page_title="Weather Dashboard",
                 layout="wide",
                 page_icon="🌦️")
import sys
sys.path.append("/app")
from weatherdashboard.functions.queries import WeatherQueries
from weatherdashboard.functions.state import WeatherState
from weatherdashboard.functions.constants import WeatherConstants
import numpy as np


class WeatherDashboard:
    def __init__(self) -> None:
        self.state = WeatherState()
        self.department = WeatherQueries().get_location()
        self.constants = WeatherConstants().department()

        if self.department:
            st.write(f"You are in {self.department}")
        else:
            st.warning("No location found")

    def get_data(self, department):
        """
        """
        data = self.state.get_query_result("get_temp_data", 'mart_newdata', department)
        info_dict = dict(
            weekdayname=data["weekday_name"].loc[0],
            descriptions=data["descriptions"].loc[0],
            temperature=data["temp"].loc[0],
            feelslike=data["feelslike"].loc[0],
            tempmin=data["tempmin"].loc[0],
            tempmax=data["tempmax"].loc[0],
            department=data["department"].loc[0],

        )
        return info_dict

    def display_info(self, info_dict):
        """
        """
        st.write(f"# {info_dict['temperature']} °C")
        st.write(f"## {info_dict['weekdayname']} · Today  ")
        st.write(f"{info_dict['department']}")
        container = st.container(border=True)
        text =  f"""
                    <div style="text-align: center;">
                        <p>T (max/min) : {info_dict['tempmax']}°/ {info_dict['tempmin']}°</p>
                        <p>Feels like : {info_dict['feelslike']}°</p>
                        <p>{info_dict['descriptions']}</p>
                    </div>
                """
        container.write(text, unsafe_allow_html=True)


    def introduction_page(self):
        """Layout the views of the dashboard"""

        st.markdown("""
        <style>
        .big-font {
            font-size:100px !important;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown('<p class="big-font"> 🌦️ Weather Dashboard </p>', unsafe_allow_html=True)
        col1, col2 = st.columns([4.7, 2.3])
        with col1:
            with st.container(border=True):
                st.markdown(
                """
                This dashboard application will allow you to overview weather behavior througout the seven next days from present to the seven one. \n
                -------------------

                You can get a bit of description of what we intend to show you as service. \n
                -------------------

                On ``global statistic trends`` page, you could visualize :

                👉 An overwiew of data retrieved and saved into our bigquery database \n
                👉 Chart makes Temperature, feels like  throught the week (the seven next days), ... up \n


                On ``solar trends page`` , you could see charts like :

                👉 Map of Metropolitan France showing solar energy (sunchine in kWh/m²) for each department\n
                👉 Trends according distributions by date and by region


                On ``ai suggestions`` page, you will hit/select your department name : \n
                👉 Our AI could give you more quick informations about solar trends which could give you a lot of ideas.

                Time series forecast is being built and will comes soon ⏰.

                """
                )

        with col2 :
            place = np.random.choice(self.constants)
            try:
                if self.department:
                    info_dict = self.get_data(self.department)
                    with col2:
                        with st.container(border=True):
                            self.display_info(info_dict)
                elif place:
                    info_dict = self.get_data(place)
                    with col2:
                        with st.container(border=True):
                            self.display_info(info_dict)
                else:
                    info_dict = self.get_data("Paris")
                    with col2:
                        with st.container(border=True):
                            self.display_info(info_dict)

            except Exception as e:
                st.write(f"""⚠️ ``Something was wrong !! Can't display the day weather info !``\n
                         {e}""")


if __name__ == "__main__":
    dashboard = WeatherDashboard()
    dashboard.introduction_page()
