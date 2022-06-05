#!/usr/bin/env python3
#
# Copyright (c) 2022
# Andres Eloy Rivera Garcia
#
# SPDX-License-Identifier: MIT
"""Change the status of a given process (or a group of processes) sending SIGSTOP/SIGCONT"""

import sys
from os import getpid
from subprocess import check_output, CalledProcessError

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Arguments must be given to proceed")
        sys.exit(1)
    elif len(sys.argv) < 3:
        print("An action must be given to proceed")
        sys.exit(2)
    elif sys.argv[2] != "suspend" and sys.argv[2] != "continue":
        print(
            f"Unrecognized action: {sys.argv[2]}\n"
            "The action can be either 'suspend' or 'continue'"
        )
        sys.exit(3)
    else:
        process_txt = sys.argv[1]
        suspend = sys.argv[2] == "suspend"

    try:
        PIDS = check_output(["pgrep", "-f", process_txt]).decode().strip().split("\n")
    except CalledProcessError:  # For some reason this isn't being thrown when executed as a script
        print("No processes found")
        sys.exit(4)

    OUR_PID = str(getpid())
    if OUR_PID in PIDS:
        PIDS.remove(OUR_PID)

    for pid in PIDS:
        if suspend:
            check_output(["kill", "-SIGSTOP", pid])
        else:
            check_output(["kill", "-SIGCONT", pid])

    print(f"Signaled {len(PIDS)} process", end="")
    if len(PIDS) > 1 or len(PIDS) < 1:
        print("es")
    else:
        print()
    sys.exit(0)
