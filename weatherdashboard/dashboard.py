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

        st.markdown('<p class="big-font"> 🌦️ Weather Dashboard </p>', unsafe_allow_html=True)
        col1, col2 = st.columns([5, 2])
        with col1:
            with st.container(border=True):
                st.markdown(
                """
                This dashboard application will allow you to overview weather behavior througout the seven next days from present to the seven one. \n
                -------------------

                You can get a bit of description of what we intend to show you as service. \n
                -------------------

                On visualizations page, you could see:

                👉 A map of France Metropolitan visualizing the values of wind, solar radiation (sunshine), rain, ...\n
                👉 A line chart with the points of data for next seven days including the current one.

                """
                )

        exemple_temp = 7
        place = "Essonne"

        with col2:
            with st.container(border=True):
                st.write(f"# Today   {exemple_temp} °C")
                st.write(f"{place}")
                container = st.container(border=True)
                container.write("This is inside the container")


if __name__ == "__main__":
    dashboard = WeatherDashboard()
    dashboard.introduction_page()
