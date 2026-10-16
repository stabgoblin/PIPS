"""Thin wrapper around the PIPS API used by the dashboard views."""

import requests

from settings import API_BASE_URL, REQUEST_TIMEOUT


def get(endpoint, params=None):
    return _request("GET", endpoint, params=params)


def post(endpoint, payload=None):
    return _request("POST", endpoint, json=payload)


def _request(method, endpoint, **kwargs):
    url = f"{API_BASE_URL}{endpoint}"
    try:
        response = requests.request(method, url, timeout=REQUEST_TIMEOUT, **kwargs)
        response.raise_for_status()
        result = response.json()
        if not isinstance(result, dict) or "status" not in result:
            return {"status": "error", "message": "The API returned an unexpected response.", "data": None}
        return result
    except requests.exceptions.ConnectionError:
        return {
            "status": "error",
            "message": (
                f"Could not reach the API at {API_BASE_URL}. "
                "Start it with: uvicorn src.api.main:app --reload"
            ),
            "data": None,
        }
    except requests.exceptions.HTTPError as exc:
        try:
            detail = exc.response.json().get("detail", "Request failed")
            if isinstance(detail, list):
                detail = "; ".join(item.get("msg", "Invalid input") for item in detail)
        except ValueError:
            detail = "The server could not complete this request."
        return {
            "status": "error",
            "message": str(detail),
            "data": None,
        }
    except requests.exceptions.Timeout:
        return {"status": "error", "message": "The request timed out. Please retry.", "data": None}
    except (requests.exceptions.RequestException, ValueError) as exc:
        return {"status": "error", "message": str(exc), "data": None}
