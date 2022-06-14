from phylogemetric import DeltaScoreMetric, QResidualMetric
from lingpy import Wordlist
import random
from tabulate import tabulate
from tqdm import tqdm as progressbar
import statistics


def get_deltaq(wordlist, ref, shuffle=False, sample=None):
    matrix = get_matrix(wordlist, ref, shuffle=shuffle, sample=sample)
    delta = DeltaScoreMetric(matrix)
    qres = QResidualMetric(matrix)
    scoresD = delta.score()
    scoresQ = qres.score()
    return (
            statistics.mean(scoresD.values()),
            statistics.stdev(scoresD.values()),
            statistics.mean(scoresQ.values()),
            statistics.stdev(scoresQ.values()))

def get_matrix(wordlist, ref, shuffle=False, sample=None):
    def get_mapper(languages):
        mapper = {}
        idxs = list(range(len(languages)))
        random.shuffle(idxs)
        for i, idx in enumerate(idxs):
            mapper[languages[i]] = languages[idx]
        return mapper
    language_map = {}
    if shuffle:
        language_map = get_mapper(wordlist.cols)

    paps = wordlist.get_paps(ref=ref, missing="?")
    if sample:
        sample = random.sample(list(paps), sample)
        paps = {cogid: paps[cogid] for cogid in sample}
    matrix = {t: [] for t in wordlist.cols}
    language_map = {}
    for cogid, pap in sorted(paps.items(), key=lambda x: x[0]):
        if shuffle:
            language_map = get_mapper(wordlist.cols)
        for i, p in enumerate(pap):
            matrix[language_map.get(
                wordlist.cols[i],
                wordlist.cols[i])] += [str(p)]
    return matrix

print("# Body Parts")
wl = Wordlist("pano-body-parts.tsv")
our_sample = len(wl.get_etymdict(ref="bodyid"))

dm, ds, qm, qs = get_deltaq(wl, "bodyid")
dms, dss, qms, qss = [], [], [], []

for i in progressbar(range(100)):
    a, b, c, d = get_deltaq(wl, "bodyid", shuffle=True)
    dms += [a]
    dss += [b]
    qms += [c]
    qss += [d]
table = [[dm, ds, qm, qs],
        [
            statistics.mean(dms),
            statistics.mean(dss),
            statistics.mean(qms),
            statistics.mean(qss)]]
print(tabulate(
    table,
    floatfmt=".4f",
    headers=["Delta", "Delta STD", "Q-Res", "Q-Res STD"],
        ))
print("")
print("# With samples")
wl = Wordlist("pano-auto.tsv")

obsa, supa, cona, rata = [], [], [], []
obsb, supb, conb, ratb = [], [], [], []

for i in progressbar(range(100)):
    a, b, c, d = get_deltaq(wl, "autocogid", sample=our_sample)
    obsa += [a]
    supa += [b]
    cona += [c]
    rata += [d]
    a, b, c, d = get_deltaq(wl, "autocogid", shuffle=True, sample=our_sample)
    obsb += [a]
    supb += [b]
    conb += [c]
    ratb += [d]

table = [
        [
            statistics.mean(obsa),
            statistics.mean(supa),
            statistics.mean(cona),
            statistics.mean(rata)
            ],    
        [
            statistics.mean(obsb),
            statistics.mean(supb),
            statistics.mean(conb),
            statistics.mean(ratb)

            ]
        ]
print(tabulate(
    table,
    floatfmt=".4f",
    headers=["Delta", "Delta STD", "Q-Res", "Q-Res STD"],
        ))
print("")
print("# All data")


wl = Wordlist("pano-auto.tsv")
observed, supported, conflicted, ratio = get_deltaq(wl, "autocogid")
ob_s, sup_s, con_s, rat_s = [], [], [], []

for i in progressbar(range(100)):
    a, b, c, d = get_deltaq(wl, "autocogid", shuffle=True)
    ob_s += [a]
    sup_s += [b]
    con_s += [c]
    rat_s += [d]
table = [[observed, supported, conflicted, ratio],
        [
            statistics.mean(ob_s),
            statistics.mean(sup_s),
            statistics.mean(con_s),
            statistics.mean(rat_s)]]
print(tabulate(
    table,
    floatfmt=".4f",
    headers=["Delta", "Delta STD", "Q-Res", "Q-Res STD"],
        ))


