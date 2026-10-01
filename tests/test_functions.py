import pytest
import requests

from weatherdashboard.functions.api_client import APIClient


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
