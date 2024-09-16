#!/bin/bash

set -eu

pushd $(dirname $0) > /dev/null

GOLANG_MIGRATE_VERSION="4.18.1"

# Shell script to setup and activate a Python virtual environment
python3.12 -m pip install virtualenv
python3.12 -m virtualenv .venv
if [[ "$OSTYPE" == "linux-gnu"* ]]
then
    source .venv/bin/activate
    pip install -r requirements.txt
else [[ "$OSTYPE" == "msys" ]]
    source .\\venv\\Scripts\\activate
    pip install -r requirements.txt
fi

mkdir -p ./golang-migrate
pushd ./golang-migrate > /dev/null
curl -L https://github.com/golang-migrate/migrate/releases/download/v${GOLANG_MIGRATE_VERSION}/migrate.linux-amd64.tar.gz | tar xvz
popd > /dev/null

popd > /dev/null
