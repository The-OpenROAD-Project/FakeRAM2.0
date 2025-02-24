#!/usr/bin/env bash

set -eoux pipefail

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

for test_file in $SCRIPT_DIR/*_test.py; do
    $test_file
done
