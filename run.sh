#!/bin/bash

home=$(dirname "$(realpath "$0")")
test_dir=$home/tests/chi
test_output=$home/outputs/chi
test_script=$home/src/specgen.py
test_format=hemiola
test_target=CHI

usage() {
    echo "Usage: $0 [--test]"
    echo "Options:"
    echo "  --test     : Run in test mode"
    echo "  -h, --help : Display this help message"
    exit 1
}

if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    usage
fi

test_mode=false
if [ "$1" = "--test" ]; then
    test_mode=true
    shift
fi

if [ "$test_mode" = true ]; then
    mkdir -p $test_output
    python3 $test_script -f $test_format -i $test_dir -o $test_output -t $test_target
    exit 0
fi
