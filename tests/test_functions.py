import ast
from pathlib import Path

import pytest
import requests

from weatherdashboard.functions.api_client import APIClient
from weatherdashboard.functions.queries import WeatherQueries
from weatherdashboard.functions.state import WeatherState


def test_application_uses_streamlit_script_root_function_imports():
    app_root = Path(__file__).resolve().parents[1] / "weatherdashboard"
    invalid_imports = []

    for source_file in app_root.rglob("*.py"):
        syntax_tree = ast.parse(source_file.read_text(encoding="utf-8"))
        for node in ast.walk(syntax_tree):
            if (
                isinstance(node, ast.ImportFrom)
                and node.module
                and node.module.startswith("weatherdashboard.functions")
            ):
                invalid_imports.append(f"{source_file}:{node.lineno}: {node.module}")

    assert invalid_imports == []


def test_health_check_returns_true_when_api_is_available(mocker):
    response = mocker.Mock()
    mock_get = mocker.patch(
        "weatherdashboard.functions.api_client.requests.get",
        return_value=response,
    )
    client = APIClient("https://api.example.com", "test-key")

    assert client.health_check() is True
    mock_get.assert_called_once_with("https://api.example.com/health")
    response.raise_for_status.assert_called_once_with()


def test_health_check_returns_false_when_api_request_fails(mocker):
    mocker.patch(
        "weatherdashboard.functions.api_client.requests.get",
        side_effect=requests.exceptions.ConnectionError,
    )
    client = APIClient("https://api.example.com", "test-key")

    assert client.health_check() is False


def test_get_sends_api_key_and_query_params(mocker):
    response = mocker.Mock()
    response.json.return_value = [{"temperature": 18}]
    mock_get = mocker.patch(
        "weatherdashboard.functions.api_client.requests.get",
        return_value=response,
    )
    client = APIClient("https://api.example.com", "test-key")

    result = client.get("/weather", params={"department": "Paris"})

    assert result == [{"temperature": 18}]
    mock_get.assert_called_once_with(
        "https://api.example.com/weather",
        params={"department": "Paris"},
        headers={"X-API-Key": "test-key"},
        timeout=10,
    )
    response.raise_for_status.assert_called_once_with()


@pytest.mark.parametrize(
    ("request_error", "message"),
    [
        (requests.exceptions.Timeout, "L'API ne répond pas dans le délai imparti."),
        (requests.exceptions.ConnectionError, "Impossible de joindre l'API."),
    ],
)
def test_get_translates_network_errors(mocker, request_error, message):
    mocker.patch(
        "weatherdashboard.functions.api_client.requests.get",
        side_effect=request_error,
    )
    client = APIClient("https://api.example.com", "test-key")

    with pytest.raises(ConnectionError, match=message):
        client.get("/weather")


def test_get_raises_runtime_error_for_http_error(mocker):
    response = requests.Response()
    response.status_code = 403
    response._content = b"Forbidden"
    mocker.patch(
        "weatherdashboard.functions.api_client.requests.get",
        side_effect=requests.exceptions.HTTPError(response=response),
    )
    client = APIClient("https://api.example.com", "test-key")

    with pytest.raises(RuntimeError, match="403 - Forbidden"):
        client.get("/weather")


def test_get_location_returns_department_from_geolocation(mocker):
    mocker.patch("weatherdashboard.functions.queries.st.write")
    mocker.patch("weatherdashboard.functions.queries.st.warning")
    mocker.patch("weatherdashboard.functions.queries.st.error")
    mock_geolocation = mocker.patch(
        "weatherdashboard.functions.queries.streamlit_js_eval",
        return_value={
            "value": {"latitude": 48.8566, "longitude": 2.3522},
            "dataType": "json",
        },
    )

    reverse_response = mocker.Mock()
    reverse_response.raise_for_status.return_value = None
    reverse_response.json.return_value = {
        "features": [
            {
                "properties": {
                    "context": "75, Paris, Île-de-France",
                }
            }
        ]
    }
    mock_get = mocker.patch(
        "weatherdashboard.functions.queries.requests.get",
        return_value=reverse_response,
    )

    department = WeatherQueries().get_location()

    assert department == "Paris"
    geolocation_expression = mock_geolocation.call_args.kwargs["js_expressions"]
    assert "new Promise" in geolocation_expression
    assert "getCurrentPosition" in geolocation_expression
    assert "(error) => resolve({error: error.message})" in geolocation_expression
    mock_get.assert_called_once_with(
        "https://api-adresse.data.gouv.fr/reverse/",
        params={"lon": 2.3522, "lat": 48.8566},
        timeout=10,
    )


def test_get_location_reports_geolocation_denial_without_reverse_lookup(mocker):
    mock_warning = mocker.patch("weatherdashboard.functions.queries.st.warning")
    mocker.patch(
        "weatherdashboard.functions.queries.streamlit_js_eval",
        return_value={
            "value": {"error": "User denied Geolocation"},
            "dataType": "json",
        },
    )
    mock_get = mocker.patch("weatherdashboard.functions.queries.requests.get")

    assert WeatherQueries().get_location() is None

    mock_warning.assert_called_once_with(
        "Can't get your location: User denied Geolocation. "
        "Please allow location access to continue."
    )
    mock_get.assert_not_called()


def test_reverse_geocode_extracts_department_not_city():
    payload = {
        "features": [
            {
                "properties": {
                    "context": "69003, Lyon 3e Arrondissement, Rhône, "
                    "Auvergne-Rhône-Alpes",
                }
            }
        ]
    }

    assert WeatherQueries._extract_department_from_reverse_geocode(payload) == "Rhône"


def test_location_department_becomes_selectbox_default(mocker):
    session_state = {}
    mocker.patch("weatherdashboard.functions.state.st.session_state", session_state)
    state = WeatherState()

    state.apply_location_default(
        "Rhône",
        ["Ain", "Rhône", "Paris"],
        "weather_statistics_department",
    )

    assert session_state["weather_statistics_department"] == "Rhône"


def test_location_default_does_not_override_user_department(mocker):
    session_state = {"home_energy_department": "Paris"}
    mocker.patch("weatherdashboard.functions.state.st.session_state", session_state)
    state = WeatherState()

    state.apply_location_default(
        "Rhône",
        ["Ain", "Rhône", "Paris"],
        "home_energy_department",
    )

    assert session_state["home_energy_department"] == "Paris"
