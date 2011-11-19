#!/usr/bin/env python

import glob
import subprocess
import re

VAR_LOG_MESSAGES = "/var/log/messages"
DOCK = "+"
UNDOCK = "-"

def get_dock_strings():
    dock_strings = []
    all_files = [VAR_LOG_MESSAGES]
    all_files.extend(glob.glob(VAR_LOG_MESSAGES+".*"))
    all_files.reverse() # ASCENDING
    for filename in all_files:
        cmdline = ["zgrep", "docking", filename]
        proc = subprocess.Popen(cmdline, stdout=subprocess.PIPE)
        stdout = proc.communicate()[0]

        for line in stdout.split("\n"):
            if line:
                print filename, line
                dock_strings.append(line)

    return dock_strings

def parse_dock_strings(dock_strings):
    parsed_events = []
    for dock_string in dock_strings:
        regexp = re.search("^(\S+)\s+(\S+)\s+(\S+)", dock_string)

        if not regexp:
            raise Exception("Bad line '%s'" % dock_string)

        (mon, mday, hour) = regexp.groups()
        if " undocking" in dock_string:
            action = UNDOCK
        elif " docking" in dock_string:
            action = DOCK
        else:
            raise Exception("Bad line '%s'" % dock_strings)

        parsed_events.append( (action, (mon, mday, hour)) )

    return parsed_events

def main():
    dock_strings = get_dock_strings()
    parsed_data = parse_dock_strings(dock_strings)
    for item in parsed_data:
        print item[0], " ".join(item[1])

if __name__ == "__main__":
    main()
