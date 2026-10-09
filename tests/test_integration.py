import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from urllib.parse import parse_qs, urlparse

import pytest

from weatherdashboard.functions.api_client import APIClient


@pytest.fixture
def mock_solar_api():
    received_requests = []

    class MockSolarAPIHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed_url = urlparse(self.path)
            received_requests.append(
                {
                    "path": parsed_url.path,
                    "query": parse_qs(parsed_url.query),
                    "api_key": self.headers.get("X-API-Key"),
                }
            )

            if parsed_url.path != "/get_solarenergy_agg_pday":
                self.send_error(404)
                return

            response = [
                {
                    "department": "Paris",
                    "solarenergy_kwhpm2": 3.0,
                    "available_solarenergy_kwhc": 8.1,
                    "real_production_kwhpday": 1.7577,
                }
            ]
            body = json.dumps(response).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), MockSolarAPIHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        yield f"http://127.0.0.1:{server.server_port}", received_requests
    finally:
        server.shutdown()
        thread.join()
        server.server_close()


def test_solar_energy_query_works_with_mock_backend(mock_solar_api):
    base_url, received_requests = mock_solar_api
    client = APIClient(base_url=base_url, api_key="integration-test-key")

    result = client.get(
        "/get_solarenergy_agg_pday",
        params={"department": "Paris"},
    )

    assert result[0]["department"] == "Paris"
    assert result[0]["solarenergy_kwhpm2"] == 3.0
    assert result[0]["available_solarenergy_kwhc"] == 8.1
    assert result[0]["real_production_kwhpday"] == 1.7577
    assert received_requests == [
        {
            "path": "/get_solarenergy_agg_pday",
            "query": {"department": ["Paris"]},
            "api_key": "integration-test-key",
        }
    ]
