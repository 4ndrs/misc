#!/usr/bin/env python3
#
# qblist.py:
#       Prints a list of files sorted by size in descending order
#       from a given path using ls with subprocess
#
# Copyright (c) 2022
# Andres Eloy Rivera Garcia
#
# SPDX-License-Identifier: MIT
#
from os.path import realpath
import subprocess
import sys
import re

# Usage: ./% /path/to/files
if len(sys.argv) < 2:
    print(f'{sys.argv[0]}: No arguments given', file=sys.stderr)
    sys.exit(1)

path    = realpath(sys.argv[1]) # For link dereferencing support
result  = subprocess.run(['ls', '-la', path], capture_output=True)

if result.returncode != 0:
    print(result.stderr.decode(), end='', file=sys.stderr)
    sys.exit(result.returncode)

files   = []
pattern = r'.*[ ]+([\d]+)[ ]+[\w]{3}[ ]+[\d]{,2}[ ]+[\d]{2}[:]{,1}[\d]{2}[ ]+(.+)'

for line in result.stdout.decode().split('\n'):
    if not line.startswith('-'): continue # Process only regular files
    size, filename = re.search(pattern, line).groups()
    files.append((int(size), filename))

files.sort(reverse=True)

print(f'{"Size":>10} - Filename')
for file in files:
    size, filename = file

    if   (size / 1.074e+9) > 1: size = f'{size / 1.074e+9:.0f}' + 'GiB'
    elif (size / 1.049e+6) > 1: size = f'{size / 1.049e+6:.0f}' + 'MiB'
    elif (size / 1024)     > 1: size = f'{size / 1024:.0f}'     + 'KiB'
    else                      : size = f'{size}'                + 'B'

    print(f'{size:>10} - {filename}')
