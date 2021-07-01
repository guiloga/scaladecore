from abc import ABC, abstractmethod
from datetime import datetime
import sys
from typing import List
from uuid import UUID, uuid4

from .config import InputConfig, OutputConfig, PositionConfig
from .exceptions import EntityFactoryError
from .utils import parse_dt, format_dt, decode_b64str, bytes_to_b64str
from .variables import Variable


class EntityContract(ABC):
    def __init__(self, uuid: UUID = None, created: datetime = None):
        self.__uuid = uuid or uuid4()
        self._created = created or datetime.utcnow()

    @property
    def uuid(self):
        return self.__uuid

    def get(self, attr_name: str):
        return getattr(self, '_' + attr_name)

    @classmethod
    @abstractmethod
    def create_from_dict(cls, obj_d: dict):
        pass

    @classmethod
    def create_entity_from_dict(cls, type_: str, obj_d: dict):
        """Factory function
        Creates a new entity of a given type providing its name and entity data.
        It calls create_from_dict child method of the given entity type, passing obj_d.

        :param type_: (str) the entity type name i.e: 'Account', 'User', 'FunctionType', 'Stream'.
        :param obj_d: (dict) the entity data.
        """
        class_name = '%sEntity' % type_.capitalize()
        try:
            entity_type = getattr(sys.modules[__name__], class_name)
        except AttributeError:
            raise EntityFactoryError(class_name)
        return entity_type.create_from_dict(obj_d)

    @property
    @abstractmethod
    def as_dict(self) -> dict:
        return dict(
            uuid=str(self.uuid),
            created=format_dt(self._created), )

    @staticmethod
    def get_base_kwargs(obj_d: dict) -> dict:
        return dict(
            uuid=UUID(obj_d.get('uuid')),
            created=parse_dt(obj_d.get('created')), )


class AccountEntity(EntityContract):
    def __init__(self, auth_id: str, username: str, email: str, date_joined: datetime,
                 last_login: datetime = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._auth_id = auth_id
        self._username = username
        self._email = email
        self._date_joined = date_joined
        self._last_login = last_login

    @classmethod
    def create_from_dict(cls, obj_d):
        last_login = obj_d.get('last_login')
        return cls(
            **cls.get_base_kwargs(obj_d),
            auth_id=obj_d.get('auth_id'),
            username=obj_d.get('username'),
            email=obj_d.get('email'),
            date_joined=parse_dt(obj_d.get('date_joined')),
            last_login=parse_dt(last_login) if last_login else None, )

    @property
    def as_dict(self) -> dict:
        acc_d = super().as_dict
        acc_d.update(dict(
            auth_id=self._auth_id,
            username=self._username,
            email=self._email,
            date_joined=format_dt(self._date_joined),
            last_login=format_dt(self._last_login) if self._last_login else None, ))

        return acc_d


class BusinessEntity(EntityContract):
    def __init__(self, master_account: AccountEntity, organization_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._master_account = master_account
        self._organization_name = organization_name

    @classmethod
    def create_from_dict(cls, obj_d):
        return cls(
            **cls.get_base_kwargs(obj_d),
            master_account=AccountEntity.create_from_dict(
                obj_d.get('master_account')),
            organization_name=obj_d.get('organization_name'), )

    @property
    def as_dict(self) -> dict:
        bs_d = super().as_dict
        bs_d.update(dict(
            master_account=self._master_account.as_dict,
            organization_name=self._organization_name,
        ))

        return bs_d


class UserEntity(EntityContract):
    def __init__(self, account: AccountEntity, business: BusinessEntity, first_name: str,
                 last_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._account = account
        self._business = business
        self._first_name = first_name
        self._last_name = last_name

    @classmethod
    def create_from_dict(cls, obj_d: dict):
        return cls(
            **cls.get_base_kwargs(obj_d),
            account=AccountEntity.create_from_dict(obj_d.get('account')),
            business=BusinessEntity.create_from_dict(obj_d.get('business')),
            first_name=obj_d.get('first_name'),
            last_name=obj_d.get('last_name'),
        )

    @property
    def as_dict(self) -> dict:
        user_d = super().as_dict
        user_d.update(dict(
            account=self._account.as_dict,
            business=self._business.as_dict,
            first_name=self._first_name,
            last_name=self._last_name, ))

        return user_d


class WorkspaceEntity(EntityContract):
    def __init__(self, name: str, business: BusinessEntity, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = name
        self._business = business

    @classmethod
    def create_from_dict(cls, obj_d):
        return cls(
            **cls.get_base_kwargs(obj_d),
            name=obj_d.get('name'),
            business=BusinessEntity.create_from_dict(obj_d.get('business')),
        )

    @property
    def as_dict(self) -> dict:
        ws_d = super().as_dict
        ws_d.update(dict(
            name=self._name,
            business=self._business.as_dict,
        ))

        return ws_d


class FunctionTypeEntity(EntityContract):
    def __init__(self, key: str, verbose_name: str, description: str, updated: datetime,
                 account: AccountEntity, inputs: List[InputConfig] = None,
                 outputs: List[OutputConfig] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._key = key
        self._verbose_name = verbose_name
        self._description = description
        self._updated = updated
        self._inputs = inputs
        self._outputs = outputs
        self._account = account

    @classmethod
    def create_from_dict(cls, obj_d: dict):
        inputs_d = obj_d.get('inputs')
        inputs = [InputConfig.deserialize(it)
                  for it in inputs_d] if inputs_d else None
        outputs_d = obj_d.get('outputs')
        outputs = [OutputConfig.deserialize(
            ot) for ot in outputs_d] if outputs_d else None
        return cls(
            **cls.get_base_kwargs(obj_d),
            key=obj_d.get('key'),
            verbose_name=obj_d.get('verbose_name'),
            description=obj_d.get('description'),
            updated=parse_dt(obj_d.get('updated')),
            inputs=inputs,
            outputs=outputs,
            account=AccountEntity.create_from_dict(obj_d.get('account')),
        )

    @property
    def as_dict(self) -> dict:
        ft_d = super().as_dict
        ft_d.update(dict(
            key=self._key,
            verbose_name=self._verbose_name,
            description=self._description,
            updated=format_dt(self._updated),
            inputs=[it.serialize for it in self._inputs] if self._inputs else None,
            outputs=[
                ot.serialize for ot in self._outputs] if self._outputs else None,
            account=self._account.as_dict, ))

        return ft_d


class StreamEntity(EntityContract):
    STATUS = [
        ('settled', 'Settled'),
        ('pushed', 'Pushed'),
        ('paused', 'Paused'),
        ('cancelled', 'Cancelled'),
        ('finished', 'Finished'),
    ]

    def __init__(self, name: str, updated: datetime, status: str, account: AccountEntity,
                 pushed: datetime = None, finished: datetime = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = name
        self._pushed = pushed
        self._updated = updated
        self._finished = finished
        self._status = status
        self._account = account

    @classmethod
    def create_from_dict(cls, obj_d: dict):
        pushed = obj_d.get('pushed')
        finished = obj_d.get('finished')
        return cls(
            **cls.get_base_kwargs(obj_d),
            name=obj_d.get('name'),
            pushed=parse_dt(pushed) if pushed else None,
            updated=parse_dt(obj_d.get('updated')),
            finished=parse_dt(finished) if finished else None,
            status=obj_d.get('status'),
            account=AccountEntity.create_from_dict(obj_d.get('account')),
        )

    @property
    def as_dict(self) -> dict:
        stream_d = super().as_dict
        stream_d.update(dict(
            name=self._name,
            pushed=format_dt(self._pushed) if self._pushed else None,
            updated=format_dt(self._updated),
            finished=format_dt(self._finished) if self._finished else None,
            status=self._status,
            account=self._account.as_dict, ))

        return stream_d


class FunctionInstanceEntity(EntityContract):
    STATUS = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('blocked', 'Blocked'),
        ('canceled', 'Canceled'),
        ('completed', 'Completed'),
    ]

    def __init__(self, function_type: FunctionTypeEntity, stream: StreamEntity,
                 position: PositionConfig, updated: datetime, status: str,
                 initialized: datetime = None, completed: datetime = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._function_type = function_type
        self._stream = stream
        self._position = position
        self._initialized = initialized
        self._updated = updated
        self._completed = completed
        self._status = status

    @classmethod
    def create_from_dict(cls, obj_d: dict):
        initialized = obj_d.get('initialized')
        completed = obj_d.get('completed')
        return cls(
            **cls.get_base_kwargs(obj_d),
            function_type=FunctionTypeEntity.create_from_dict(
                obj_d.get('function_type')),
            stream=StreamEntity.create_from_dict(obj_d.get('stream')),
            position=PositionConfig.deserialize(obj_d.get('position')),
            initialized=parse_dt(initialized) if initialized else None,
            updated=parse_dt(obj_d.get('updated')),
            completed=parse_dt(completed) if completed else None,
            status=obj_d.get('status'),
        )

    @property
    def as_dict(self) -> dict:
        fi_d = super().as_dict
        fi_d.update(dict(
            function_type=self._function_type.as_dict,
            stream=self._stream.as_dict,
            position=self._position.serialize,
            initialized=format_dt(
                self._initialized) if self._initialized else None,
            updated=format_dt(self._updated),
            completed=format_dt(self._completed) if self._completed else None,
            status=self._status, ))

        return fi_d

    def get_input(self, input_name: str):
        pass


class VariableEntity(EntityContract):
    def __init__(self, iot: str, id_name: str, type_: str, charset: str, bytes_: bytes,
                 fi_uuid: str, rank: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._iot = iot
        self._id_name = id_name
        self._type = type_
        self._charset = charset
        self._bytes = bytes_
        self._fi_uuid = fi_uuid
        self._rank = rank

    @classmethod
    def create_from_dict(cls, obj_d: dict):
        return cls(
            **cls.get_base_kwargs(obj_d),
            iot=obj_d.get('iot'),
            id_name=obj_d.get('id_name'),
            type_=obj_d.get('type'),
            charset=obj_d.get('charset'),
            bytes_=decode_b64str(obj_d.get('body')),
            fi_uuid=obj_d.get('fi_uuid'),
            rank=obj_d.get('__rank__'),
        )

    @property
    def as_dict(self) -> dict:
        var_d = super().as_dict
        var_d.update(dict(
            iot=self._iot,
            id_name=self._id_name,
            type=self._type,
            charset=self._charset,
            body=bytes_to_b64str(self._bytes),
            fi_uuid=str(self._fi_uuid),
            __rank__=self._rank, ))

        return var_d

    @property
    def to_var(self) -> Variable:
        return Variable.create(
            type_=self._type,
            id_name=self._id_name,
            bytes_=self._bytes,
            charset=self._charset,
        )


class FunctionInstanceLogMessageEntity(EntityContract):
    LOG_LEVELS = [('debug', 'Debug'),
                  ('info', 'Info'),
                  ('warning', 'Warning'),
                  ('error', 'Error')]

    def __init__(self, fi_uuid: UUID, log_message: str,
                 log_level: str = LOG_LEVELS[1][0], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._fi_uuid = fi_uuid
        self._log_message = log_message
        self._log_level = log_level

    @classmethod
    def create_from_dict(cls, obj_d: dict):
        return cls(
            **cls.get_base_kwargs(obj_d),
            fi_uuid=UUID(obj_d.get('fi_uuid')),
            log_message=obj_d.get('log_message'),
            log_level=obj_d.get('log_level', cls.LOG_LEVELS[1][0]),
        )

    @property
    def as_dict(self) -> dict:
        fi_log_message_d = super().as_dict
        fi_log_message_d.update(dict(
            fi_uuid=str(self._fi_uuid),
            log_message=self._log_message,
            log_level=self._log_level, ))

        return fi_log_message_d
