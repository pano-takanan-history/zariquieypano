from collections import defaultdict

from pathlib import Path
from pylexibank.dataset import Dataset as BaseDataset 
from pylexibank import Language, FormSpec, Concept
from pylexibank import progressbar

from clldutils.misc import slug
import attr
from pyedictor import fetch
from pylexibank import Lexeme
import lingpy

LANGUAGES = [
        "Arara",
        "Amawaka",
        "Chakobo",
        "Chaninawa",
        "Iskonawa",
        "Kakataibo",
        "Kanamari",
        "Kapanawa",
        "Kashinawa_B",
        "Kashinawa_P",
        "Katukina",
        "Kaxarari",
        "Marinawa",
        "Marubo",
        "Mastanawa",
        "Matis",
        "Matses",
        "Nawa",
        "Nukini",
        "Pakawara",
        "Poyanawa",
        "Shanenawa",
        "Sharanawa",
        "Shipibo_Konibo",
        "Yaminawa",
        "Yawanawa",
        ]

@attr.s
class CustomLanguage(Language):
    SubGroup = attr.ib(default=None)
    Family = attr.ib(default='Pano')
    Note = attr.ib(default=None)
    SourceDate = attr.ib(default=None)
    Source = attr.ib(default=None)


@attr.s
class CustomConcept(Concept):
    Spanish_Gloss = attr.ib(default=None)


@attr.s
class CustomLexeme(Lexeme):
    Partial_Cognacy = attr.ib(default=None)
    Motivation_Structure = attr.ib(default=None)


def desegment(tokens):
    out = []
    for t in tokens:
        if '.' in t:
            out += t.split('.')
        else:
            out += [t]
    return out


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "zariquieypano"
    language_class = CustomLanguage
    lexeme_class = CustomLexeme
    concept_class = CustomConcept
    form_spec = FormSpec(
            missing_data=("–", "-")
            )
    def cmd_download(self, args):
        args.log.info('updating ...')
        with open(self.raw_dir.joinpath("pano.tsv"), "w",
                encoding="utf-8") as f:
            f.write(fetch("pano", base_url="https://digling.org/edictor",
                languages=LANGUAGES))

    def cmd_makecldf(self, args):
        """
        Convert the raw data to a CLDF dataset.
        """
        wl = lingpy.Wordlist(str(self.raw_dir / "pano.tsv"))
        concepts = {}
        for concept in self.concepts:
            idx = concept["NUMBER"] + "_" + slug(concept["ENGLISH"])
            args.writer.add_concept(
                    ID=idx,
                    Name=concept["ENGLISH"],
                    Spanish_Gloss=concept["SPANISH"],
                    Concepticon_ID=concept["CONCEPTICON_ID"],
                    Concepticon_Gloss=concept["CONCEPTICON_GLOSS"]
                    )
            concepts[concept["ENGLISH"]] = idx
    
        for language in self.languages:
            if language["ID"] in LANGUAGES:
                args.writer.add_language(**language)
        sources = {}
        for language in self.languages:
            sources[language["ID"]] = language["Source"]
        args.writer.add_sources()

        for idx in wl:
            args.writer.add_form_with_segments(
                    Parameter_ID=concepts[wl[idx, "concept"]],
                    Language_ID=wl[idx, "doculect"],
                    Value=wl[idx, "value"],
                    Form=wl[idx, "form"],
                    Segments=desegment(wl[idx, "tokens"]),
                    Cognacy=wl[idx, 'cogid'],
                    Partial_Cognacy=str(lingpy.basictypes.ints(wl[idx, "cogids"])) or 0,
                    Motivation_Structure=str(lingpy.basictypes.strings(wl[idx, "morphemes"])) or "?",
                    Source=sources[wl[idx, "doculect"]]
                    )



