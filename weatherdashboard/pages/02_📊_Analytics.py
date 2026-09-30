import streamlit as st
from streamlit_folium import folium_static
from functions.queries import WeatherQueries
from views.dash_weather_kpi import fig, kpi
import pandas as pd

st.set_page_config(page_title="Weather Analytics", layout="wide", page_icon="📊")

st.markdown("""
<style>
.analytics-title {
    font-size: 40px;
    font-weight: bold;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
</style>
<p class="analytics-title">📊 Weather Analytics Dashboard</p>
""", unsafe_allow_html=True)

st.markdown("Analyze weather patterns and key metrics across French departments and regions")

horizon_map = {
    "Today": "today",
    "Next 3 Days": "next3days",
}

level_map = {
    "Department": "department",
    "Region": "region"
}
top_or_bottom_map = {
    "Top": True,
    "Bottom": False
}

st.markdown("---")
st.markdown("### 🎯 Configure Your Analysis")

cols = st.columns([1, 3])

with cols[0]:
    config_container = st.container(border=True)
    with config_container:
        st.markdown("**Geographic Level**")
        level_choice = st.pills(
            "Select geographic level",
            options=list(level_map.keys()),
            default="Department",
            label_visibility="collapsed"
        )

        st.markdown("**Ranking Type**")
        ranking_choice = st.pills(
            "Ranking type",
            options=list(top_or_bottom_map.keys()),
            default="Top",
            label_visibility="collapsed"
        )

        st.markdown("**Time Period**")
        horizon = st.pills(
            "Time period",
            options=list(horizon_map.keys()),
            default="Today",
            label_visibility="collapsed"
        )

with cols[1]:
    map_container = st.container(border=True)


choices = [level_choice, horizon, ranking_choice]

if any(c is None for c in choices):
    st.info("📋 Please select all filter options to display analytics", icon="ℹ️")
    st.stop()

level = level_map[level_choice]
period = horizon_map[horizon]
top = top_or_bottom_map[ranking_choice]

with map_container:
    st.markdown("**🗺️ Geographic Distribution**")
    date = st.selectbox(
        "Select visualization date",
        WeatherQueries().get_date(),
        key="date_selectbox",
        label_visibility="collapsed"
    )
    figs = fig(date=date)
    if level == "region":
        folium_static(figs["m_region_map"], width="stretch")
    else:
        folium_static(figs["m_department_map"], width=1200, height=600)

data = kpi(level=level, period=period, top=top)
column_0 = data.columns[0]

columns = data.iloc[:, 1:].columns.tolist()

st.markdown("---")

if top:
    st.markdown(f"""### 🏆 Top 3 {level.capitalize()}s - {horizon}""")
    st.markdown(f"<span style='color: #27ae60; font-weight: bold;'>✅ Showing the 3 **best-performing** {level.lower()}s</span>", unsafe_allow_html=True)
    arrow_icon = "📈"
    delta_color = "normal"
else:
    st.markdown(f"""### 🔻 Bottom 3 {level.capitalize()}s - {horizon}""")
    st.markdown(f"<span style='color: #e74c3c; font-weight: bold;'>⚠️ Showing the 3 **lowest-performing** {level.lower()}s</span>", unsafe_allow_html=True)
    arrow_icon = "📉"
    delta_color = "inverse"

NUM_COLS = 4
metric_cols = st.columns(NUM_COLS)

for i, col in enumerate(columns):
    with metric_cols[i % NUM_COLS]:
        cell = st.container(border=True)

        with cell:
            if col == "temperature":
                st.subheader("🌡️ Temperature (°C)")
            elif col == "humidity":
                st.subheader("💧 Humidity (%)")
            elif col == "solarenergy":
                st.subheader("🌞 Solar Energy (kWh/m²)")
            elif col == "windspeed":
                st.subheader("💨 Wind Speed (km/h)")
            elif col == "pressure":
                st.subheader("🎚️ Pressure (mb)")
            elif col == "cloudcover":
                st.subheader("☁️ Cloud Cover (%)")
            elif col == "solarradiation":
                st.subheader("🔆 Solar Radiation (W/m²)")

            df_sorted = data[[column_0, col]].sort_values(
                by=col,
                ascending=not top
            ).head(3)

            kcols = st.columns(3)
            rank_medals = ["🥇", "🥈", "🥉"]
            for k, row in enumerate(df_sorted.itertuples()):
                delta_text = f"{arrow_icon} {rank_medals[k]}"
                kcols[k].metric(
                    label=row[1],
                    value=f"{row[2]:.1f}",
                    delta=delta_text,
                    delta_color=delta_color
                )

st.markdown("---")
st.markdown("### 📋 Full Dataset")
st.dataframe(data, use_container_width=True)
