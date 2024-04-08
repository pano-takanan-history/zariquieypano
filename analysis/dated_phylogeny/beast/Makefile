
XMLS = $(wildcard pano_*.xml)
LOGS = $(patsubst %.xml, %.run, $(XMLS))
TXTS = $(patsubst %.xml, %.hpd.txt, $(XMLS))

all: $(XMLS) $(LOGS) $(TXTS)

# run BEAST
%.run: %.xml
	beast2 -beagle_SSE $< | tee $@

# summarise
%.hpd.txt: %.run
	loganalyser $(patsubst %.run,%.log, $<) > $@

.PHONY: checkhpd
checkhpd:
	@awk '{printf "%-20s\t%-33s\t%-8s\t[%s,%s]\t%-8s\n", FILENAME, $$1, $$5, $$6, $$7, $$9}' *.hpd.txt | sort -k 5 -g -r | awk '($$5 < 200)'

## clean: removes auto-generated files
.PHONY: clean
clean:
	rm *.log *.trees *.run *.txt

# debugging helper to show target. Run make print-VARNAME
print-%  : ; @echo $* = $($*)

