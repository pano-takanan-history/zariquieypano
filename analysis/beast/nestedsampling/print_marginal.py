#!/usr/bin/env python3
# coding=utf-8
import re
from collections import namedtuple
from pathlib import Path

Likelihood = namedtuple("Likelihood", ['Marginal', 'H_N', 'SD', 'Information', 'MaxESS'])


is_regex1 = re.compile(r"""^Marginal likelihood: (.*) sqrt\(H/N\)=\((.*)\)=\?=SD=\((.*)\) Information: (.*)$""")
is_regex2 = re.compile(r"""^Max ESS: (.*)$""")


def read(filename):
    lh, max_ess = None, None
    with open(filename, 'r') as handle:
        for line in handle:
            if m:= is_regex1.match(line):
                lh = [float(f) for f in m.groups()]
            elif m:= is_regex2.match(line):
                max_ess = [float(m.groups()[0])]
    if max_ess:
        lh.append(max_ess[0])
    return Likelihood(*lh)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("filenames", help='filename(s)', nargs="+")
    args = parser.parse_args()
    
    results = []
    for filename in args.filenames:
        r = read(filename)
        out = "%-35s\t%0.4f\t%0.4f\t%0.4f\t%0.4f\t%0.4f" % (Path(filename).stem, r.Marginal, r.H_N, r.SD, r.Information, r.MaxESS)
        results.append((r.Marginal, out))


    print("%-35s\t%s\t%s\t%s\t%s\t%s" % ('Filename', 'Marginal Lh', 'H/N', 'SD', 'Information', 'MaxESS'))
    for m, o in sorted(results, reverse=True):
        print(o)