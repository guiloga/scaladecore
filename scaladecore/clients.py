import os
from requests import Session
from requests.models import Response
from requests.structures import CaseInsensitiveDict
from typing import Tuple

from .utils import get_pckg_config_subset


class ScaladeRuntimeAPIClient:
    """
    Scalade runtime API namespace HTTP client.
    """
    API_NAMESPACE = '/api/{version}/runtime/'
    BASE_HEADERS = {
        'Authorization': 'Bearer {token}',
        'Content-Type': 'application/json'
    }

    def __init__(self, token: str = None):
        self._set_base_api_url()
        self._token = token

        self.new_http_session()

    def _set_base_api_url(self):
        use_ssl = os.getenv('SCALADE_API_SERVER_USE_SSL', 'False')
        self._base_api_url = "{protocol}://{hostname}:{port}{relative_url}".format(
            protocol='https' if use_ssl == 'True' else 'http',
            hostname=os.getenv(
                'SCALADE_API_SERVER_HOST', 'localhost'),
            port=os.getenv(
                'SCALADE_API_SERVER_PORT', '8000'),
            relative_url=self.API_NAMESPACE.format(
                version="v%s" % get_pckg_config_subset(['metadata', 'version'])[0])
        )

    def _eval_response(self, resp: Response) -> Tuple[Response, bool]:
        if resp.status_code == 200:
            return resp, True
        else:
            return resp, False

    def new_http_session(self):
        headers = dict()
        headers |= self.BASE_HEADERS
        headers['Authorization'] = headers['Authorization'].format(
            token=self._token)

        self._session = Session()
        default_headers = dict(self._session.headers)
        headers |= default_headers
        self._session.headers = CaseInsensitiveDict(headers)

    def retrieve_fi_context(self):
        return self._eval_response(
            self._session.get(self._base_api_url + 'retrieve-fi-context/'))

    def create_fi_log_message(self, body: dict):
        return self._eval_response(
            self._session.post(self._base_api_url + 'create-fi-log-message/', json=body))

    def update_fi_status(self, body: dict):
        return self._eval_response(
            self._session.patch(self._base_api_url + 'update-fi-status/', json=body))

    def create_fi_output(self, body: dict):
        return self._eval_response(
            self._session.post(self._base_api_url + 'create-fi-output/', json=body))
