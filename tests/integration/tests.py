import pytest

from scaladecore.utils import encode_scalade_token, generate_token_payload
from scaladecore.managers import ContextManager
from scaladecore.clients import ScaladeRuntimeAPIClient

class TestScaladeWSRpcClient:
    def test_run_method(self):
        pass


class TestContextManager:
    @pytest.mark.usefixtures('rsa_keys')
    def test_initialize_from_token(self, running_functions):
        assert len(running_functions) >= 3
        for fi_uuid in running_functions:
            cm = self._init_context(fi_uuid)
            assert isinstance(cm, ContextManager)
    """
    def test_Block(self, running_functions):
        fi_uuid = running_functions[0]
        cm = self._init_context(fi_uuid)
        assert cm.Block()

    def test_Complete(self, running_functions):
        fi_uuid = running_functions[1]
        cm = self._init_context(fi_uuid)
        assert cm.Complete()

    def test_Output(self, running_functions):
        fi_uuid = running_functions[2]
        cm = self._init_context(fi_uuid)
        # assert cm.Output()
    """
    @staticmethod
    def _init_context(fi_uuid: str) -> ContextManager:
        payload = generate_token_payload(fi_uuid)
        token = encode_scalade_token(payload)
        return ContextManager.initialize_from_token(token)


class TestScaladeRuntimeAPIClient:
    @pytest.fixture(scope='class')
    def api_client(self):
        client = ScaladeRuntimeAPIClient()

    def test_retrieve_fi_context(self, api_client):
        # response = api_client.retrieve_fi_context()
        assert False # response.status_code == 200
    
    def test_create_fi_log_message(self, api_client):
        # response = api_client.create_fi_log_message(body={})
        assert False # response.status_code == 200

    def test_update_fi_status(self, api_client):
        # response = api_client.update_fi_status(body={})
        assert False # response.status_code == 200

    def test_create_fi_output(self, api_client):
        # response = api_client.create_fi_output(body={})
        assert False ##  response == 200
