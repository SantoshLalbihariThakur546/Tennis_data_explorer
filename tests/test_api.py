import pytest
from unittest.mock import patch, Mock
from src.tennis_analytics import api

def test_missing_key(monkeypatch):
    monkeypatch.setattr(api, "API_KEY", "")
    with pytest.raises(api.APIError):
        api.fetch_feed("competitions")

def test_reject_unknown_feed():
    with pytest.raises(ValueError):
        api.fetch_feed("unknown")
