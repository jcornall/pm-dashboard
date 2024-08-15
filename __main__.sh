#!/bin/bash
# Shell script to execute the __main__.py module with the virtual environment interpreter
source ~/.bash_profile
PYSCRIPT_NAME="__main__.py"
CWD="$(dirname -- "$0")"
PATH="$CWD/.venv/Scripts:$PATH"
if [[ "$OSTYPE" == "linux-gnu"* ]];
then
    PATH="$CWD/.venv/bin:$PATH"
elif [[ "$OSTYPE" == "msys" ]];
then
    PATH="$CWD/.venv/Scripts:$PATH"
fi
"$CWD/$PYSCRIPT_NAME" "$@"