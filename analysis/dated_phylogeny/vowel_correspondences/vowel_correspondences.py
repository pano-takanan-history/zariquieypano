from pathlib import Path
from lingpy import Wordlist
from lingreg.lingreg import prepare_alignment
from lingrex import CoPaR


wl = Wordlist.from_cldf(
    Path("../../cldf", "cldf-metadata.json").as_posix(),
    columns=(
        "form",
        "segments",
        "cognacy",
        "language_id",
        "concept_name",
        "concept_concepticon_id",
        "concept_concepticon_gloss",
        "language_glottocode"),
    namespace=(
        ("cognacy", "cogid"),
        ("segments", "tokens"),
        ("language_id", "doculect"),
        ("language_glottocode", "glottocode"),
        ("concept_name", "concept"),
        ("concept_concepticon_gloss", "concepticon_gloss"),
        ("concept_concepticon_id", "concepticon_id"),
        )
)

# wl.add_entries("old_alignments", "alignment", lambda x: x)

# for idx in wl:
#     wl[idx, "alignment"] = wl[idx, "tokens"]

aligned_data = prepare_alignment(wl, ref="cogid", function="coregaps")
copar = CoPaR(aligned_data, ref="cogid", transcription="form")
copar.get_sites()
copar.cluster_sites()
copar.sites_to_pattern()
copar.add_patterns()

for (cogid, _), val in copar.patterns.items():
    # print(val)
    for v in val:
        if v[1] == "V":
            # print(v)
            # v[0] is ?
            # v[1] is C or V
            # v[2] is the list of items in correspondences

            print(v[2])

            # this gives the cogid and some other number of the respectie pattern
            # possibly the position! within the alignment
            print(copar.clusters[v[1:]])

            # This gives me the full entries, but without structure
            # print(copar.msa["cogid"][cogid])
            # print(copar.msa["cogid"][cogid]["alignment"])

copar.write_patterns("patterns.tsv")
