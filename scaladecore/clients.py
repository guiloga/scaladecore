import requests
import os

from .utils import decode_scalade_token, get_pckg_config_subset


class ScaladeRuntimeAPIClient:
    """
    Scalade runtime API namespace HTTP client.
    """
    API_NAMESPACE = '/api/{version}/runtime/'
    BASE_HEADERS = {
        'Authentication': 'Bearer {token}',
        'Content-Type': 'application/json'
    }

    def __init__(self, token: str = None):
        self._base_url = self.API_NAMESPACE.format(
            version=get_pckg_config_subset(['metadata', 'version']))
        self._set_token_payload(token)

        self.new_http_session()

    def _set_token_payload(token: str):
        if not token:
            self._token = os.getenv('FI_TOKEN')
        else:
            self._token = token

        self._payload = decode_scalade_token(self._token)
    
    def new_http_session(self):
        self._session = requests.Session()
        self._session.headers |= self.BASE_HEADERS['Authentication'].format(
            self._token)

    def retrieve_fi_context(self):
        resp = self._session.get(self._base_url + 'retrieve-fi-context')
        return resp
    
    def create_fi_log_message(self, body: dict):
        resp = self._session.post(self._base_url + 'create-fi-log',
                                  json=body)
        return resp

    def update_fi_status(self, body: dict):
        resp = self._session.patch(self._base_url + 'update-fi-status',
                                   json=body)
        return resp

    def create_fi_output(self, body: dict):
        resp = self._session.post(self._base_url + 'create-fi-output',
                                  json=body)
        return resp
