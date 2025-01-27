import streamlit as st


class WeatherDashboard:
    def __init__(self) -> None:
        pass

    def introduction_page(self):
        """Layout the views of the dashboard"""
        st.title("Weather Dashboard")
        st.write(
            """
        describe
        ---
        the
        ---
        Visualization
        """
        )


if __name__ == "__main__":
    dashboard = WeatherDashboard()
    dashboard.introduction_page()
