from pylento import Lento
from lingpy import Wordlist
import random
from tabulate import tabulate
from tqdm import tqdm as progressbar
import statistics


def get_lento(wordlist, ref, shuffle=False):
    matrix = get_matrix(wordlist, ref, shuffle=shuffle)
    lnt = Lento(matrix)
    summary = lnt.summary()
    return (
            summary["observed"],
            summary["supported"],
            summary["conflicted"]
            )

def get_matrix(wordlist, ref, shuffle=False):
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


wl = Wordlist("pano-auto.tsv")
observed, supported, conflicted = get_lento(wl, "autocogid")
ob_s, sup_s, con_s = [], [], []

for i in progressbar(range(10)):
    a, b, c = get_lento(wl, "autocogid", shuffle=True)
    ob_s += [a]
    sup_s += [b]
    con_s += [c]
table = [[observed, supported, conflicted],
        [
            statistics.mean(ob_s),
            statistics.mean(sup_s),
            statistics.mean(con_s)]]
print(tabulate(table))


print("---")
wl = Wordlist("pano-body-parts.tsv")

observed, supported, conflicted = get_lento(wl, "bodyid")
ob_s, sup_s, con_s = [], [], []

for i in progressbar(range(100)):
    a, b, c = get_lento(wl, "bodyid", shuffle=True)
    ob_s += [a]
    sup_s += [b]
    con_s += [c]
table = [[observed, supported, conflicted],
        [
            statistics.mean(ob_s),
            statistics.mean(sup_s),
            statistics.mean(con_s)]]
print(tabulate(table))
print("")

