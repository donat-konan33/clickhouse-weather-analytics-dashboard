# Weather & Solar Energy Dashboard

[![Streamlit](https://img.shields.io/badge/Streamlit-1.40.0-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-supported-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)

A Streamlit application for exploring weather and solar-energy data across French departments and regions. The dashboard consumes data from a separate REST API connected to the ClickHouse data warehouse; it does not connect directly to ClickHouse.

[![Dashboard preview](assets/images/dashboard_ui_screenshot.png)](https://donat-konan33.github.io/assets/videos/demo.mp4)

The screenshot links to a short application demo.

## What the dashboard provides

| Section | Current capabilities |
| --- | --- |
| Weather statistics | Department-level temperature, feels-like, precipitation, wind, gust and pressure trends. |
| Weather analytics | Department or region views, today or the next three days, top or bottom rankings, geographic maps and KPI summaries. |
| Solar energy | Department and region maps, date-based solar-energy indicators, seven-day distribution charts and aggregated data. |
| Home energy planner | Estimates appliance energy use and autonomy from the selected department's solar data, adjusted to the entered panel area and efficiency. |
| Forecasting | Navigation page is present, but advanced forecasting models are marked as coming soon and are not currently implemented in the dashboard. |

### Home energy planner reference assumptions

The planner's API reference calculation uses a total panel area of **2.7 m²** and a module efficiency of **21.7%**:

```text
estimated daily production = average solar energy (kWh/m²/day)
                             × panel area (m²)
                             × module efficiency
```

The efficiency reference comes from the Trina Solar **Vertex TSM-DE19R** datasheet, which specifies a maximum module efficiency of 21.7% (for the 585 W version). The **2.7 m²** area is the fixed reference area used by the API calculation; it is an assumption, not a user-specific installation measurement. In the planner, users can change both the total panel area and module efficiency, and the production estimate is scaled from those reference values.

Source: [Trina Solar Vertex TSM-DE19R datasheet (French, 2023)](https://static.trinasolar.com/sites/default/files/Datasheet_Vertex_DE19R_FR_2023%20C_web.pdf).

## Previous README and this update

| Previous README | Updated README |
| --- | --- |
| Described the dashboard broadly, without a clear breakdown of its pages. | Documents each available dashboard section and its current scope. |
| Presented an AI assistant and 15-day predictions as part of the experience. | No hosted LLM integration is required. This keeps the dashboard independent of usage-based AI charges; advanced forecasting remains planned rather than implemented. |
| Referred to environment variables and an `.env.example` file, although the app reads API settings from Streamlit secrets. | Gives the configuration format used by the application and identifies the API-key header. |
| Mentioned the backend without clearly separating it from this frontend repository. | Explains the Streamlit-to-REST-API-to-ClickHouse architecture and the backend prerequisite. |

This is a documentation comparison with the previous README, not a claim that each capability was newly introduced in a particular software release.

## Architecture

```text
Streamlit dashboard
	|
	| HTTPS/HTTP requests with X-API-Key
	v
REST API (separate backend project)
	|
	v
ClickHouse data warehouse
```

The data pipeline and API are maintained separately in the [ETLT Airbyte, MinIO, ClickHouse, dbt and Airflow project](https://github.com/donat-konan33/EtltAirbyteMinioClickhouseDbtAirflow). Start that backend and make its API reachable before using the dashboard.

## Requirements

- Python 3.12 for local development, or Docker with Docker Compose.
- Access to the REST API used by the dashboard.
- An API key accepted by that backend.

## Run locally

Clone the repository and enter its directory:

```bash
git clone https://github.com/donat-konan33/clickhouse-weather-analytics-dashboard.git
cd clickhouse-weather-analytics-dashboard
```

Create `.streamlit/secrets.toml` using the structure below. Replace the placeholders with the API base URL and API key supplied by your backend operator; do not commit real credentials.

```toml
[api]
BASE_URL = "https://your-api.example.com"
API_KEY = "your-api-key"
```

Install dependencies and start Streamlit:

```bash
poetry install
poetry run streamlit run "weatherdashboard/00_🏠_Home.py"
```

Open the local URL printed by Streamlit, normally `http://localhost:8501`.

## Run with Docker Compose

Create `.streamlit/secrets.toml` as shown above, then build and start the dashboard:

```bash
docker compose up --build -d
```

The dashboard is exposed on port `8501`. To stop it:

```bash
docker compose down
```

## Configuration

| Setting | Location | Purpose |
| --- | --- | --- |
| `api.BASE_URL` | `.streamlit/secrets.toml` | Base URL of the REST API. |
| `api.API_KEY` | `.streamlit/secrets.toml` | Key sent in the `X-API-Key` request header. |

The application performs a health check against the API when it starts. Keep credentials out of source control; `.streamlit/secrets.toml` is excluded by `.gitignore`.

The dashboard does not require an LLM provider or an AI-provider API key. AI-generated recommendations are not part of the current application, avoiding additional usage-based service costs.

## Project structure

```text
weatherdashboard/
├── 00_🏠_Home.py             # Dashboard landing page and API health check
├── functions/
│   ├── api_client.py         # REST API client
│   ├── constants.py          # Department, region and feature lists
│   ├── queries.py            # API-backed data access
│   └── state.py              # Session-state data caching
├── pages/                    # Weather, analytics, solar, energy and forecast pages
└── views/                    # Shared map and KPI visualizations
tests/                         # Automated tests
```

## Tests

Run the unit and mocked-backend integration tests locally with:

```bash
poetry run pytest -q
```

The integration test starts a local fake REST API and checks the solar-energy request, authentication header and response shape without requiring API credentials or a network connection to the production backend.

## CI/CD and Streamlit Community Cloud

GitHub Actions runs unit tests and the mocked-backend integration test for pull requests targeting `master`, pushes to `master`, and manual runs. No production API secrets are needed in GitHub Actions.

Yes, Streamlit Community Cloud deploys directly from GitHub: connect the app to this repository and choose its deployment branch, for example `master`. New commits on that branch trigger Streamlit Cloud to update the app; this workflow does not itself deploy to Streamlit Cloud. To make CI pass before deployment, protect the selected deployment branch in GitHub by requiring pull requests and the **CI / Tests** status check before merging. Avoid direct pushes that bypass branch protection.
