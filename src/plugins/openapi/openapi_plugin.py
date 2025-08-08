import requests

class OpenAPIPlugin:
    def get_openapi_spec(self, url: str) -> str | None:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
            return None
        except requests.exceptions.RequestException:
            return None
