bp-wordlist:
	edictor wordlist --name=pano-body-parts --data=../cldf/cldf-metadata.json --addon="motivation_structure:morphemes,cognacy:cogid" --preprocessing=preprocessing.py

bp-nexus: 
	python -c "from lingpy import *; from lingpy.convert.strings import write_nexus; wl = Wordlist('pano-body-parts.tsv'); write_nexus(wl, mode='splitstree', filename='pano-body-parts.nex', ref='bodyid')"
