import requests
from django.conf import settings

from integrations.allegro.auth import get_valid_access_token, refresh_access_token


class AllegroClient:
    def __init__(self, account):
        self.account = account

    def get(self, endpoint):
        return self._request("GET", endpoint)

    def post(self, endpoint, data=None):
        return self._request("POST", endpoint, data)

    def patch(self, endpoint, data=None):
        return self._request("PATCH", endpoint, data)

    def _request(self, method, endpoint, data=None):
        url = f'{settings.ALLEGRO_API_URL}{endpoint}'
        token = get_valid_access_token(self.account)

        response = self._send_request(method, url, token, data)

        # retry if no authorization
        if response.status_code == 401:
            refresh_access_token(self.account)

            token = self.account.access_token

            response = self._send_request(method, url, token, data)

        return response

    def _send_request(self, method, url, token, data):
        return requests.request(
            method,
            url,
            headers=self._get_headers(token),
            json=data,
            timeout=10
        )

    def _get_headers(self, token):
        return {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.allegro.public.v1+json",
            "Content-Type": "application/vnd.allegro.public.v1+json",
            "User-Agent": "HandlingTimeApp/1.0",
        }
