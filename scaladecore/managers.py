from uuid import UUID

from .entities import FunctionInstanceEntity, VariableEntity
from .rpc.client_stub import ScaladeWSRpcClient
from .variables import Variable
from .utils import decode_scalade_token

from typing import List


class ContextManager:
    __ws_client = ScaladeWSRpcClient()

    def __init__(self, fi: FunctionInstanceEntity, inputs: List[VariableEntity]):
        self._fi = fi
        self._inputs = inputs

    @classmethod
    def initialize_from_token(cls, token):
        payload = decode_scalade_token(token)
        resp, ok = cls.__ws_client.run_method('retrieve_bi', UUID(payload['fi_uuid']))
        if ok:
            return cls(
                fi=FunctionInstanceEntity.create_from_dict(resp.object['bi_dict']),
                inputs=[VariableEntity.create_from_dict(var_)
                        for var_ in resp.object['inputs_dict']]
            )
        else:
            raise Exception('Unable to initialize properly the ContextManager object.')

    def Block(self):
        resp, ok = self.__ws_client.run_method(
            'change_bi_status', bi_uuid=self._fi.uuid, status_method='block'
        )
        if ok:
            pass
        else:
            raise Exception()

    def Complete(self):
        resp, ok = self.__ws_client.run_method(
            'change_bi_status', bi_uuid=self._fi.uuid, status_method='complete'
        )
        if ok:
            pass
        else:
            raise Exception()

    def Output(self, variable: Variable):
        resp, ok = self.__ws_client.run_method(
            'create_bi_output', bi_uuid=self._fi.uuid, output=variable
        )
        if ok:
            pass
        else:
            raise Exception()
