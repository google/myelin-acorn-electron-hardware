#!/bin/bash
set -euxo pipefail

# Shared env
ENV=$HOME/pypi-env
# ENV=$(dirname $0)/env

if [ ! -d "$ENV" ]; then
    python3 -m venv $ENV
fi

# activate our virtualenv
export VIRTUAL_ENV=$ENV
export PATH=$ENV/bin:$PATH
unset PYTHONHOME

# install prereqs
pip install twine wheel keyring

# build the package
rm -rf build dist
python setup.py sdist bdist_wheel --universal

# push to pypi
python -m twine upload -u myelin dist/*
