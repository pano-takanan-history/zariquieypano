wordlist:
	edictor wordlist --name=pano-full --data=../cldf/cldf-metadata.json --addon="cognacy:cogid" 

beast-full:
	python -c "from lingpy import *; from lingpy.convert.strings import write_nexus; wl = Wordlist('pano-full.tsv'); write_nexus(wl, mode='beast', filename='pano-full.nex', ref='cogid')"

splitstree:
	python -c "from lingpy import *; from lingpy.convert.strings import write_nexus; wl = Wordlist('pano-full.tsv'); write_nexus(wl, mode='splitstree', filename='pano-full_splitstree.nex', ref='cogid')"
