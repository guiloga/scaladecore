import base64
import configparser
from datetime import datetime, timedelta
import jwt
import yaml
import os
from pkg_resources import get_distribution, DistributionNotFound
import re
from typing import TypeVar, Any

from .config import FunctionConfig
from .exceptions import BearerTokenParseError

ISO_8601_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
ID_NAME_REGEX = re.compile("^[a-zA-Z-_][a-zA-Z-_0-9]*$")
BASE64_REGEX = re.compile("^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$")
TOKEN_REGEX = re.compile("[A-Za-z_.+-]*$")

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


def parse_bearer_token(bearer_token):
    match = TOKEN_REGEX.search(bearer_token)
    if not match:
        raise BearerTokenParseError()
    token = match.group(0)
    return token


def encode_scalade_token(payload):
    private_key = os.getenv('SCALADE_PRIVATE_KEY', '').encode()
    return jwt.encode(payload, private_key, algorithm='RS256')


def decode_scalade_token(token: str) -> dict:
    public_key = os.getenv('SCALADE_PUBLIC_KEY', '').encode()
    try:
        decoded_token = jwt.decode(token, public_key, algorithms='RS256')
    except jwt.exceptions.DecodeError:
        raise jwt.exceptions.DecodeError(
            'Error decoding function Token. '
            'This may be key missmatch or wrong key.')
    except jwt.exceptions.ExpiredSignatureError:
        raise jwt.exceptions.ExpiredSignatureError(
            'The function Token has been expired')
    return decoded_token


def generate_token_payload(fi_uuid: str, ttl=7200):
    gen_time = datetime.now()
    exp_time = gen_time + timedelta(hours=ttl / 3600)
    return {
        'fi_uuid': fi_uuid,
        'iat': int(gen_time.timestamp()),
        'exp': int(exp_time.timestamp()),
    }


def _read_pckg_conf():
    def convert_config_to_dict(config: configparser.ConfigParser) -> dict:
        dict_config = {}
        for section in config.sections():
            dict_section = {}
            for key, value in config[section].items():
                dict_section[key] = value
            dict_config[section] = dict_section

        return dict_config

    filepath = os.path.join(os.path.dirname(
        os.path.dirname(__file__)), 'setup.cfg')
    with open(filepath, 'r') as file:
        config = configparser.ConfigParser(allow_no_value=True)
        config.read_string(file.read())

    return convert_config_to_dict(config)


def _get_pckg_config_subset(subset_fields_seq: list) -> Any:
    config = _read_pckg_conf()
    sb_conf = {} | config
    for param in subset_fields_seq:
        sb_conf = sb_conf[param]
    return sb_conf


def get_pckg_dist_version_num() -> str:
    try:
        dist = get_distribution('scaladecore')
        version = dist.version
    except DistributionNotFound:
        version = _get_pckg_config_subset(['metadata', 'version'])
    return version[0]
