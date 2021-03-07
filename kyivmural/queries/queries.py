from flask import current_app
from urllib.parse import urlparse
from aws_requests_auth.boto_utils import BotoAWSRequestsAuth
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


def get_murals():
    return _get_from_kyivmural_api("murals")


def get_mural(mural_id, artist_name):
    return _get_from_kyivmural_api(f"murals/{mural_id}/{artist_name}")


def get_artists():
    return _get_from_kyivmural_api("artists")


def get_artist(artist_id):
    return _get_from_kyivmural_api(f"artists/{artist_id}")


def _requests_retry_session(
        retries=5,
        backoff_factor=2,
        status_forcelist=(500, 502, 503, 504),
        session=None
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods={"GET"}
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    return session


def _get_from_kyivmural_api(resource):
    region = current_app.config["AWS_REGION"]
    api_url = f"{current_app.config['KYIVMURAL_API_ENDPOINT']}/{resource}"
    api_host = urlparse(api_url).netloc

    auth = BotoAWSRequestsAuth(
        aws_host=api_host,
        aws_region=region,
        aws_service="execute-api"
    )

    requests_session = _requests_retry_session()

    response = requests_session.get(api_url, auth=auth)
    response.raise_for_status()
    if response.text:
        return response.json()
    return {}
