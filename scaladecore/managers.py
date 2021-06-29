from typing import List

from scaladecore.exceptions import ContextBlockError, ContextCompleteError, ContextInitError, ContextLogError, ContextOutputError

from .clients import ScaladeRuntimeAPIClient
from .entities import FunctionInstanceEntity, VariableEntity
from .variables import Variable


class ContextManager:
    def __init__(self,
                 fi: FunctionInstanceEntity,
                 api_client: ScaladeRuntimeAPIClient,
                 inputs: List[VariableEntity],
                 outputs: List[VariableEntity] = None):
        self._fi = fi
        self.__client = api_client
        self._inputs = inputs
        self._outputs = outputs

    @property
    def fi(self):
        return self._fi

    @property
    def inputs(self):
        return self._inputs

    @property
    def outputs(self):
        return self._outputs

    @classmethod
    def initialize_from_token(cls, token):
        api_client = ScaladeRuntimeAPIClient(token)
        resp, ok = api_client.retrieve_fi_context()
        data = resp.json()
        if ok:
            return cls(
                fi=create_function_instance(data['function_instance']),
                api_client=api_client,
                inputs=create_variables(data['inputs']),
                outputs=create_variables(data['outputs']),
            )
        else:
            raise ContextInitError(data)

    def Log(self, message: str):
        resp, ok = self.__client.create_fi_log_message(
            body={"log_message": message})
        data = resp.json()
        if not ok:
            raise ContextLogError(data)

    def Block(self):
        resp, ok = self.__client.update_fi_status(
            body={"status_method": "block"})
        data = resp.json()
        if not ok:
            # todo: raise custom exception
            raise ContextBlockError(data)
        else:
            self._fi = create_function_instance(data['function_instance'])

    def Complete(self):
        resp, ok = self.__client.update_fi_status(
            body={"status_method": "complete"})
        data = resp.json()
        if not ok:
            # todo: raise custom exception
            raise ContextCompleteError(data)
        else:
            self._fi = create_function_instance(data['function_instance'])

    def Output(self, variable: Variable):
        resp, ok = self.__client.create_fi_output(
            body={"output": variable.dump()})
        data = resp.json()
        if not ok:
            # todo: raise custom exception
            raise ContextOutputError(data)
        else:
            self._outputs = create_variables(data['outputs'])


def create_function_instance(function_instance_data: dict) -> FunctionInstanceEntity:
    return FunctionInstanceEntity.create_from_dict(
        function_instance_data)


def create_variables(variables_data: dict) -> List[VariableEntity]:
    return [
        VariableEntity.create_from_dict(var_)
        for var_ in variables_data
    ]
