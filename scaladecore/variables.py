from datetime import datetime
import pickle
import sys
from tempfile import TemporaryFile
from typing import Any

from .utils import bytes_to_b64str

DEFAULT_CHARSET = 'utf-8'
ISO_8601_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


class Variable:
    TYPES = ('text', 'integer', 'boolean', 'datetime',
             'file')

    def __init__(self,
                 id_name: str,
                 type_: str = None,
                 bytes_: bytes = None,
                 value: Any = None,
                 charset: str = DEFAULT_CHARSET):
        self._id_name = id_name
        self._set_type(type_)
        self._charset = charset
        self._bytes = self.encode(value) if value else bytes_

    @property
    def id_name(self):
        return self._id_name

    @property
    def type(self):
        return self.__type

    @property
    def charset(self):
        return self._charset

    @property
    def bytes(self) -> bytes:
        return self._bytes

    @property
    def value(self):
        """
        Wrapps decoded property
        """
        return self.decoded

    @property
    def decoded(self) -> Any:
        return self._bytes.decode(encoding=self._charset)

    @classmethod
    def create(cls, type_: str, *args, **kwargs):
        """Factory function"""
        if type_ not in cls.TYPES:
            raise Exception(
                f'Invalid variable type: valid ones are {cls.TYPES}')

        class_name = '%sVariable' % type_.capitalize()
        var_type = getattr(sys.modules[__name__], class_name)

        return var_type(*args, **kwargs)

    def encode(self, value: Any) -> bytes:
        return value.encode(encoding=self._charset)

    def get_body(self):
        return bytes_to_b64str(self._bytes)

    def update(self, value):
        self._bytes = self.encode(value)

    def dump(self):
        serialized = pickle.dumps(self)
        return bytes_to_b64str(serialized)

    def _set_type(self, type_=None):
        if not type_:
            self.__type = self.__class__.__name__.split('Variable')[
                0].lower() or None
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
