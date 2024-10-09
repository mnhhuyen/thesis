#!/bin/bash

# Find all .py files in the current directory and run them in parallel with python3
find . -name "*.py" | xargs -n 1 -P 0 python3
