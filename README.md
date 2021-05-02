# scaladecore

### Scalade function creation core package

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

```
docker-compose run test
```

Optionally, run code static analysis (with flake8):

```
docker-compose run static_analysis
```

### Build

```
# Create setup.py file:
touch setup.py
echo "import setuptools
setuptools.setup()" > setup.py

# Build the distribution in .zip format:
python setup.py bdist --format=zip
```

In development create a link file which associates source code with your interpreter site-packages directory:

```
pip install --editable .
```

Upload it yo PyPi with
**twine**

## Resources

* TODO

## Authors

* **Guillem López Garcia** - [guiloga](https://github.com/guiloga)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
