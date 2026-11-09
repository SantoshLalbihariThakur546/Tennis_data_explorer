import requests
from .config import API_KEY, ACCESS_LEVEL, LANGUAGE, TIMEOUT

class APIError(RuntimeError):
    pass

def fetch_feed(feed):
    allowed = {"competitions", "complexes", "double_competitors_rankings"}
    if feed not in allowed:
        raise ValueError("Unsupported Sportradar feed")
    if not API_KEY:
        raise APIError("Set SPORTRADAR_API_KEY in .env or Streamlit secrets.")
    if ACCESS_LEVEL not in {"trial", "production"}:
        raise APIError("SPORTRADAR_ACCESS_LEVEL must be trial or production.")
    url = f"https://api.sportradar.com/tennis/{ACCESS_LEVEL}/v3/{LANGUAGE}/{feed}.json"
    try:
        response = requests.get(url, headers={"x-api-key": API_KEY}, timeout=TIMEOUT)
    except requests.RequestException as exc:
        raise APIError(f"Network error: {exc}") from exc
    if response.status_code == 403:
        raise APIError("403: check API key, access level, and feed entitlement.")
    if response.status_code == 429:
        raise APIError("429: API quota exceeded; wait before retrying.")
    if not response.ok:
        raise APIError(f"HTTP {response.status_code}: {response.text[:250]}")
    try:
        return response.json()
    except ValueError as exc:
        raise APIError("The API response was not valid JSON.") from exc
