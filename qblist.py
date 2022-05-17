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
import subprocess
import sys
import re
import os

# Usage: ./% /path/to/files
#        ./% /path/to/files -R
#        ./% /path/to/files -R --limit 10
if len(sys.argv) < 2:
    print(f'{sys.argv[0]}: No arguments given', file=sys.stderr)
    sys.exit(1)

recursive   = False
limit       = None
path        = os.path.realpath(sys.argv[1]) # For link dereferencing support

if len(sys.argv) > 2 and sys.argv[2] == '-R': recursive = True
if len(sys.argv) > 4 and sys.argv[3] == '--limit' and sys.argv[4].isnumeric(): limit = int(sys.argv[4])

if not recursive: result = subprocess.run(['ls', '-la', path], capture_output=True)
else            : result = subprocess.run(['ls', '-la', '--recursive', path], capture_output=True)

if result.returncode != 0 and result.returncode != 1:
    print(result.stderr.decode(), end='', file=sys.stderr)
    sys.exit(result.returncode)
elif result.returncode == 1: print(result.stderr.decode(), end='', file=sys.stderr) # permission denied

files   = []
header  = None
pattern = r'.*[ ]+([\d]+)[ ]+[\w]{3}[ ]+[\d]{,2}[ ]+[\d]{2}[:]{,1}[\d]{2}[ ]+(.+)'

for line in result.stdout.decode().split('\n'):
    if recursive and re.match('^\./|^/', line): header = line[:-1]
    if not line.startswith('-'): continue # Process only regular files
    size, filename = re.search(pattern, line).groups()
    if recursive: filename = os.path.join(header, filename)
    files.append((int(size), filename))

files.sort(reverse=True)

if limit is None: limit = len(files) - 1

print(f'{"Size":>10} - Filename')
for file in files[:limit]:
    size, filename = file

    if   (size / 1.074e+9) > 1: size = f'{size / 1.074e+9:.0f}' + 'GiB'
    elif (size / 1.049e+6) > 1: size = f'{size / 1.049e+6:.0f}' + 'MiB'
    elif (size / 1024)     > 1: size = f'{size / 1024:.0f}'     + 'KiB'
    else                      : size = f'{size}'                + 'B'

    print(f'{size:>10} - {filename}')
