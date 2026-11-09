import os
from dotenv import load_dotenv
load_dotenv()

def get_setting(name, default=""):
    value = os.getenv(name)
    if value:
        return value
    try:
        import streamlit as st
        return str(st.secrets.get(name, default))
    except Exception:
        return default

API_KEY = get_setting("SPORTRADAR_API_KEY")
ACCESS_LEVEL = get_setting("SPORTRADAR_ACCESS_LEVEL", "trial")
LANGUAGE = get_setting("SPORTRADAR_LANGUAGE", "en")
DATABASE_URL = get_setting("DATABASE_URL", "sqlite:///tennis_analytics.db")
TIMEOUT = int(get_setting("REQUEST_TIMEOUT", "30"))
