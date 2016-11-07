include Makefile.in

REQ = 'Requirements -\n'
REQ += '\033[92m'
REQ += 'pyYAML(via pip)'
REQ += '\033[0m'
REQ += 'to convert yaml to json waveform file \n\033[0m'
REQ += '\033[92m'
REQ += 'WAVEDROM+PhantomJS(via npm)'
REQ += '\033[0m'
REQ += 'to convert JSON to waveform png\n'
REQ += '\033[92m'
REQ += 'rsvg-convert(via librsvg)'
REQ += '\033[0m'
REQ += 'to convert SVG to PNG'
REQ += '\033[0m'

MDDIR:= markdown
DATADIR:= data
TARGETDIR:= Out
IMAGEDIR:= images
WAVEDIR:= images/waves
BITFIELD:= images/bitfields

INPUT:= TITLE.md
TARGET = TARGET

CSV:= $(shell cd $(DATADIR); ls *.csv)
TABLES:= $(CSV:%.csv=$(TARGETDIR)/%.tmd)

WAVEYAML:= $(shell cd $(DATADIR); ls *.yaml)
PYWAVEOPTS:= -c
PYWAVEOPTS += 'import sys, yaml, json; \
							json.dump(yaml.load(sys.stdin), sys.stdout, indent=4)'
WAVEJSON:= $(WAVEYAML:%.yaml=$(TARGETDIR)/%.json)
WAVEPNG:= $(WAVEYAML:%.yaml=$(WAVEDIR)/%.png)

FILTERED= $(INPUT:%.md=$(TARGETDIR)/%.fmd)
HTML:=$(TARGETDIR)/$(TARGET).html
DOCX:=$(TARGETDIR)/$(TARGET).docx

PANFLAGS += --toc
PANFLAGS += --listings
PANFLAGS += --number-sections --highlight-style=pygments
PANFLAGS += -M localfontdir=$(FONTDIR)
PANFLAGS += -M css=$(MISC)/github_css/github.css
PANFLAGS += -M short-hash=`git rev-parse --short HEAD`
PANFLAGS += -M tables=true

MARKDOWN = $(shell ls $(MDDIR)/*.md)

.PHONY: docx html filtered tables pdf tex merge clean linking

all: html

help:
	@echo $(REQ)"\033[0m"

docx: $(DOCX)
$(DOCX): $(HTML)
	$(PANDOC) --reference-docx=$(REFERENCE) $(HTML) -o $(DOCX); \
	$(PYTHON) $(DOCXPWRTR) -I $(MDDIR)/$(INPUT) -O $(DOCX)

html: $(HTML)
$(HTML): $(TARGETDIR)/$(TARGET).md
	$(PANDOC) $(PANFLAGS) --self-contained -thtml5 --template=$(MISC)/github.html \
		$(FILTERED) -o $(HTML)

pdf: $(TARGETDIR)/$(IMAGEDIR) $(TARGETDIR)/$(TARGET).tex
	cd $(TARGETDIR);\
	xelatex --no-pdf $(TARGET).tex; \
	xelatex $(TARGET).tex

linking: $(TARGETDIR)/$(IMAGEDIR)
$(TARGETDIR)/$(IMAGEDIR):
	rm -f $(TARGETDIR)/$(IMAGEDIR); \
	cd $(TARGETDIR);\
	ln -s ../$(IMAGEDIR)

tex: $(TARGETDIR)/$(TARGET).tex
$(TARGETDIR)/$(TARGET).tex: $(TARGETDIR)/$(TARGET).md
	$(PANDOC) $(PANFLAGS) --template=$(MISC)/CJK_xelatex.tex --latex-engine=xelatex \
		$(TARGETDIR)/$(TARGET).md -o $(TARGETDIR)/$(TARGET).tex

merge: $(TARGETDIR)/$(TARGET).md
$(TARGETDIR)/$(TARGET).md: $(FILTERED)
	cat $(FILTERED) > $(TARGETDIR)/$(TARGET).md

filtered: $(FILTERED)
$(FILTERED): $(MDDIR)/$(INPUT) $(MARKDOWN) $(TABLES) $(WAVEPNG)
	cat $< | $(PYTHON) $(FILTER) --out $@

tables: $(TABLES)
$(TARGETDIR)/%.tmd: $(DATADIR)/%.csv
	$(PYTHON) $(CSV2TABLE) --file $< --out $@ --delimiter ','

wavedrom: $(WAVEPNG)
$(WAVEDIR)/%.png: $(TARGETDIR)/%.json
	phantomjs $(WAVEDROM) -i $< -p $@

yaml2json: $(WAVEJSON)
$(TARGETDIR)/%.json: $(DATADIR)/%.yaml
	$(PYTHON) $(PYWAVEOPTS) < $< > $@

$(TARGETDIR):
	mkdir -p $(TARGETDIR)
$(DATADIR):
	mkdir -p $(DATADIR)
$(MDDIR):
	mkdir -p $(MDDIR)
$(IMAGEDIR):
	mkdir -p $(IMAGEDIR)
$(WAVEDIR):
	mkdir -p $(WAVEDIR)

clean: $(TARGETDIR)
	rm -rf $(TARGETDIR)/* $(WAVEDIR)/
