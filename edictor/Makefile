bp-wordlist:
	edictor wordlist --name=pano-body-parts --data=../cldf/cldf-metadata.json --addon="motivation_structure:morphemes,partial_cognacy:cogs,cognacy:cogid" --preprocessing=preprocessing.py

bp-nexus: 
	python -c "from lingpy import *; from lingpy.convert.strings import write_nexus; wl = Wordlist('pano-body-parts.tsv'); write_nexus(wl, mode='splitstree', filename='pano-body-parts.nex', ref='bodyid')"

beast-wordlist:
	edictor wordlist --name=pano-full --data=../cldf/cldf-metadata.json --addon="cognacy:cogid" 

auto-wordlist:
	edictor wordlist --name=pano-auto --data=../cldf/cldf-metadata.json --preprocessing=fullproc.py

beast-full:
	python -c "from lingpy import *; from lingpy.convert.strings import write_nexus; wl = Wordlist('pano-full.tsv'); write_nexus(wl, mode='full', filename='../analysis/dated_phylogeny/beast/pano-full.nex', ref='cogid')"

splitstree:
	python -c "from lingpy import *; from lingpy.convert.strings import write_nexus; wl = Wordlist('pano-full.tsv'); write_nexus(wl, mode='splitstree', filename='../analysis/dated_phylogeny/plots/pano-full_splitstree.nex', ref='cogid')"


