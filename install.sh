#!/bin/bash

python3.12 -m pip install virtualenv
python3.12 -m virtualenv .venv
source .\.venv\Scripts\activate
pip install -r requirements.txt