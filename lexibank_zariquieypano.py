from pathlib import Path
import dataclasses
import lingpy.basictypes
from lingpy import Wordlist
from clldutils.misc import slug
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank import Concept, Language, Lexeme
from edictor.wordlist import fetch_wordlist


@dataclasses.dataclass
class CustomConcept(Concept):
    Spanish_Gloss: Optional[str] = None


@dataclasses.dataclass
class CustomLexeme(Lexeme):
    Partial_Cognacy: Optional[str] = None
    Alignment: Optional[str] = None
    Morphemes: Optional[str] = None
    Note: Optional[str] = None


@dataclasses.dataclass
class CustomLanguage(Language):
    SubGroup: Optional[str] = None
    SourceDate: Optional[str] = None
    Source: Optional[str] = None


def desegment(sequence):
    out = []
    for tok in sequence:
        out += tok.split('.')
    return out


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "zariquieypano"
    lexeme_class = CustomLexeme
    concept_class = CustomConcept
    language_class = CustomLanguage

    def cmd_download(self, _):
        """Download the most recent data from Edictor."""
        print("updating ...")
        with open(self.raw_dir.joinpath("raw.tsv"), "w", encoding="utf-8") as f:
            f.write(
                fetch_wordlist(
                    "zariquieypano",
                    columns=[
                        "CONCEPT",
                        "DOCULECT",
                        "FORM",
                        "VALUE",
                        "TOKENS",
                        "COGID",
                        "COGIDS",
                        "ALIGNMENT",
                        "MORPHEMES",
                        "NOTE"
                    ],
                    base_url='http://lingulist.de/pth/',
                    script_url='get_data.py'
                )
            )

    def cmd_makecldf(self, args):
        """
        Convert the raw data to a CLDF dataset.
        """
        wl = Wordlist(str(self.raw_dir / "pano.tsv"))
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

        sources = {}
        for language in self.languages:
            args.writer.add_language(**language)
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
                    Alignment=wl[idx, 'alignment'],
                    Morphemes=str(lingpy.basictypes.strings(wl[idx, "morphemes"])) or "?",
                    Note=wl[idx, 'note'],
                    Source=sources[wl[idx, "doculect"]]
                    )
