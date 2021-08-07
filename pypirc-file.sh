#!/bin/sh

FILE="./.pypirc"

cat >$FILE <<EOL
[distutils]
index-servers=
    pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username: $PYPI_USERNAME
password: $PYPI_PASSWORD
EOL