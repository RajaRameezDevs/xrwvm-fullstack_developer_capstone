import os
from urllib.parse import quote
import requests
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030"
)
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5000/"
)


def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"
        params = params.rstrip("&")

    base_url = backend_url.rstrip("/")
    path = endpoint.lstrip("/")
    request_url = f"{base_url}/{path}"
    if params:
        request_url = f"{request_url}?{params}"

    print(f"GET from {request_url}")
    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except Exception as err:
        print(f"Network exception occurred in get_request: {err}")
        return None


def analyze_review_sentiments(text):
    base_url = sentiment_analyzer_url.rstrip("/")
    encoded_text = quote(str(text), safe="")
    request_url = f"{base_url}/analyze/{encoded_text}"
    print(f"Analyzing sentiment via {request_url}")
    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except Exception as err:
        print(f"Network exception occurred in analyze_review_sentiments: {err}")
        return {"sentiment": "neutral"}


def post_review(data_dict):
    base_url = backend_url.rstrip("/")
    request_url = f"{base_url}/insert_review"
    print(f"POST to {request_url}")
    try:
        response = requests.post(request_url, json=data_dict)
        response.raise_for_status()
        return response.json()
    except Exception as err:
        print(f"Network exception occurred in post_review: {err}")
        return None