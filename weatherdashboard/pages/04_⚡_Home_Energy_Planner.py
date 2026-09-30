"""
Energy Consumption Advisor
Predicts appliance usage autonomy based on available solar energy
"""
import streamlit as st
st.set_page_config(page_title="Weather Dashboard",
                 layout="wide",
                 page_icon="⚡")

import sys
sys.path.append("/app")

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from functions.queries import WeatherQueries
from functions.state import WeatherState
from functions.constants import WeatherConstants


class EnergyConsumptionAdvisor:
    """Calculate energy consumption autonomy based on solar energy availability"""

    APPLIANCES = {
        "🔦 Lighting": {"power_w": 60, "daily_hours": 5},
        "❄️ Refrigerator": {"power_w": 150, "daily_hours": 24},
        "📺 Television": {"power_w": 100, "daily_hours": 4},
        "💻 Laptop": {"power_w": 65, "daily_hours": 8},
        "🧺 Washing Machine": {"power_w": 2000, "daily_hours": 1.5},
        "🔥 Microwave": {"power_w": 1000, "daily_hours": 0.5},
    }

    def __init__(self):
        self.state = WeatherState()
        self.queries = WeatherQueries()
        self.constants = WeatherConstants()

    def get_appliance_daily_consumption(self, appliance_name):
        """Calculate daily consumption in kWh for an appliance"""
        appliance = self.APPLIANCES[appliance_name]
        return (appliance["power_w"] * appliance["daily_hours"]) / 1000

    def calculate_autonomy(self, available_energy_kwh, selected_appliances):
        """Calculate how many hours the selected appliances can run"""
        results = []
        total_daily_consumption = 0

        for appliance in selected_appliances:
            daily_kwh = self.get_appliance_daily_consumption(appliance)
            total_daily_consumption += daily_kwh

            appliance_config = self.APPLIANCES[appliance]
            autonomy_hours = (available_energy_kwh / daily_kwh) * appliance_config["daily_hours"] if daily_kwh > 0 else 0

            results.append({
                "Appliance": appliance,
                "Daily Consumption (kWh)": round(daily_kwh, 3),
                "Autonomy Hours": round(autonomy_hours, 2),
                "Autonomy Days": round(autonomy_hours / 24, 2) if autonomy_hours > 0 else 0
            })

        return pd.DataFrame(results), round(total_daily_consumption, 3)

    def energy_prediction(self):
        """Main interface for energy consumption prediction"""
        st.markdown("### ⚡ Solar Energy Consumption Advisor")
        st.markdown("Select appliances and discover how long they can run with available solar energy")

        col1, col2 = st.columns([2, 3])

        with col1:
            st.markdown("#### 🌍 Department Selection")
            selected_dept = st.selectbox(
                "Select your department",
                self.constants.department(),
                help="Choose your location to get local solar energy data"
            )

            try:
                energy_data = self.state.get_query_result("get_solarenergy_agg_pday", selected_dept)

                if energy_data and len(energy_data) > 0:
                    available_energy = energy_data[0]['real_production_kwhpday']
                    energy_density = energy_data[0]['solarenergy_kwhpm2']
                    available_capacity = energy_data[0].get('available_solarenergy_kwhc', 0)

                    with st.container(border=True):
                        st.metric("📍 Department", energy_data[0]["department"])
                        st.metric("☀️ Available Energy (kWh/day)", f"{round(available_energy, 2)}")
                        st.metric("💡 Energy Density (kWh/m²)", f"{round(energy_density, 2)}")
                        st.metric("⚡ Peak Capacity (kWh)", f"{round(available_capacity, 2)}")
                else:
                    st.error("No energy data available for this department")
                    return

            except Exception as e:
                st.error(f"Error loading energy data: {e}")
                return

        with col2:
            st.markdown("#### 🏠 Appliances Selection")
            st.markdown("Choose which appliances you want to use")

            selected_appliances = []
            appliance_cols = st.columns(2)

            for idx, (appliance, config) in enumerate(self.APPLIANCES.items()):
                col = appliance_cols[idx % 2]
                daily_kwh = (config["power_w"] * config["daily_hours"]) / 1000
                help_text = f"{config['power_w']}W × {config['daily_hours']}h = {round(daily_kwh, 2)}kWh/day"

                if col.checkbox(appliance, help=help_text):
                    selected_appliances.append(appliance)

        if selected_appliances and available_energy:
            st.markdown("---")
            st.markdown("#### 📊 Autonomy Prediction")

            results_df, total_consumption = self.calculate_autonomy(available_energy, selected_appliances)

            col1, col2 = st.columns([2, 1])
            with col1:
                st.dataframe(results_df, use_container_width=True)

            with col2:
                with st.container(border=True):
                    st.metric("Total Daily Consumption", f"{total_consumption} kWh")

                    if total_consumption > 0:
                        max_days = round(available_energy / total_consumption, 2)
                        status = "✅ Sufficient" if max_days >= 1 else "⚠️ Insufficient"
                        st.metric("Maximum Autonomy", f"{max_days} days", delta=status)

            # Visualization
            fig = px.bar(
                results_df,
                x="Appliance",
                y="Autonomy Days",
                color="Autonomy Days",
                labels={"Autonomy Days": "Days of Autonomy"},
                title="Autonomy Duration by Appliance",
                color_continuous_scale="RdYlGn"
            )
            st.plotly_chart(fig, use_container_width=True)


if __name__ == '__main__':
    advisor = EnergyConsumptionAdvisor()
    advisor.energy_prediction()
