import base64
from datetime import datetime
import jwt
import yaml
import os
import re
from typing import TypeVar

from .config import FunctionConfig

ISO_8601_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
ID_NAME_REGEX = re.compile("^[a-zA-Z-_][a-zA-Z-_0-9]*$")
BASE64_REGEX = re.compile("^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$")

Base64Str = TypeVar('Base64Str')


def parse_dt(date_str):
    return datetime.strptime(date_str, ISO_8601_FORMAT)


def format_dt(dt):
    return dt.strftime(ISO_8601_FORMAT)


def decode_b64str(body: Base64Str) -> bytes:
    return base64.b64decode(body.encode())


def bytes_to_b64str(_bytes: bytes) -> Base64Str:
    return base64.b64encode(_bytes).decode()


def get_foo_function_config() -> FunctionConfig:
    filename = os.path.join(
        os.path.dirname(__file__), 'fixture', 'config', 'function.yml')
    with open(filename, 'r') as file:
        config_data = yaml.safe_load(file)

    inputs_ = config_data.get('inputs', [])
    for rk in range(len(inputs_)):
        ipt = inputs_[rk]
        ipt['__rank__'] = rk

    outputs_ = config_data.get('outputs', [])
    for rk in range(len(outputs_)):
        opt = outputs_[rk]
        opt['__rank__'] = rk

    config = FunctionConfig.deserialize(config_data)
    return config


def encode_scalade_token(payload):
    private_key = os.getenv('SCALADE_PRIVATE_KEY', '').encode()
    return jwt.encode(payload, private_key, algorithm='RS256')


def decode_scalade_token(token: str) -> dict:
    public_key = os.getenv('SCALADE_PUBLIC_KEY', '').encode()
    try:
        decoded_token = jwt.decode(token, public_key, algorithms='RS256')
    except jwt.exceptions.DecodeError:
        raise Exception(f'Error decoding function Token. '
                        'This may be key missmatch or wrong key')
    except jwt.exceptions.ExpiredSignatureError:
        raise Exception(f'The function Token has been expired')
    return decoded_token
