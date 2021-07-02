from .managers import ContextManager

import os


def scalade_func(func):
    def execute(*args, **kwargs):
        SCALADE_FI_TOKEN = os.getenv('SCALADE_FI_TOKEN')
        context = ContextManager.initialize_from_token(SCALADE_FI_TOKEN)
        return func(context)

    return execute
