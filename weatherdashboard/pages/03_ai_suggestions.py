"""
With this page it will be interesting to request ai suggestions about the weather

"""
import streamlit as st
#st.set_page_config(layout="wide")
import sys
sys.path.append("/app")

import os
import openai as ai
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from pandasai.llm.local_llm import LocalLLM
from pandasai import SmartDataframe

from weatherdashboard.functions.database import WeatherDataWarehouse
from weatherdashboard.functions.queries import WeatherQueries
from weatherdashboard.functions.state import WeatherState
from weatherdashboard.functions.constants import WeatherConstants

ai.api_key = os.environ["OPENAI_API_KEY"]

# ---------  add login credentials -------- #


class AiPrompt:
    def __init__(self):
        self.state = WeatherState()
        self.queries = WeatherQueries()
        self.constants = WeatherConstants()
        self.client = ai.OpenAI(api_key=ai.api_key, project='weather-2025')

    def household_use(self):
        """
        This method helps to define, with your location that you will give and other necessary features,
        which machine could consume the location corresponding to weekly solar energy recorded in the database
        """
        col1, col2 = st.columns([2, 5])
        with col1:
            pick_dep = st.selectbox("Select a department... ", self.constants.department())
            data = self.state.get_query_result("get_tfptwgp", pick_dep)
        with col2:
            prompt = st.text_input("Hit the features of your Solar panel")
            # --- llm call
            model = LocalLLM(
                        api_base="http://host.docker.internal:11434/v1",
                        model="llama3"
                    )
            if data:
                df=SmartDataframe(data,config={"llm":model})
                if st.button("Generate"):
                    if prompt:
                        with st.spinner("Generating response..."):
                            st.write(df.chat(prompt))
        st.dataframe(data)


if __name__ == '__main__':
    suggestions = AiPrompt()
    suggestions.household_use()
