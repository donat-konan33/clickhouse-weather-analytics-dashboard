import streamlit as st


class WeatherDashboard:
    def __init__(self) -> None:
        pass

    def introduction_page(self):
        """Layout the views of the dashboard"""
        st.set_page_config(layout="wide")
        st.markdown("""
        <style>
        .big-font {
            font-size:100px !important;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown('<p class="big-font">Weather Dashboard </p>', unsafe_allow_html=True)
        st.markdown(
        """
        This dashboard application will allow you to overview weather behavior througout the seven next days from present to the seven one.
        -------------------

        You can get a bit of description of what we intend to show you as service.
        -------------------

        On visualizations page, you could see:

        - A map of France Metropolitan visualizing the values of wind, solar radiation (sunshine), rain, ...
        - A line chart with the points of data for next seven days including the current one.

        """
        )


if __name__ == "__main__":
    dashboard = WeatherDashboard()
    dashboard.introduction_page()
