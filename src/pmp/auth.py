import requests

from src.pmp.constants import (
    PMP_API_URL,
    PMP_CLIENT_ID,
    PMP_CLIENT_SECRET,
    PMP_REFRESH_TOKEN,
)


def request_access_token() -> str:
    res = requests.post(
        f"https://accounts.zoho.eu/oauth/v2/token",
        params={
            "client_id": PMP_CLIENT_ID,
            "client_secret": PMP_CLIENT_SECRET,
            "refresh_token": PMP_REFRESH_TOKEN,
            "grant_type": "refresh_token",
        },
    )

    j = res.json()

    return j["access_token"]
