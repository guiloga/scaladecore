import base64
from datetime import datetime
import sys
from tempfile import TemporaryFile
from typing import Any

from .utils import bytes_to_b64str

DEFAULT_CHARSET = 'utf-8'
ISO_8601_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


class Variable:
    TYPES = ('text', 'integer', 'boolean', 'datetime',
             'file')

    def __init__(self, id_name: str, value: Any, charset: str = DEFAULT_CHARSET,
                 type_: str = None):
        self._id_name = id_name
        self._value = value
        self._charset = charset

        self._bytes = self.encode(value)
        self._set_type(type_)

    @property
    def id_name(self):
        return self._id_name

    @property
    def type(self):
        return self.__type

    @property
    def value(self):
        return self._value

    @property
    def charset(self):
        return self._charset

    @property
    def bytes(self) -> bytes:
        return self._bytes

    @property
    def decoded(self) -> Any:
        return self._bytes.decode(encoding=self._charset)

    @classmethod
    def create(cls, type_: str, id_name: str, value: Any, **kwargs):
        """Factory function"""
        if type_ not in cls.TYPES:
            raise Exception(f'Invalid variable type: valid ones are {cls.TYPES}')
        class_name = '%sVariable' % type_.capitalize()
        var_type = getattr(sys.modules[__name__], class_name)
        kwargs['type_'] = type_
        return var_type(id_name, value, **kwargs)

    def encode(self, value: Any) -> bytes:
        return value.encode(encoding=self._charset)

    def get_body(self):
        return bytes_to_b64str(self._bytes)

    def update(self, value):
        self._bytes = self.encode(value)

    def _set_type(self, type_=None):
        if not type_:
            self.__type = self.__class__.__name__.split('Variable')[0].lower() or None
        else:
            self.__type = type_


class TextVariable(Variable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class IntegerVariable(Variable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def decoded(self) -> int:
        number_str = super().decoded
        return int(number_str)

    def encode(self, value: int) -> bytes:
        number_str = str(value)
        return super().encode(number_str)


class BooleanVariable(Variable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def decoded(self) -> bool:
        bool_str = super().decoded
        return bool(bool_str)

    def encode(self, value: bool) -> bytes:
        bool_str = str(value)
        return super().encode(bool_str)


class DatetimeVariable(Variable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def decoded(self) -> datetime:
        dt_str = super().decoded
        return parse_dt(dt_str)

    def encode(self, value: datetime) -> bytes:
        dt_str = format_dt(value)
        return super().encode(dt_str)


class FileVariable(Variable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def decoded(self) -> TemporaryFile:
        tmp = TemporaryFile()
        tmp.write(self._bytes)
        return tmp

    def encode(self, value: TemporaryFile) -> bytes:
        value.seek(0)
        file_bytes = value.read()
        return file_bytes


def format_dt(dt, format_=ISO_8601_FORMAT):
    return dt.strftime(format_)


def parse_dt(date_str, format_=ISO_8601_FORMAT):
    return datetime.strptime(date_str, format_)
