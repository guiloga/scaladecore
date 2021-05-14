from .managers import ContextManager

import os


def main_handler(func):
    def execute(*args, **kwargs):
        FI_TOKEN = os.getenv('FI_TOKEN')
        context = ContextManager.initialize_from_token(FI_TOKEN)
        return func(context)

    return execute
