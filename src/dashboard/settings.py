"""Dashboard runtime settings."""

import os

API_BASE_URL = os.getenv("PIPS_API_URL", "http://127.0.0.1:8000").rstrip("/")
REQUEST_TIMEOUT = 45
