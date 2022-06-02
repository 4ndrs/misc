#!/usr/bin/env python3
#
# Copyright (c) 2022
# Andes Eloy Rivera Garcia
#
# SPDX-License-Identifier: MIT
#
"""Generate a list of files with their md5sum.

   Makes a list of dictionaries containing the files' name, md5sum, and mtime.
   The list will be restricted by {MIMETYPE} and saved in the current working
   directory as {FILENAME} using yaml.
"""

import os
import re
from subprocess import check_output as co

import yaml

FILENAME = ".md5list.yaml"
MIMETYPE = "text/x-python"  # restrict to only python files

if __name__ == "__main__":
    md5list = []
    for file in os.listdir():
        if re.search(r".*: " + MIMETYPE, co(["mimetype", file]).decode()) is None:
            continue
        md5 = re.search(r"\S+", co(["md5sum", file]).decode())[0]
        mtime = os.path.getmtime(file)

        md5list.append({"name": file, "md5": md5, "mtime": mtime})

    with open(FILENAME, "w", encoding="utf-8") as file:
        yaml.dump(md5list, file)
