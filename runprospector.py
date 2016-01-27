#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
runprospector.py

This script runs prospector and processes the output into a Sublime
Plain Tasks ToDo List

@todo Docstring
"""

import subprocess
import os

def main():
    """
    Main Fuction

    Does all the work
    """
    output = subprocess.check_output(['prospector', '-0'])
    linenumber = 0
    summary = False

    processed = ""

    for line in output.split(os.linesep):
        linenumber += 1

        if line.startswith('Check'):
            summary = True

        if (linenumber < 4) or summary or (len(line.strip()) == 0):
            processed += line + os.linesep
            continue

        indent = len(line) -len(line.lstrip())

        if (indent in (0, 2, 4)) and not summary:
            line = line[:indent] + '☐ ' + line[indent:]

        processed += line + os.linesep

    outfile = open('prospector.todo', 'w')
    outfile.write(processed)
    outfile.close()


if __name__ == '__main__':
    main()