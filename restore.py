#!/usr/bin/env python3
#
# restore.py:
#       A simple script to serialize database into yaml, or json
#
# Copyright (c) 2022
# Andres Eloy Rivera Garcia
#
# SPDX-License-Identifier: MIT
#
import pickle
import yaml
import json
from re import match

iname   = 'anime.list' # Database name
oname   = 'anime.yaml' # Use .json for json serialization, .yaml for yaml

with open(iname, 'rb') as file: 
    data = pickle.load(file, encoding='bytes')

with open(oname, 'w') as file:
    if   match('.*(.json)', oname): json.dump(data, file, sort_keys=True, default=str, indent=4)
    elif match('.*(.yaml)', oname): yaml.dump(data, file)
    else: print('Unrecognized file extension:', oname)
