#!/bin/bash
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