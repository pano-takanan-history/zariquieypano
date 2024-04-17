#!/usr/bin/env python3
# coding=utf-8
import re
from collections import namedtuple
from pathlib import Path

Likelihood = namedtuple("Likelihood", ['Marginal', 'H_N', 'SD', 'Information'])


is_regex = re.compile(r"""^Marginal likelihood: (.*) sqrt\(H/N\)=\((.*)\)=\?=SD=\((.*)\) Information: (.*)$""")


def read(filename):
    with open(filename, 'r') as handle:
        for line in handle:
            if m:= is_regex.match(line):
                yield Likelihood(*[float(f) for f in m.groups()])



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("filenames", help='filename(s)', nargs="+")
    args = parser.parse_args()

    print("%-30s\t%s\t%s\t%s\t%s" % ('Filename', 'Marginal Lh', 'H/N', 'SD', 'Information'))
    for filename in args.filenames:
        for r in read(filename):
            print("%-30s\t%0.4f\t%0.4f\t%0.4f\t%0.4f" % (Path(filename).stem, r.Marginal, r.H_N, r.SD, r.Information))
