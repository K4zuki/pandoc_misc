include Makefile.win
# include Makefile.in

MDDIR:= markdown
DATADIR:= data
TARGETDIR:= Out

INPUT:= source.md
OUTPUT:= $(shell basename $(INPUT) .md)
CSV:= $(shell cd $(DATADIR); ls *.csv)
TABLES:= $(CSV:%.csv=$(TARGETDIR)/%.tmd)
FILTERED= $(INPUT:%.md=$(TARGETDIR)/%.fmd)
HTML:=$(TARGETDIR)/$(OUTPUT).html
DOCX:=$(TARGETDIR)/$(OUTPUT).docx

.PHONY: docx html filtered tables clean

all: docx

docx: $(DOCX)
$(DOCX): $(HTML)
	$(PANDOC) --reference-docx=$(REFERENCE) $(TARGETDIR)/$(OUTPUT).html -o $(TARGETDIR)/$(OUTPUT).docx; \
	$(PYTHON) $(DOCXPWRTR) -I $(MDDIR)/$(INPUT) -O $(DOCX)

html: $(HTML)

$(HTML): $(TABLES) $(FILTERED)
	$(PANDOC) $(PANFLAGS) --self-contained -thtml5 --template=$(MISC)/github.html \
		$(FILTERED) -o $(TARGETDIR)/$(OUTPUT).html

filtered: tables $(FILTERED)
$(FILTERED): $(MDDIR)/$(INPUT)
	cat $< | $(PYTHON) $(FILTER) --out $@

tables: $(TABLES)
$(TABLES): $(CSV:%=$(DATADIR)/%)
	$(PYTHON) $(CSV2TABLE) --file $< --out $@ --delimiter ','

clean:
	rm -rf $(TARGETDIR)
	mkdir -p $(TARGETDIR)
