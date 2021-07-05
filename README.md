# scaladecore

### Scalade function creation core package.

____
[![Build Status](https://www.travis-ci.com/guiloga/guilogacore-rpc.svg?branch=master)](https://www.travis-ci.com/guiloga/guilogacore-rpc)

This package provides core functionality for creating and deploying Functions into [**Scalade**](https://scalade.io) web
automation platform.

## Prerequisites ###

* Python version [**3.6**](https://www.python.org/downloads/release/python-380/) (
  with [pip](https://pip.pypa.io/en/stable/))

## Documentation ###

Documentation for the package is not available yet.

## Tests

Tests are built with [pytest](https://docs.pytest.org/en/stable/) and run with docker. In order tu run it be sure last
that current stable versions of docker and docker-compose are installed.

Run all **unit** and **integration** tests:

```bash
docker-compose run test
```

Optionally, run code static analysis (with flake8):

```bash
docker-compose run static_analysis
```

## Tooling
For style guide and code formatting is used:
**flake8**, **autopep8**

### Useful commands
```bash
flake8 --max-complexity 10 --ignore E501
```
```bash
autopep8 -i <file>
```

### Build

```bash
# Create setup.py file:
touch setup.py
echo "import setuptools
setuptools.setup()" > setup.py

# Build the distribution in .zip format:
python setup.py bdist --format=zip
```

In development create a link file which associates source code with your interpreter site-packages directory:
```bash
pip install --editable .
```

Upload it yo PyPi with
**twine**

## Resources

* TODO

## Authors

* **Guillem López Garcia** - [guiloga](https://github.com/guiloga)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
