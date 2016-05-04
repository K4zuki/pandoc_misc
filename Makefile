include Makefile.win
# include Makefile.in

MDDIR:= markdown
DATADIR:= data
TARGETDIR:= Out

INPUT:= source.md
OUTPUT:= $(shell basename $(INPUT) .md)
CSV:= $(shell cd $(DATADIR); ls *.csv)
TABLES:= $(CSV:%.csv=%.tmd)
FILTERED= $(INPUT:%.md=$(TARGETDIR)/%.fmd)


.PHONY: docx html filtered tables clean

all: docx

docx: $(TARGETDIR)/$(OUTPUT).html
	$(PANDOC) --reference-docx=$(REFERENCE) $(TARGETDIR)/$(OUTPUT).html -o $(TARGETDIR)/$(OUTPUT).docx; \
	$(PYTHON) $(DOCXPWRTR) -I $(MDDIR)/$(INPUT) -O $(TARGETDIR)/$(OUTPUT).docx

html: filtered $(TARGETDIR)/$(OUTPUT).html

$(TARGETDIR)/$(OUTPUT).html: $(FILTERED)
	$(PANDOC) $(PANFLAGS) --self-contained -thtml5 --template=$(MISC)/github.html \
		$(FILTERED) -o $(TARGETDIR)/$(OUTPUT).html

filtered: tables $(FILTERED)
$(FILTERED): $(MDDIR)/$(INPUT)
	cat $< | $(PYTHON) $(FILTER) --out $@

tables: $(TABLES)
$(TABLES): $(CSV:%=$(DATADIR)/%)
	$(PYTHON) $(CSV2TABLE) --file $< --out $(TARGETDIR)/$@ --delimiter ','

clean:
	rm -rf $(TARGETDIR)
	mkdir -p $(TARGETDIR)
