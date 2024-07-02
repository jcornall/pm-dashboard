#!/bin/bash

# Shell script to execute the __main__.py module with the virtual environment interpreter
PYSCRIPT_NAME="__main__.py"

CWD="$(dirname -- "$0")"
PATH="$CWD/.venv.Scripts:$PATH"

"$CWD/$PYSCRIPT_NAME" "$@"

return