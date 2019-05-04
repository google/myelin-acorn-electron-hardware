#!/bin/bash
set -euxo pipefail

HERE=$(dirname $0)
rm -rf env2 env3

unset PYTHONHOME
ORIG_PATH="$PATH"

python2 -m virtualenv env2
export VIRTUAL_ENV=$HERE/env2
export PATH=$VIRTUAL_ENV/bin:$ORIG_PATH
pip install -e .

python3 -m venv env3
export VIRTUAL_ENV=$HERE/env3
export PATH=$VIRTUAL_ENV/bin:$ORIG_PATH
pip install -e .
