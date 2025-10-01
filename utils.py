import configparser
import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import json
import os

AUTH_URL = "https://acleddata.com/oauth/token"
API_BASE = "https://acleddata.com/api/acled/read"

class ACLEDTokenManager:
    def __init__(self, username: str, password: str, cache_file: str = "acled_tokens.json"):
        self.username = username
        self.password = password
        self.cache_file = cache_file
        self.access_token = None
        self.refresh_token = None
        self.expires_at = None  # epoch seconds

        # Try loading tokens from cache
        self._load_cache()

    def _load_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r") as f:
                    data = json.load(f)
                self.access_token = data.get("access_token")
                self.refresh_token = data.get("refresh_token")
                self.expires_at = data.get("expires_at")
            except Exception:
                # Ignore cache errors; will re-auth
                pass

    def _save_cache(self):
        data = {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_at": self.expires_at,
        }
        try:
            with open(self.cache_file, "w") as f:
                json.dump(data, f)
        except Exception:
            # Non-fatal if cache cannot be written
            pass

    def _request_token(self):
        """Password grant: get new access + refresh token."""
        resp = requests.post(
            AUTH_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "username": self.username,
                "password": self.password,
                "grant_type": "password",
                "client_id": "acled",
            },
            timeout=30,
        )
        self._handle_auth_response(resp)

    def _refresh_token(self):
        """Refresh grant: use refresh_token to get new tokens."""
        if not self.refresh_token:
            # If no refresh token, fallback to password grant.
            self._request_token()
            return
        resp = requests.post(
            AUTH_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "refresh_token": self.refresh_token,
                "grant_type": "refresh_token",
                "client_id": "acled",
            },
            timeout=30,
        )
        # If refresh fails (e.g. invalid refresh token), attempt password grant
        if resp.status_code != 200:
            self._request_token()
        else:
            self._handle_auth_response(resp)

    def _handle_auth_response(self, resp: requests.Response):
        try:
            resp.raise_for_status()
        except requests.HTTPError:
            raise RuntimeError(f"Auth error {resp.status_code}. Body: {resp.text[:500]}")

        try:
            payload = resp.json()
        except ValueError:
            raise RuntimeError(f"Auth response not JSON. Body: {resp.text[:500]}")

        # Expected fields: token_type, expires_in, access_token, refresh_token
        if "access_token" not in payload:
            raise RuntimeError(f"Unexpected auth payload: keys={list(payload.keys())}")

        self.access_token = payload["access_token"]
        self.refresh_token = payload.get("refresh_token")
        expires_in = payload.get("expires_in", 0)  # seconds
        # Set expiry slightly earlier to account for clock skew
        self.expires_at = int(time.time()) + max(0, int(expires_in) - 30)
        self._save_cache()

    def get_token(self) -> str:
        """Return a valid access token, refreshing/re-authing if needed."""
        now = int(time.time())
        if not self.access_token or not self.expires_at or now >= self.expires_at:
            # Try refresh first if we have a refresh token; otherwise password grant
            self._refresh_token() if self.refresh_token else self._request_token()
        return self.access_token

    def authorize_headers(self) -> dict:
        token = self.get_token()
        return {"Authorization": f"Bearer {token}"}


def fetch_acled_data():
    # Read configuration
    config = configparser.ConfigParser()
    if not config.read('config.txt'):
        raise FileNotFoundError("Could not read config.txt. Ensure it's in the working directory.")

    username = config.get('API', 'username').strip()
    password = config.get('API', 'password').strip()
    country = config.get('API', 'country').strip()
    start_date = config.get('API', 'start_date').strip()
    limit = int(config.get('API', 'limit', fallback='20000'))
    offset = int(config.get('API', 'offset', fallback='0'))

    # Dates
    end_date = datetime.now().strftime('%Y-%m-%d')
    event_date = f"{start_date}|{end_date}"

    token_mgr = ACLEDTokenManager(username=username, password=password)

    all_rows = []
    while True:
        headers = token_mgr.authorize_headers()
        params = {
            "country": country,
            "event_date": event_date,
            "event_date_where": "BETWEEN",
            "limit": limit,
            "offset": offset,
        }

        resp = requests.get(API_BASE, headers=headers, params=params, timeout=60)
        # If unauthorized, attempt to refresh and retry once
        if resp.status_code == 401:
            token_mgr._refresh_token()
            headers = token_mgr.authorize_headers()
            resp = requests.get(API_BASE, headers=headers, params=params, timeout=60)

        print(f"Request URL: {resp.url}")
        print(f"Status: {resp.status_code}")

        try:
            resp.raise_for_status()
        except requests.HTTPError:
            raise RuntimeError(f"HTTP error {resp.status_code}. Body: {resp.text[:500]}")

        # Parse JSON
        try:
            payload = resp.json()
        except ValueError:
            raise RuntimeError(f"Response is not JSON. Body: {resp.text[:500]}")

        # Handle error-shaped payloads gracefully
        if isinstance(payload, dict) and "error" in payload and "data" not in payload:
            raise RuntimeError(f"API error: {payload.get('error')}")

        # Extract rows
        rows = None
        if isinstance(payload, dict):
            if "data" in payload and isinstance(payload["data"], list):
                rows = payload["data"]
            elif "results" in payload and isinstance(payload["results"], list):
                rows = payload["results"]
            elif "items" in payload and isinstance(payload["items"], list):
                rows = payload["items"]

        if rows is None:
            raise RuntimeError(f"Unexpected payload shape. Keys: {list(payload.keys())}")

        all_rows.extend(rows)

        # Stop if fewer than limit returned (no more pages)
        count = len(rows)
        print(f"Fetched {count} rows at offset {offset}")
        if count < limit or count == 0:
            break

        # Advance offset
        offset += limit

    return pd.DataFrame(all_rows)


if __name__ == "__main__":
    df = fetch_acled_data()
    print(df.head())
    print(f"Total rows: {len(df)}")
