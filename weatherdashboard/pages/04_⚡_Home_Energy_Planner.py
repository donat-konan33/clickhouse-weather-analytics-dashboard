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
from functions.energy import calculate_required_panel_count


class EnergyConsumptionAdvisor:
    """Calculate energy consumption autonomy based on solar energy availability"""

    APPLIANCES = {
        "💡 LED Bulb (5 W)": {"power_w": 5, "daily_hours": 5},
        "❄️ Refrigerator": {"power_w": 150, "daily_hours": 24},
        "📺 Television": {"power_w": 100, "daily_hours": 4},
        "💻 Laptop": {"power_w": 65, "daily_hours": 8},
        "🧺 Washing Machine": {"power_w": 2000, "daily_hours": 1.5},
        "🔥 Microwave": {"power_w": 1000, "daily_hours": 0.5},
        "🍽️ Dishwasher": {"power_w": 1800, "daily_hours": 1.5},
        "🌬️ Cooker Hood": {"power_w": 100, "daily_hours": 2},
        "♨️ Air-to-water Heat Pump": {"power_w": 1500, "daily_hours": 8},
    }

    def __init__(self):
        self.state = WeatherState()
        self.queries = WeatherQueries()
        self.constants = WeatherConstants()

    def get_appliance_daily_consumption(self, appliance_name):
        """Calculate daily consumption in kWh for an appliance"""
        appliance = self.APPLIANCES[appliance_name]
        return (appliance["power_w"] * appliance["daily_hours"]) / 1000

    def scale_energy_for_panel_area(self, reference_energy_kwh, panel_area_m2):
        """Adjust API estimates that use the reference panel area."""
        return (
            reference_energy_kwh
            * panel_area_m2
            / self.queries.REFERENCE_PANEL_AREA_M2
        )

    def scale_energy_for_panel_configuration(
        self,
        reference_energy_kwh,
        panel_area_m2,
        panel_efficiency_percent,
    ):
        """Adjust API production estimates to the entered area and efficiency."""
        return (
            self.scale_energy_for_panel_area(reference_energy_kwh, panel_area_m2)
            * panel_efficiency_percent
            / self.queries.REFERENCE_PANEL_EFFICIENCY_PERCENT
        )

    def calculate_autonomy(self, available_energy_kwh, selected_appliances):
        """Calculate how many hours the selected appliances can run"""
        results = []
        total_daily_consumption = 0

        for appliance, quantity in selected_appliances.items():
            daily_kwh = self.get_appliance_daily_consumption(appliance) * quantity
            total_daily_consumption += daily_kwh

            appliance_config = self.APPLIANCES[appliance]
            autonomy_hours = (available_energy_kwh / daily_kwh) * appliance_config["daily_hours"] if daily_kwh > 0 else 0

            results.append({
                "Appliance": appliance,
                "Quantity": quantity,
                "Daily Consumption (kWh)": round(daily_kwh, 3),
                "Autonomy Hours": round(autonomy_hours, 2),
                "Autonomy Days": round(autonomy_hours / 24, 2) if autonomy_hours > 0 else 0
            })

        return pd.DataFrame(results), round(total_daily_consumption, 3)

    def energy_prediction(self):
        """Main interface for energy consumption prediction"""
        st.markdown("### ⚡ Solar Energy Consumption Advisor")
        st.markdown("Select appliances and discover how long they can run with available solar energy")

        departments = self.constants.department()
        self.state.apply_location_default(
            self.queries.get_location(),
            departments,
            "home_energy_department",
        )

        st.markdown("#### ⚙️ Solar panel configuration")
        with st.container(border=True):
            config_cols = st.columns([2, 1, 1, 1])
            with config_cols[0]:
                selected_dept = st.selectbox(
                    "Department",
                    departments,
                    key="home_energy_department",
                    help="Choose your location to get local solar energy data",
                )
            with config_cols[1]:
                panel_count = st.number_input(
                    "Number of panels",
                    min_value=1,
                    max_value=500,
                    value=1,
                    step=1,
                    help="Choose how many panels to include in this estimate.",
                )
            with config_cols[2]:
                panel_area_m2 = st.number_input(
                    "Area per panel (m²)",
                    min_value=0.1,
                    max_value=10.0,
                    value=self.queries.REFERENCE_PANEL_AREA_M2,
                    step=0.1,
                    help="The API reference module has a surface area of 2.7 m².",
                )
            with config_cols[3]:
                panel_efficiency_percent = st.number_input(
                    "Module efficiency (%)",
                    min_value=1.0,
                    max_value=100.0,
                    value=self.queries.REFERENCE_PANEL_EFFICIENCY_PERCENT,
                    step=0.1,
                    help=(
                        "The Trina Vertex TSM-DE19R module has a maximum efficiency "
                        "of 21.7% (2023 datasheet). Adjust this value to match your module."
                    ),
                )
            total_panel_area_m2 = panel_count * panel_area_m2
            st.caption(
                "The cited Trina datasheet lists a maximum efficiency of 21.7% "
                "for the TSM-DE19R module. The API reference uses 2.7 m² and 21.7% "
                f"per module. Your configuration: {panel_count} panel(s), "
                f"{total_panel_area_m2:.1f} m² total surface."
            )

        try:
            energy_data = self.state.get_query_result(
                "get_solarenergy_agg_pday",
                selected_dept,
            )

            if energy_data and len(energy_data) > 0:
                reference_energy = energy_data[0]["real_production_kwhpday"]
                available_energy = self.scale_energy_for_panel_configuration(
                    reference_energy,
                    total_panel_area_m2,
                    panel_efficiency_percent,
                )
                daily_production_per_panel = self.scale_energy_for_panel_configuration(
                    reference_energy,
                    panel_area_m2,
                    panel_efficiency_percent,
                )
                energy_density = energy_data[0]["solarenergy_kwhpm2"]
                reference_capacity = energy_data[0].get(
                    "available_solarenergy_kwhc",
                    0,
                )
                available_capacity = self.scale_energy_for_panel_area(
                    reference_capacity,
                    total_panel_area_m2,
                )

                st.markdown("#### ☀️ Estimated solar production")
                with st.container(border=True):
                    st.markdown(f"**📍 {energy_data[0]['department']}**")
                    metric_cols = st.columns(3)
                    metric_cols[0].metric(
                        "Daily production",
                        f"{available_energy:.2f} kWh",
                    )
                    metric_cols[1].metric(
                        "Solar energy density",
                        f"{energy_density:.2f} kWh/m²",
                    )
                    metric_cols[2].metric(
                        "Peak capacity",
                        f"{available_capacity:.2f} kWh",
                    )
            else:
                st.error("No energy data available for this department")
                return

        except Exception as e:
            st.error(f"Error loading energy data: {e}")
            return

        st.markdown("#### 🏠 Appliances")
        st.caption("Select the appliances in your household and set the quantity for each.")
        selected_appliances = {}
        appliance_cols = st.columns(3)

        for idx, (appliance, config) in enumerate(self.APPLIANCES.items()):
            col = appliance_cols[idx % 3]
            daily_kwh = (config["power_w"] * config["daily_hours"]) / 1000
            help_text = (
                f"{config['power_w']} W × {config['daily_hours']} h "
                f"= {daily_kwh:.2f} kWh/day per appliance"
            )
            with col.container(border=True):
                is_selected = st.checkbox(
                    appliance,
                    help=help_text,
                    key=f"home_energy_appliance_{idx}",
                )
                if is_selected:
                    selected_appliances[appliance] = st.number_input(
                        "Quantity",
                        min_value=1,
                        max_value=100,
                        value=1,
                        step=1,
                        key=f"home_energy_quantity_{idx}",
                    )

        if selected_appliances:
            st.markdown("---")
            st.markdown("#### 📊 Daily energy balance")

            results_df, total_consumption = self.calculate_autonomy(available_energy, selected_appliances)

            balance_cols = st.columns(3)
            balance_cols[0].metric(
                "Selected appliances consumption",
                f"{total_consumption:.2f} kWh/day",
            )
            balance_cols[1].metric(
                "Estimated production",
                f"{available_energy:.2f} kWh/day",
            )
            if total_consumption > 0:
                max_days = round(available_energy / total_consumption, 2)
                balance_cols[2].metric(
                    "Daily coverage",
                    f"{max_days * 100:.0f}%",
                    delta="Sufficient" if max_days >= 1 else "Insufficient",
                )

            st.dataframe(results_df, use_container_width=True, hide_index=True)

            if total_consumption > available_energy:
                required_panel_count = calculate_required_panel_count(
                    total_consumption,
                    daily_production_per_panel,
                )
                if required_panel_count is None:
                    st.warning(
                        "No daily solar production is available for this location, "
                        "so a panel recommendation cannot be calculated."
                    )
                else:
                    additional_panels = max(0, required_panel_count - panel_count)
                    st.warning(
                        f"Daily production is insufficient. At least "
                        f"{required_panel_count} panels are estimated to cover "
                        f"{total_consumption:.2f} kWh/day "
                        f"({additional_panels} additional panel(s) from your current selection)."
                    )

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
