import streamlit as st
# autres imports
from streamlit_folium import folium_static, st_folium
from functions.queries import WeatherQueries
from views.dash_weather_kpi import fig, kpi
import pandas as pd
from folium import Figure

st.empty()
st.markdown("""
# :material/query_stats: Analytics Stats

Aide KPI pour la synthèse des données météorologiques.
"""
)


horizon_map = {
"Aujourd'hui": "today",
"3 prochains jours": "next3days",
}

level_map = {
    "Département": "department",
    "Région": "region"
}
top_or_bottom_map = {
    "Top": True,
    "Bottom": False
}

cols = st.columns([1, 3])
## container
bottom_left_cell = cols[0].container(
    border=True, height=230
)

right_cell = cols[1].container(
    border=True,
)

with bottom_left_cell:
    # Buttons for picking the geographical level for relevant stats
    level_choice = st.pills(
        "Niveau géographique",
        options=list(level_map.keys()),
        default="Département",
    )
    # Buttons for picking the ranking type
    ranking_choice = st.pills(
        "Type de classement",
        options=list(top_or_bottom_map.keys()),
        default="Top",
    )

    # Buttons for picking time horizon
    horizon = st.pills(
        "Périodes d'étude",
        options=list(horizon_map.keys()),
        default="Aujourd'hui",
    )

top_right_cell = cols[0].container(
    border=True, height=100
)


NUM_COLS = 4
cols = st.columns(NUM_COLS)

def top3(data: pd.DataFrame, metric: str):
    return data[metric].sort_values(ascending=False).head(3)

def bottom3(data: pd.DataFrame, metric: str):
    return data[metric].sort_values(ascending=True).head(3)

choices = [level_choice, horizon, ranking_choice]

if any(c is None for c in choices):
    bottom_left_cell.info("Veuillez sélectionner tous les critères.", icon=":material/info:")
    st.stop()


level = level_map[level_choice]
period = horizon_map[horizon]
top = top_or_bottom_map[ranking_choice]

with right_cell:
    date = st.selectbox(
    "Sélectionnez la date de visualisation",
    WeatherQueries().get_date(),
    key="date_selectbox"
    )
    figs = fig(date=date)
    if level == "region":
        folium_static(figs["m_region_map"], width="stretch")
    else:
        folium_static(figs["m_department_map"], width=1200, height=600)

data = kpi(level=level, period=period, top=top)
delta_label = "⬇️" if not top else "⬆️"
column_0 = data.columns[0]

columns = data.iloc[:, 1:].columns.tolist()


if top:
    st.markdown(f"""#### 🏆 Top 3 {level}s pour {horizon}""")
    st.write(f"Affichage des 3 {level}s avec les meilleures valeurs pour chaque métrique.")
else:
    st.markdown(f"""#### 🔻 Bottom 3 {level}s pour {horizon}""")
    st.write(f"Affichage des 3 {level}s avec les plus basses valeurs pour chaque métrique.")

NUM_COLS = 4
metric_cols = st.columns(NUM_COLS)
for i, col in enumerate(columns):
    with metric_cols[i % NUM_COLS]:
        cell = st.container(border=True)

        with cell:
            if col == "temperature":
                st.subheader("🌡️ Température °C")
            elif col == "humidity":
                st.subheader("💧 Humidité %")
            elif col == "solarenergy":
                st.subheader("🌞 Énergie Solaire kWh/m²")
            elif col == "windspeed":
                st.subheader("💨 Vitesse du Vent km/h")
            elif col == "pressure":
                st.subheader("� Pression atmosphérique mb")
            elif col == "cloudcover":
                st.subheader("☁️ Couverture Nuageuse %")
            elif col == "solarradiation":
                st.subheader("🔆 Radiation Solaire W/m²")

            df_sorted = data[[column_0, col]].sort_values(
                by=col,
                ascending=not top
            ).head(3)

            kcols = st.columns(3)
            for k, row in enumerate(df_sorted.itertuples()):
                kcols[k].metric(
                    label=row[1],       # name / department
                    value=row[2],
                    delta=f"{delta_label} #{k+1}",
                    delta_color="off"
                )
st.markdown(f"---")
st.markdown(f"### Raw Data")
data
