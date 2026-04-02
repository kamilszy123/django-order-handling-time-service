from datetime import timedelta
from django.utils import timezone
from django.conf import settings
import requests

from integrations.allegro.exceptions import AllegroAuthError


def exchange_code_for_token(account, code):
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.ALLEGRO_REDIRECT_URI
    }

    token_data = _post_token(data)
    _save_tokens(account, token_data)


def get_valid_access_token(account):
    if account.is_token_expired():
        refresh_access_token(account)

    if not account.access_token:
        raise Exception("Missing access token")

    return account.access_token


def refresh_access_token(account):
    if not account.refresh_token:
        raise Exception("Missing refresh token")

    data = {
        "grant_type": "refresh_token",
        "refresh_token": account.refresh_token
    }

    token_data = _post_token(data)
    _save_tokens(account, token_data)


def _post_token(data):
    response = requests.post(
        settings.ALLEGRO_TOKEN_URL,
        data=data,
        headers=_get_headers(),
        auth=_get_auth(),
        timeout=10
    )
    if response.status_code != 200:
        raise AllegroAuthError(
            f"Allegro auth error: {response.text}",
            status_code=response.status_code
        )
    return response.json()


def _save_tokens(account, token_data):
    account.access_token = token_data["access_token"]
    account.refresh_token = token_data["refresh_token"]
    account.expires_at = timezone.now() + timedelta(seconds=token_data["expires_in"])
    account.save()


def _get_headers():
    return {
        "Accept": "application/json",
        "User-Agent": "TimeControlApp/1.0",
    }


def _get_auth():
    return (settings.ALLEGRO_CLIENT_ID, settings.ALLEGRO_CLIENT_SECRET)


