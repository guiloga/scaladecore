from datetime import datetime, timedelta
import os
from uuid import uuid4

import pytest


from scaladecore.utils import format_dt, get_foo_function_config


@pytest.fixture(scope='session', name='function_cd')
def function_config_data():
    config = get_foo_function_config()
    return config.serialize


@pytest.fixture(scope='session', name='var_cd')
def variable_config_data():
    return {
        'id_name': 'my_var',
        'type': 'text',
        'verbose_name': 'My Variable',
        '__rank__': 0,
    }


@pytest.fixture(scope='session')
def account_obj_d():
    return dict(
        **new_base_kwargs(),
        auth_id='xxxxyyyy/test_user',
        username='test_user',
        email='test_user@tryscaffold.com',
        date_joined=format_dt(datetime.utcnow()),
        last_login=format_dt(datetime.utcnow()),
    )


@pytest.fixture(scope='session')
def business_obj_d(account_obj_d):
    return dict(
        **new_base_kwargs(),
        master_account=account_obj_d,
        organization_name='Fake Company',
    )


@pytest.fixture(scope='session')
def user_obj_d(account_obj_d, business_obj_d):
    return dict(
        **new_base_kwargs(),
        account=account_obj_d,
        business=business_obj_d,
        first_name='Foo',
        last_name='Bar',
    )


@pytest.fixture(scope='session')
def workspace_obj_d(business_obj_d):
    return dict(
        **new_base_kwargs(),
        name='default',
        business=business_obj_d,
    )


@pytest.fixture(scope='session')
def function_type_obj_d(function_cd, account_obj_d):
    return dict(
        **new_base_kwargs(),
        key='%s/%s' % (str(account_obj_d.get('uuid'))[:8], function_cd['key']),
        verbose_name=function_cd['verbose_name'],
        description=function_cd['description'],
        updated=format_dt(datetime.utcnow()),
        inputs=function_cd['inputs'],
        outputs=function_cd['outputs'],
        account=account_obj_d,
    )


@pytest.fixture(scope='session')
def stream_obj_d(account_obj_d):
    return dict(
        **new_base_kwargs(),
        name='FakeStream',
        pushed=format_dt(datetime.utcnow()),
        updated=format_dt(datetime.utcnow()),
        finished=format_dt(datetime.utcnow()),
        status='pushed',
        account=account_obj_d,
    )


@pytest.fixture(scope='session')
def function_instance_obj_d(function_type_obj_d, stream_obj_d):
    return dict(
        **new_base_kwargs(),
        function_type=function_type_obj_d,
        stream=stream_obj_d,
        position={'row': 0, 'col': 0},
        initialized=format_dt(datetime.utcnow()),
        updated=format_dt(datetime.utcnow()),
        completed=format_dt(datetime.utcnow()),
        status='pending',
    )


@pytest.fixture(scope='session')
def variable_obj_d():
    return dict(
        **new_base_kwargs(),
        iot='input',
        id_name='fake_input_1',
        type='text',
        charset='utf-8',
        body='TXkgbmFtZSBpcyBGb28gYW5kIEkgbG92ZSBCYXJz',
        fi_uuid=str(uuid4()),
        __rank__=0,
    )


@pytest.fixture(scope='session')
def fi_message_obj_d():
    return dict(
        **new_base_kwargs(),
        fi_uuid=str(uuid4()),
        log_message='This is a log message',
        log_level='info',
    )


@pytest.fixture(scope='session')
def brick_instance_message():
    cd = new_base_kwargs()
    cd['created'] = datetime.utcnow().timestamp()
    return dict(
        **cd,
        bi_uuid=str(uuid4()),
        message='Fake message to log',
    )


@pytest.fixture(scope='session')
def rsa_keys():
    # Generate a new private/public rsa key:
    # $ openssl genrsa -out key.pem 2048
    # Extract the public key
    # $ openssl rsa -in key.pem -pubout -outform PEM -out key.pub
    private_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA6HDtyULvSptZIV32De+/YfA4eeyweElBNwuFFM/oElRp1TqG
w0SZWt+3yOBJce9IK/95r7N2vIQSQRj2xgdXH/UDVIQd82juwfPRcXXdehSk8k2u
MDa+BrwcPydOw1LAVX2T5ZMvV8W0VSoLsuLwSqLDZhTqYfT0w9rqj7fYVkat03yT
6fjJF9OdsMjgY8ftyvcSR2c7jWjVjPH1VYAPxEsmZtz5/RLbtZ6q5LVcZ9ZvwxVT
vDQdI5W+hFWnJ08Bcu9SGJA8Rp+lhNf714SOd8f4uJ5sUZ2BBfcQ96o+HJ1tPog7
pgjweiwZhKOZ9PC3lsXCMY3VxftacNfKCCUVvQIDAQABAoIBAQC0RcFl8m+8ITfD
VShcLrDzuGdUyGklIUte8aRJO+X1MVrTcQzLrQxzGkdjl+/eWYJT/VPXHQzdsGCn
9ECP3WmI83Gdvsmr2pox+nNZ19vprtEuy2hpJEvE1Wfi4w2HF0rsAvUNfFWfcUon
MvDX0IIkoI+DQH13c4/Rxptc020Jm1TdegFFDvRjVAPTbYfdAzpNh+yc8MN5MV40
Nc+7scjyeKM7qOoGdaqIAxHaMlz6YlUMUC0nPqTz7ymKVJ1F3h10nOHARBmB+M5O
Dt491m3dwAdACXxl/ejnsCR1oCROYx4GA6k/zrPjvHQSAlUL2UUb36PoYf9Gg4xQ
A6pSg1jRAoGBAPzWvL7mqzHz1Aj21NvUKA/aOAq+6yITF8gVFHZIzCivO+tek/wo
0HbR7sFHvDTJmG0mLK45t6uSluZnFFcwHdLZQpadOx5cL3/F6RdDkDWXQaXihzbH
+WJGhopiAJfLZacRj/h0KuopCd1vBX/nYoTnUOpo0+boNPwQrmVviYNzAoGBAOtY
55EqJOhW010qXPa/egkXEtPadBRFKo5RBd6ycHgyAHmQsgvf0y5dZ0ut6k+gBMHP
ESxz+1MSakwrhy6XN8X3Z2/jBD2I/6DoBp+xpZizKmkofFJUV6E/fBGgQbRtWFlH
X4lY3vPziC0kwWxR3DMu6zQ3LeW3n6IR1StZa5YPAoGAOieiLj6cLdcpdA5iE1YP
COZmcYJMTwAZPjorBLHl043KuG5+l0dD+7B5vBcl4PZliuV27XP1HQ+Qido3wX4d
vfue50mu6WLGwhrhbCpsJwdtYBxkgWMpp0MVewrjnAZ6kRznAnylyko6LKZ2m167
OFqEMAaAhuHuHfQwSMCI3qUCgYAtW9ItqTi5ytorz5lhOSA1FkxbpnPO4FHGYhlG
hY+lqsVqqJeYMEhMXFYnQNqzA/1GuTjvH19l8FuqWI1STnTCY998sf1EOt5BzdZQ
+vUWjBl1cQcc+wJ0on6wCvn+40Au3NGt8AHwdJRfVwEsdk6BUt6kDqp65rwOiW9T
ToWswwKBgFgBCWJSGlfb7GYgcSa4Q9X85P0CcmZU0uwYvNxaGLirSgNFusfKmE/h
e7oP9kMT1k4IV3EjTZ4wpnOnUJbG9x7fLbpBJtcNzUd+nE68XaM+r78YDnqalH7G
+4Ral2gTA+RaWx+rKn8/D5MFKJSUDEM/4sRw+VBB0+9AOhHzr+fh
-----END RSA PRIVATE KEY-----"""
    public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA6HDtyULvSptZIV32De+/
YfA4eeyweElBNwuFFM/oElRp1TqGw0SZWt+3yOBJce9IK/95r7N2vIQSQRj2xgdX
H/UDVIQd82juwfPRcXXdehSk8k2uMDa+BrwcPydOw1LAVX2T5ZMvV8W0VSoLsuLw
SqLDZhTqYfT0w9rqj7fYVkat03yT6fjJF9OdsMjgY8ftyvcSR2c7jWjVjPH1VYAP
xEsmZtz5/RLbtZ6q5LVcZ9ZvwxVTvDQdI5W+hFWnJ08Bcu9SGJA8Rp+lhNf714SO
d8f4uJ5sUZ2BBfcQ96o+HJ1tPog7pgjweiwZhKOZ9PC3lsXCMY3VxftacNfKCCUV
vQIDAQAB
-----END PUBLIC KEY-----"""
    os.environ['SCALADE_PRIVATE_KEY'] = private_key
    os.environ['SCALADE_PUBLIC_KEY'] = public_key


@pytest.fixture(scope='session')
def running_functions():
    return ['082eef3b-6e74-4242-902d-91122abd7ab2',
            '06b9056f-d41d-4881-8a85-bd801fccad17',
            '03f8a39f-5a6c-4c0a-9d22-02839c52d168', ]


def new_base_kwargs():
    return dict(
        uuid=str(uuid4()),
        created=format_dt(datetime.utcnow()), )

