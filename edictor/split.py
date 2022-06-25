"""
Split data into 10 subsets.
"""

from lingpy import *
from lingpy.convert.strings import write_nexus
import random
random.seed(1234)

body = Wordlist("pano-body-parts.tsv")
auto = Wordlist("pano-auto.tsv")

# get length of characters
clen = len(body.rows)

# iterate and split
for i in range(10):
    run = "pano-subset-{0}.nex".format(str(i+1))
    concepts = random.sample(auto.rows, clen)
    D = {0: [c for c in auto.cols]}
    for idx, concept in auto.iter_rows("concept"):
        if concept in concepts:
            D[idx] = [auto[idx, c] for c in D[0]]
    wl = Wordlist(D)
    write_nexus(wl, mode="beastwords", filename="../analysis/beast/"+run)
    write_nexus(wl, mode="mrbayes", filename="../analysis/mb/"+run)



