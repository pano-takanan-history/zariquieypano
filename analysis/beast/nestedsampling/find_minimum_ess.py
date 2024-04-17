#!/usr/bin/env python3
# coding=utf-8
import re
import sys
import codecs
from pathlib import Path

is_whitespace = re.compile(r"""\s+""")

def read(filename):
    header = None
    with codecs.open(filename, 'r', 'utf8') as handle:
        for line in handle:
            line = [_.strip() for _ in is_whitespace.split(line)]
            if not header:
                header = line
            else:
                yield dict(zip(header, line))

def find_min(variable, rows, key="item"):
    minimum = (None, sys.maxsize)
    for r in rows:
        assert variable in r, 'Variable %s not in rows' % variable
        v = float(r[variable])
        if v < minimum[1]:
            minimum = (r[key], v)
    return minimum


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Finds the minimum ESS from an HPD file')
    parser.add_argument("filenames", help='filename(s)', nargs="+")
    args = parser.parse_args()

    for filename in args.filenames:
        print("%-30s\t%-50s\t%0.3f" % (filename, *find_min("ESS", read(filename))))

