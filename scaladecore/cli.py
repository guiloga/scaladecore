from importlib import util
import os
import yaml
from shutil import copytree, rmtree, ignore_patterns

import click
from scaladecore.config import FunctionConfig
from scaladecore.utils import encode_scalade_token, generate_token_payload


WORKING_DIR = os.getcwd()

FIXTURES_DIR = os.path.join(
    os.path.dirname(__file__), 'fixtures')

FUNCTION_MODULE = None


@click.group()
def cli_handler():
    pass


command_collection = click.CommandCollection(
    help="##### Scalade CLI Application (cmd alias 'scalade') #####\n\n"
         "This is the Scalade CLI manager that allows the following operations: "
         "generate a new token, run a function, start a new function project, "
         "verify a function configuration.",
    sources=[cli_handler, ])


@cli_handler.command('token')
@click.argument('fi_uuid', type=str, envvar='FI_UUID')
def generate_token(fi_uuid):
    """Generates an new token with the given FunctionInstance (fi_uuid)."""
    _generate_token(fi_uuid)


@cli_handler.command('startfunction')
@click.option('-t', '--template', help='The selected fixture template project to start.',
              default='random_person_names')
@click.option('-D', '--destdir',
              help='Overrides destination directory of the project files (default: current dir).')
@click.argument('project_name', type=str)
def start_function(project_name, **options):
    """Starts a new Scalade Function project by a template project."""
    _start_function(project_name, **options)


@cli_handler.command('run')
@click.option('-A', '--function', type=str,
              help='Function module path. Default location is $(pwd)/src/function.py.')
@click.option('--self', is_flag=True,
              help='With this flag it runs with Self mode (suitable for development).')
def run(**options):
    """Runs a FunctionInstance."""
    _run(**options)


@cli_handler.command('verifyconfig')
@click.argument('config', type=str)
def verify_config(config):
    """Verifies a Function config."""
    _verify_config(config)


def _generate_token(fi_uuid: str) -> str:
    payload = generate_token_payload(fi_uuid)
    token = encode_scalade_token(payload)
    print("Generated token with payload %s\nSCALADE_FI_TOKEN=%s" %
          (payload, token))


def _start_function(project_name: str, template: str, destdir: str = None):
    src = os.path.join(FIXTURES_DIR, template)
    if destdir:
        dest = os.path.join(destdir, project_name)
    else:
        dest = os.path.join(
            WORKING_DIR,
            project_name)
    try:
        copytree(src, dest,
                 ignore=ignore_patterns('*.pyc', 'tmp*'),
                 ignore_dangling_symlinks=True)
        error = None
    except FileExistsError as exc:
        error = exc
    except Exception as exc:
        rmtree(dest)
        error = exc
    finally:
        if error:
            print(f'An error occurred: {error}')
        else:
            print("Started a new function project '%s' located at '%s'"
                  % (project_name, dest))


def _run(function: str = None, **kwargs):
    def import_function_module(function_file):
        global FUNCTION_MODULE

        spec = util.spec_from_file_location('function_module', function_file)
        FUNCTION_MODULE = util.module_from_spec(spec)
        spec.loader.exec_module(FUNCTION_MODULE)

    def find_scalade_func(function_file):
        err = import_function_module(function_file)
        if not err:
            attr_names = [
                item for item in FUNCTION_MODULE.__dict__ if item[:2] != '__']
            for name in attr_names:
                attr_ = getattr(FUNCTION_MODULE, name)
                try:
                    if attr_.__qualname__ == 'scalade_func.<locals>.execute':
                        return attr_
                except AttributeError:
                    pass

        # todo: custom exception
        raise Exception()

    self_mode = kwargs.get('self')
    if not function:
        function_file = os.path.join(WORKING_DIR, 'src', 'function.py')
    else:
        function_file = function

    scalade_func = find_scalade_func(function_file)
    print("Running Function in '%s' mode .." %
          ('self' if self_mode else 'scalade'))
    scalade_func.__call__()


def _verify_config(config_file: str):
    filepath = config_file
    try:
        with open(filepath, 'r') as file:
            config_data = yaml.safe_load(file)
    except FileNotFoundError as exc:
        print(f'An error occurred: {exc}')
        return
    try:
        for i, ipt in enumerate(config_data['inputs']):
            ipt['__rank__'] = i
        for j, opt in enumerate(config_data['outputs']):
            opt['__rank__'] = j
        _ = FunctionConfig.deserialize(
            config_data)
    except Exception as exc:
        print("Function configuration is invalid\n%s: %s" %
              (exc.__class__.__name__, exc))
        return

    print('Verified Function configuration ..')


if __name__ == '__main__':
    command_collection()
