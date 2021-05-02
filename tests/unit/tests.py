"""
This module covers all unit tests about domain and
infrastructure layers of guirpc.amqp package.
"""
from datetime import datetime, timedelta
from tempfile import TemporaryFile
from typing import Tuple
from unittest import mock

import pytest

from scaladecore.entities import AccountEntity, BusinessEntity, UserEntity, WorkspaceEntity, \
    FunctionTypeEntity, StreamEntity, FunctionInstanceEntity, VariableEntity, \
    BrickInstanceMessageEntity
from scaladecore.variables import Variable, TextVariable, IntegerVariable, BooleanVariable, \
    DatetimeVariable, FileVariable
from scaladecore.config import VariableConfig, InputConfig, OutputConfig, FunctionConfig, \
    FunctionConfigProvider
from scaladecore.utils import encode_scalade_token, decode_scalade_token
from tests.conftest import generate_token_payload


class TestAccountEntity:
    @pytest.mark.usefixtures('account_obj_d')
    def test_create_from_dict(self, account_obj_d):
        account = AccountEntity.create_from_dict(account_obj_d)
        assert isinstance(account, AccountEntity)

    @pytest.mark.usefixtures('account_obj_d')
    def test_as_dict(self, account_obj_d):
        account = AccountEntity.create_from_dict(account_obj_d)
        assert account.as_dict == account_obj_d


class TestBusinessEntity:
    @pytest.mark.usefixtures('business_obj_d')
    def test_create_from_dict(self, business_obj_d):
        bs = BusinessEntity.create_from_dict(business_obj_d)
        assert isinstance(bs, BusinessEntity)
        assert isinstance(bs._master_account, AccountEntity)

    @pytest.mark.usefixtures('business_obj_d')
    def test_as_dict(self, business_obj_d):
        bs = BusinessEntity.create_from_dict(business_obj_d)
        assert bs.as_dict == business_obj_d


class TestUserEntity:
    @pytest.mark.usefixtures('user_obj_d')
    def test_create_from_dict(self, user_obj_d):
        user = UserEntity.create_from_dict(user_obj_d)
        assert isinstance(user, UserEntity)
        assert isinstance(user._account, AccountEntity)
        assert isinstance(user._business, BusinessEntity)

    @pytest.mark.usefixtures('user_obj_d')
    def test_as_dict(self, user_obj_d):
        user = UserEntity.create_from_dict(user_obj_d)
        assert user.as_dict == user_obj_d


class TestWorkspaceEntity:
    @pytest.mark.usefixtures('workspace_obj_d')
    def test_create_from_dict(self, workspace_obj_d):
        ws = WorkspaceEntity.create_from_dict(workspace_obj_d)
        assert isinstance(ws, WorkspaceEntity)
        assert isinstance(ws._business, BusinessEntity)

    @pytest.mark.usefixtures('workspace_obj_d')
    def test_as_dict(self, workspace_obj_d):
        ws = WorkspaceEntity.create_from_dict(workspace_obj_d)
        assert ws.as_dict == workspace_obj_d


class TestFunctionTypeEntity:
    @pytest.mark.usefixtures('function_type_obj_d')
    def test_create_from_dict(self, function_type_obj_d):
        ft = FunctionTypeEntity.create_from_dict(function_type_obj_d)
        assert isinstance(ft, FunctionTypeEntity)
        assert isinstance(ft.get('account'), AccountEntity)

    @pytest.mark.usefixtures('function_type_obj_d')
    def test_as_dict(self, function_type_obj_d):
        ft = FunctionTypeEntity.create_from_dict(function_type_obj_d)
        assert ft.as_dict == function_type_obj_d


class TestStreamEntity:
    @pytest.mark.usefixtures('stream_obj_d')
    def test_create_from_dict(self, stream_obj_d):
        stream = StreamEntity.create_from_dict(stream_obj_d)
        assert isinstance(stream, StreamEntity)
        assert isinstance(stream.get('account'), AccountEntity)

    @pytest.mark.usefixtures('stream_obj_d')
    def test_as_dict(self, stream_obj_d):
        stream = StreamEntity.create_from_dict(stream_obj_d)
        assert stream.as_dict == stream_obj_d


class TestFunctionInstanceEntity:
    @pytest.mark.usefixtures('function_instance_obj_d')
    def test_create_from_dict(self, function_instance_obj_d):
        fi = FunctionInstanceEntity.create_from_dict(function_instance_obj_d)
        assert isinstance(fi, FunctionInstanceEntity)
        assert isinstance(fi.get('function_type'), FunctionTypeEntity)
        assert isinstance(fi.get('stream'), StreamEntity)

    @pytest.mark.usefixtures('function_instance_obj_d')
    def test_as_dict(self, function_instance_obj_d):
        fi = FunctionInstanceEntity.create_from_dict(function_instance_obj_d)
        assert fi.as_dict == function_instance_obj_d


class TestVariableEntity:
    @pytest.mark.usefixtures('variable_obj_d')
    def test_create_from_dict(self, variable_obj_d):
        variable = VariableEntity.create_from_dict(variable_obj_d)
        assert isinstance(variable, VariableEntity)

    @pytest.mark.usefixtures('variable_obj_d')
    def test_as_dict(self, variable_obj_d):
        variable = VariableEntity.create_from_dict(variable_obj_d)
        assert variable.as_dict == variable_obj_d


class TestBrickInstanceMessage:
    @pytest.mark.usefixtures('brick_instance_message')
    def test_create_from_dict(self, brick_instance_message):
        msg = BrickInstanceMessageEntity.create_from_dict(brick_instance_message)
        assert isinstance(msg, BrickInstanceMessageEntity)

    @pytest.mark.usefixtures('brick_instance_message')
    def test_as_dict(self, brick_instance_message):
        msg = BrickInstanceMessageEntity.create_from_dict(brick_instance_message)
        assert msg.as_dict == brick_instance_message


class TestVariableConfig:
    @pytest.mark.usefixtures('var_cd')
    def test_serialize_deserialize(self, var_cd):
        my_var = VariableConfig.deserialize(var_cd)
        assert isinstance(my_var, VariableConfig)

        var_data = my_var.serialize
        assert var_data == var_cd


class TestFunctionConfig:
    def test_serialize_deserialize(self, function_cd):
        function_config = FunctionConfig.deserialize(function_cd)

        assert isinstance(function_config, FunctionConfig)
        assert function_config.serialize == function_cd


class TestFunctionConfigProvider:
    @pytest.mark.usefixtures('function_cd')
    @mock.patch.object(FunctionConfigProvider, 'read_config')
    def test_get_config(self, read_config, function_cd):
        read_config.return_value = function_cd
        function_config = FunctionConfigProvider.get_config()

        assert isinstance(function_config, FunctionConfig)

        assert len(function_config.inputs) == 2
        for it in function_config.inputs:
            assert isinstance(it, InputConfig)

        assert len(function_config.outputs) == 2
        for ot in function_config.outputs:
            assert isinstance(ot, OutputConfig)


class TestVariable:
    def test_create(self):
        my_var = Variable.create(type_='text',
                                 id_name='my_var',
                                 value='fake_value')
        assert isinstance(my_var, TextVariable)

        my_var = Variable.create(type_='integer',
                                 id_name='my_var',
                                 value=3)
        assert isinstance(my_var, IntegerVariable)

        my_var = Variable.create(type_='boolean',
                                 id_name='my_var',
                                 value=False)
        assert isinstance(my_var, BooleanVariable)

        my_var = Variable.create(type_='datetime',
                                 id_name='my_var',
                                 value=datetime.utcnow())
        assert isinstance(my_var, DatetimeVariable)

        tmp, file_bytes = _create_tmp_file()
        my_var = Variable.create(type_='file',
                                 id_name='my_var',
                                 value=tmp)
        assert isinstance(my_var, FileVariable)

        tmp_file_ = my_var.decoded
        tmp_file_.seek(0)
        assert tmp_file_.read() == file_bytes


class TestTextVariable:
    @pytest.fixture(scope='class')
    def var_data(self):
        return 'my_var', 'foo'

    def test_creation(self, var_data):
        variable = TextVariable(*var_data)

        assert getattr(variable, 'id_name') == 'my_var'
        assert getattr(variable, 'type') == 'text'
        assert getattr(variable, 'value') == 'foo'
        assert isinstance(variable.bytes, bytes)
        assert variable.decoded == 'foo'


class TestIntegerVariable:
    @pytest.fixture(scope='class')
    def var_data(self):
        return 'my_var', 5

    def test_creation(self, var_data):
        variable = IntegerVariable(*var_data)

        assert getattr(variable, 'id_name') == 'my_var'
        assert getattr(variable, 'type') == 'integer'
        assert getattr(variable, 'value') == 5
        assert isinstance(variable.bytes, bytes)
        assert variable.decoded == 5


class TestBooleanVariable:
    @pytest.fixture(scope='class')
    def var_data(self):
        return 'my_var', True

    def test_creation(self, var_data):
        variable = BooleanVariable(*var_data)

        assert getattr(variable, 'id_name') == 'my_var'
        assert getattr(variable, 'type') == 'boolean'
        assert getattr(variable, 'value') is True
        assert isinstance(variable.bytes, bytes)
        assert variable.decoded is True


class TestDatetimeVariable:
    @pytest.fixture(scope='class')
    def var_data(self):
        return 'my_var', datetime.utcnow()

    def test_creation(self, var_data):
        variable = DatetimeVariable(*var_data)

        assert getattr(variable, 'id_name') == 'my_var'
        assert getattr(variable, 'type') == 'datetime'
        assert getattr(variable, 'value') == var_data[1]
        assert isinstance(variable.bytes, bytes)
        assert variable.decoded == var_data[1]


class TestFileVariable:
    @pytest.fixture(scope='class')
    def tmpf(self):
        return _create_tmp_file()

    @pytest.fixture(scope='class')
    def var_data(self, tmpf):
        return 'my_var', tmpf[0]

    def test_creation(self, tmpf, var_data):
        variable = FileVariable(*var_data)

        assert getattr(variable, 'id_name') == 'my_var'
        assert getattr(variable, 'type') == 'file'
        assert getattr(variable, 'value') == var_data[1]
        assert isinstance(variable.bytes, bytes)
        tmp_file = variable.decoded
        tmp_file.seek(0)
        assert tmp_file.read() == tmpf[1]


# TODO: Test Domain


class TestScaladeJWToken:
    @pytest.fixture(scope='class')
    def payload(self, running_functions):
        fi_uuid = running_functions[0]
        return generate_token_payload(fi_uuid)

    @pytest.mark.usefixtures('rsa_keys')
    def test_encode_scalade_token(self, payload):
        token = encode_scalade_token(payload)
        assert token

    @pytest.mark.usefixtures('rsa_keys')
    def test_decode_scalade_token(self, payload):
        token = encode_scalade_token(payload)
        decoded_payload = decode_scalade_token(token)
        assert payload == decoded_payload


def _create_tmp_file() -> Tuple[TemporaryFile, bytes]:
    tmp_file = TemporaryFile()
    file_bytes = 'López Montaña'.encode()
    tmp_file.write(file_bytes)

    return tmp_file, file_bytes
