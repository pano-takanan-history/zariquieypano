
JOBS = $(wildcard ../pano_*.xml)
XMLS = $(notdir $(JOBS))
LOGS = $(patsubst %.xml, %.run, $(XMLS))
TXTS = $(patsubst %.xml, %.txt, $(XMLS))

all: $(XMLS) $(LOGS) $(TXTS) results.txt

# Step 1: patch XMLS to run nested sampling
%.xml: ../%.xml
	sed 's|\<run id="mcmc" spec="MCMC" chainLength="20000000" storeEvery="10000"\>|\<run id="mcmc" spec="beast.gss.MultiThreadedNS" threads="4" chainLength="20000000" particleCount="1" subChainLength="100000" epsilon="1e-12"\>|g' $< > $@

# Step 2: run pathsampling (may want to do this on cluster)
%.run: %.xml
	beast276 -beagle_SSE $< | tee $@

# summarise
%.txt: %.run
	/Applications/beast2/beast276/bin/applauncher NSLogAnalyser -N 4 -noposterior -log $(wildcard *$(patsubst %.run,%.log, $<)) > $@ 2>&1

results.txt: $(TXTS)
	python print_marginal.py $^ | tee $@

## clean: removes auto-generated files
.PHONY: clean
clean:
	rm *.log *.trees *.run *.txt

# debugging helper to show target. Run make print-VARNAME
print-%  : ; @echo $* = $($*)

