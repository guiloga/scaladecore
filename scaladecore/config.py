from abc import ABC, abstractmethod
from typing import List
import json
import os
import yaml


class ConfigSerializer(ABC):
    @classmethod
    @abstractmethod
    def deserialize(cls, config_data: dict): pass

    @property
    @abstractmethod
    def serialize(self) -> dict: pass

    @property
    def as_json(self) -> str:
        return json.dumps(self.serialize)


class VariableConfig(ConfigSerializer):
    def __init__(self, id_name: str, type_: str, verbose_name: str, rank: int):
        self.id_name = id_name
        self.type = type_
        self.verbose_name = verbose_name
        self.rank = rank

    @classmethod
    def deserialize(cls, config_data: dict):
        v_name = config_data.get('verbose_name')
        if not v_name:
            v_name = config_data.get('id_name').replace('_', ' ').capitalize()

        return cls(
            id_name=config_data['id_name'],
            type_=config_data['type'],
            verbose_name=v_name,
            rank=config_data['__rank__'], )

    @property
    def serialize(self) -> dict:
        return dict(
            id_name=self.id_name,
            type=self.type,
            verbose_name=self.verbose_name,
            __rank__=self.rank, )


class InputConfig(VariableConfig):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # TODO: Extend with more options


class OutputConfig(VariableConfig):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # TODO: Extend with more options


class FunctionConfig:
    def __init__(self, key: str, verbose_name: str, description: str,
                 inputs: List[InputConfig] = None, outputs: List[OutputConfig] = None):
        self.key = key
        self.verbose_name = verbose_name
        self.description = description
        self.inputs = inputs
        self.outputs = outputs

    @classmethod
    def deserialize(cls, config_data: dict):
        inputs = config_data.get('inputs')
        outputs = config_data.get('outputs')

        return cls(
            key=config_data['key'],
            verbose_name=config_data['verbose_name'],
            description=config_data['description'],
            inputs=[InputConfig.deserialize(item) for item in inputs] if inputs else None,
            outputs=[OutputConfig.deserialize(item) for item in outputs] if outputs else None)

    @property
    def serialize(self) -> dict:
        return dict(
            key=self.key,
            verbose_name=self.verbose_name,
            description=self.description,
            inputs=[it.serialize for it in self.inputs],
            outputs=[ot.serialize for ot in self.outputs], )

    @property
    def inputs_as_json(self):
        return json.dumps([it.serialize for it in self.inputs]) if self.inputs else None

    @property
    def outputs_as_json(self):
        return json.dumps([ot.serialize for ot in self.outputs]) if self.outputs else None


class PositionConfig(ConfigSerializer):
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    @classmethod
    def deserialize(cls, config_data: dict):
        return cls(
            row=config_data['row'],
            col=config_data['col'], )

    @property
    def serialize(self) -> dict:
        return dict(
            row=self.row,
            col=self.col, )


class FunctionConfigProvider:
    @classmethod
    def get_config(cls):
        config_data = cls.read_config()
        config = FunctionConfig.deserialize(config_data)

        return config

    @staticmethod
    def read_config():
        filepath = os.path.join(os.getcwd(), 'config', 'function.yml')
        with open(filepath, 'r') as file:
            config_data = yaml.safe_load(file.read())

        return config_data
