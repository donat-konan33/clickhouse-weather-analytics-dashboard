import altair as alt
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from timeit import default_timer as timer


conn_string = URL.create(**st.secrets["postgres"])
conn = create_engine(conn_string, echo=False)
TABLES = [

]


@st.cache_data
def load_data(table_name):
    """
    """
    data = pd.read_sql_query()

    return data


def create_main_page():
    """
    """
    st.title("Weather Dashboard")
    st.info(
        """
    Delete me once completed
    """
    )
    selected_table = ""

    st.subheader("Welcome to the Weather Dashboard")
    st.sidebar.title("Info")
    st.sidebar.markdown("This page shows the current weather of your department")  # track your position
    selected_table = st.sidebar.selectbox("Select a table", TABLES, key="table")

    return selected_table


def summary_statistics(data):
    """
    Creates a subheader and writes the summary statistics for the data
    """
    st.subheader("Summary statistics")
    st.info("Use the describe method to get the summary statistics")

    st.write(data.describe())



def session_state(data):
    """
    """

    # Initialization of session state, assign a random value
    # to the session state

    if "data" not in st.session_state:
        st.session_state["data"] = "value"

    # Update the session state using the dataframe

    st.session_state["data"] = data


if __name__ == "__main__":
    selected_table = create_main_page()

    # used to time the loading of the data
    start = timer()
    data = load_data(selected_table)
    end = timer()
    st.sidebar.info(f"{round(end-start,4)} seconds to load the data")

    st.dataframe(data)

    summary_statistics(data)
    session_state(data)
