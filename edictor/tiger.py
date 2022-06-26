from pylotiger import get_set_partitions, corrected_pas
from lingpy import *
from collections import defaultdict
from statistics import mean, stdev
import itertools
from tabulate import tabulate
import random
from tqdm import tqdm as progressbar


def get_tiger(wordlist, shuffle=False, sample=None, ref="cogid"):
    """
    Compute TIGER scores for a wordlist.
    """
    def get_mapper(languages):
        mapper = {}
        idxs = list(range(len(languages)))
        random.shuffle(idxs)
        for i, idx in enumerate(idxs):
            mapper[languages[i]] = languages[idx]
        return mapper

    # make characters
    characters = {concept: defaultdict(list) for concept in wordlist.rows}
    mapper = {}
    for concept in wordlist.rows:
        for idx in wordlist.get_list(row=concept, flat=True):
            if shuffle:
                mapper = get_mapper(wordlist.cols)
            characters[concept][
                    mapper.get(
                        wordlist[idx, "doculect"], 
                        wordlist[idx, "doculect"]
                        )] += [wl[idx, ref]]

    if sample:
        selected = random.sample(list(characters), sample)
        characters = {concept: characters[concept] for concept in selected}
    
    set_partitions = get_set_partitions(characters, wordlist.cols)

    scores, scored = [], {char: [] for char in characters}
    for charA, charB in itertools.combinations(characters, r=2):
        score = corrected_pas(set_partitions[charA], set_partitions[charB])
        if score:
            scores += [score]
            scored[charA] += [score]
    return scored, mean(scores), stdev(scores)

sig = 100

wl = Wordlist("pano-body-parts.tsv")
scored, mean_score, stdev_score = get_tiger(wl, ref="bodyid")
all_scores, all_stdevs, hits = [], [], 0
for i in progressbar(range(sig), desc="run shuffle"):
    a, b, c = get_tiger(wl, ref="bodyid", shuffle=True)
    all_scores += [b]
    all_stdevs += [c]
    if b >= mean_score:
        hits += 1
print("# Body Suffixes")
print(tabulate([
    ["Attested", "{0:.2f}".format(mean_score), "{0:.2f}".format(stdev_score)],
    ["Random", "{0:.2f}".format(mean(all_scores)),
        "{0:.2f}".format(mean(all_stdevs))],
    ["Significance", "{0}".format(hits), "{0:.2f}".format(hits/sig)]]))
bpchars = wl.height

wl = Wordlist("pano-auto.tsv")
scores, stdevs = [], []
for i in progressbar(range(sig), desc="run sample"):
    scored, mean_score, stdev_score = get_tiger(wl, ref="autocogid",
            sample=bpchars)
    scores += [mean_score]
    stdevs += [stdev_score]

all_scores, all_stdevs, hits = [], [], 0
for i in progressbar(range(sig), desc="run shuffle and sample"):
    a, b, c = get_tiger(wl, ref="autocogid", shuffle=True, sample=bpchars)
    all_scores += [b]
    all_stdevs += [c]
    if b >= mean_score:
        hits += 1
print("\n# LexStat Cognates (Sampled)")
print(tabulate([
    ["Attested", "{0:.2f}".format(mean(scores)), "{0:.2f}".format(mean(stdevs))],
    ["Random", "{0:.2f}".format(mean(all_scores)),
        "{0:.2f}".format(mean(all_stdevs))],
    ["Significance", "{0}".format(hits), "{0:.2f}".format(hits/sig)]]))

wl = Wordlist("pano-auto.tsv")
scored, mean_score, stdev_score = get_tiger(wl, ref="autocogid")

all_scores, all_stdevs, hits = [], [], 0
for i in progressbar(range(sig), desc="run shuffle"):
    a, b, c = get_tiger(wl, ref="autocogid", shuffle=True)
    all_scores += [b]
    all_stdevs += [c]
    if b >= mean_score:
        hits += 1
print("\n# LexStat Cognates")
print(tabulate([
    ["Attested", "{0:.2f}".format(mean_score), "{0:.2f}".format(stdev_score)],
    ["Random", "{0:.2f}".format(mean(all_scores)),
        "{0:.2f}".format(mean(all_stdevs))],
    ["Significance", "{0}".format(hits), "{0:.2f}".format(hits/sig)]]))




