from unittest.mock import MagicMock

from scaladecore.exceptions import ContextBlockError, ContextCompleteError, ContextOutputError
from scaladecore.entities import FunctionInstanceEntity, VariableEntity
from scaladecore.managers import ContextManager
from scaladecore.variables import Variable
import pytest

from scaladecore.clients import ScaladeRuntimeAPIClient
from scaladecore.utils import encode_scalade_token, generate_token_payload


class TestScaladeRuntimeAPIClient:
    @pytest.mark.usefixtures('fi_uuid')
    @pytest.fixture(scope='class')
    def api_client(self, fi_uuid):
        token = encode_scalade_token(
            generate_token_payload(fi_uuid))
        api_client = ScaladeRuntimeAPIClient(token)
        return api_client

    def test_retrieve_fi_context(self, api_client):
        _, ok = api_client.retrieve_fi_context()
        assert ok

    def test_create_fi_log_message(self, api_client):
        _, ok = api_client.create_fi_log_message(
            body={"log_message": "Hello, this is a test log message."})
        assert ok

    def test_update_fi_status(self, api_client):
        _, ok = api_client.update_fi_status(
            body={"status_method": "complete"})
        assert ok

    def test_create_fi_output(self, api_client):
        _, ok = api_client.create_fi_output(
            body={"output": "gASV2QAAAAAAAACMFXNjYWxhZGVjb3JlLnZhcmlhYmxlc5SMDFRleHRWYXJpYWJsZZ"
                            "STlCmBlH2UKIwIX2lkX25hbWWUjAVOYW1lc5SMBl92YWx1ZZSMKEd1aWxsZW0gTG9wZ"
                            "XogR2FyY2lhLEFsYmVydCBMb3BleiBHYXJjaWGUjAhfY2hhcnNldJSMBXV0Zi04lIwG"
                            "X2J5dGVzlEMoR3VpbGxlbSBMb3BleiBHYXJjaWEsQWxiZXJ0IExvcGV6IEdhcmNpYZS"
                            "MD19WYXJpYWJsZV9fdHlwZZSMBHRleHSUdWIu"})
        assert ok


class TestContextManager:
    @pytest.mark.usefixtures('rsa_keys')
    @pytest.mark.usefixtures('fi_uuid')
    def test_initialize_from_token(self, fi_uuid):
        ctx = _init_context(fi_uuid)
        assert isinstance(ctx, ContextManager)
        assert isinstance(ctx.fi, FunctionInstanceEntity)
        for ipt in ctx.inputs:
            assert isinstance(ipt, VariableEntity)
        assert isinstance(ctx._ContextManager__client, ScaladeRuntimeAPIClient)

    @pytest.mark.usefixtures('fi_uuid')
    def test_Log(self, fi_uuid):
        ctx = _init_context(fi_uuid)
        ctx.Log('Fake log message')

    @pytest.mark.usefixtures('running_fi')
    def test_Block(self, running_fi):
        ctx = _init_context(running_fi[0])
        ctx.Block()
        assert ctx.fi.get('status') == 'blocked'
        
        with pytest.raises(ContextBlockError):
            ctx.Block()
        assert ContextBlockError().__str__()

    @pytest.mark.usefixtures('running_fi')
    def test_Complete(self, running_fi):
        ctx = _init_context(running_fi[1])
        ctx.Complete()
        assert ctx.fi.get('status') == 'completed'
        
        with pytest.raises(ContextCompleteError):
            ctx.Complete()
        assert ContextCompleteError().__str__()

    @pytest.mark.usefixtures('fi_uuid')
    def test_Output(self, fi_uuid):
        ctx = _init_context(fi_uuid)
        variable = Variable.create('text', 'Names', value='Guillem,Albert')
        ctx.Output(variable)
        assert ctx.outputs
        
        with pytest.raises(ContextOutputError):
            var_ = Variable.create('text', 'Names', value='Guillem,Albert')
            var_.dump = MagicMock(return_value="")
            ctx.Output(var_)
        assert ContextOutputError().__str__()


def _init_context(fi_uuid: str) -> ContextManager:
    payload = generate_token_payload(fi_uuid)
    token = encode_scalade_token(payload)
    return ContextManager.initialize_from_token(token)
