#!/bin/bash

PYSCRIPT_NAME="__main__.py"

CWD="$(dirname "$0")"
PATH="$CWD/.venv.bin:$PATH"

"$CWD/$PYSCRIPT_NAME" "$@"

exit $?