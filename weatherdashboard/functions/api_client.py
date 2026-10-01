# services/api_client.py

import requests


class APIClient:

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def health_check(self):
        try:
            response = requests.get(
                f"{self.base_url}/health",
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException:
            return False

    def get(self, endpoint: str, params: dict | None = None):
        try:
            response = requests.get(
                f"{self.base_url}{endpoint}",
                params=params,
                headers={"X-API-Key": self.api_key},
                timeout=10,
            )
            print("URL finale :", response.request.url)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout:
            raise ConnectionError("L'API ne répond pas dans le délai imparti.")

        except requests.exceptions.ConnectionError:
            raise ConnectionError("Impossible de joindre l'API.")

        except requests.exceptions.HTTPError as e:
            detail = e.response.text
            raise RuntimeError(
                f"Erreur HTTP de l'API : {e.response.status_code} - {detail}"
            )
