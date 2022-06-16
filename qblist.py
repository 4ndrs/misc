#!/usr/bin/env python3
# Copyright (c) 2022 4ndrs <andres.degozaru@gmail.com>
# SPDX-License-Identifier: MIT
"""Prints a list of files sorted by size in descending order from a given path using ls
   with subprocess

   Usage: qblist /path/to/files
          qblist /path/to/files -R
          qblist /path/to/files -R --limit 10
"""

import subprocess
import sys
import re
import os

if len(sys.argv) < 2:
    print(f"{sys.argv[0]}: No arguments given", file=sys.stderr)
    sys.exit(1)

RECURSIVE = False
LIMIT = None
path = os.path.realpath(sys.argv[1])  # For link dereferencing support

if len(sys.argv) > 2 and sys.argv[2] == "-R":
    RECURSIVE = True
if len(sys.argv) > 4 and sys.argv[3] == "--limit" and sys.argv[4].isnumeric():
    LIMIT = int(sys.argv[4])

if not RECURSIVE:
    result = subprocess.run(["ls", "-la", path], check=True, capture_output=True)
else:
    result = subprocess.run(["ls", "-la", "-R", path], check=True, capture_output=True)

if result.returncode not in (0, 1):
    print(result.stderr.decode(), end="", file=sys.stderr)
    sys.exit(result.returncode)
elif result.returncode == 1:
    print(result.stderr.decode(), end="", file=sys.stderr)  # permission denied

files = []
HEADER = None
PATTERN = r".*[ ]+([\d]+)[ ]+[\w]{3}[ ]+[\d]{,2}[ ]+[\d]{2}[:]{,1}[\d]{2}[ ]+(.+)"

for line in result.stdout.decode().split("\n"):
    if RECURSIVE and re.match(r"^\./|^/", line):
        HEADER = line[:-1]
    if not line.startswith("-"):
        continue  # Process only regular files
    size, filename = re.search(PATTERN, line).groups()
    if RECURSIVE:
        filename = os.path.join(HEADER, filename)
    files.append((int(size), filename))

files.sort(reverse=True)

if LIMIT is None:
    LIMIT = len(files)

print(f'{"Size":>10} - Filename')
for file in files[:LIMIT]:
    size, filename = file

    if (size / 1.074e9) > 1:
        size = f"{size / 1.074e+9:.0f}" + "GiB"
    elif (size / 1.049e6) > 1:
        size = f"{size / 1.049e+6:.0f}" + "MiB"
    elif (size / 1024) > 1:
        size = f"{size / 1024:.0f}" + "KiB"
    else:
        size = f"{size}" + "B"

    print(f"{size:>10} - {filename}")
