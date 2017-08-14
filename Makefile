include Makefile.in

REQ = 'Requirements -\n'
REQ += '\033[92m'
REQ += 'pandoc'
REQ += '\033[0m'
REQ += 'to convert Markdown to TeX/html\n\033[0m'
REQ += '\033[92m'
REQ += 'XeLaTeX'
REQ += '\033[0m'
REQ += 'to convert TeX to PDF\n\033[0m'
REQ += '\033[92m'
REQ += 'pyYAML(via pip)'
REQ += '\033[0m'
REQ += 'to convert yaml to json waveform file \n\033[0m'
REQ += '\033[92m'
REQ += 'WAVEDROM+PhantomJS(via npm)'
REQ += '\033[0m'
REQ += 'to convert JSON to waveform png\n\033[0m'
REQ += '\033[92m'
REQ += 'rsvg-convert(via librsvg)'
REQ += '\033[0m'
REQ += 'to convert SVG to PNG\n\033[0m'

CSV:= $(shell cd $(DATADIR); ls *.csv)
TABLES:= $(CSV:%.csv=$(TARGETDIR)/%.table.md)

WAVEYAML:= $(shell cd $(DATADIR)/$(WAVEDIR); ls *.yaml)
PYWAVEOPTS:= -c
PYWAVEOPTS += 'import sys, yaml, json, io;\
						sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8"); \
						json.dump(yaml.load(sys.stdin), sys.stdout, indent=4)'

WAVEJSON:= $(WAVEYAML:%.yaml=$(TARGETDIR)/%.wavejson)
WAVEPNG:= $(WAVEYAML:%.yaml=$(IMAGEDIR)/$(WAVEDIR)/%.png)

BITYAML:= $(shell cd $(DATADIR)/$(BITDIR); ls *.yaml)
BITJSON:= $(BITYAML:%.yaml=$(TARGETDIR)/%.bitjson)
BITPNG:=  $(BITYAML:%.yaml=$(IMAGEDIR)/$(BITDIR)/%.png)
BIT16YAML:= $(shell cd $(DATADIR)/$(BIT16DIR); ls *.yaml)
BIT16JSON:= $(BIT16YAML:%.yaml=$(TARGETDIR)/%.bit16json)
BIT16PNG:=  $(BIT16YAML:%.yaml=$(IMAGEDIR)/$(BIT16DIR)/%.png)
# rsvg-convert alpha.svg --format=png --output=sample_rsvg.png

FILTERED= $(INPUT:%.md=$(TARGETDIR)/%.md)
HTML:=$(TARGETDIR)/$(TARGET).html
DOCX:=$(TARGETDIR)/$(TARGET).docx

MARKDOWN = $(shell ls $(MDDIR)/*.md)

.PHONY: docx html filtered pdf tex merge clean linking

all: html

help:
	@echo $(REQ)"\033[0m"

docx: $(DOCX)
$(DOCX): $(FILTERED)
	$(PANDOC) $(PANFLAGS) --reference-docx=$(REFERENCE) $(FILTERED) -o $(DOCX); \
	$(PYTHON) $(DOCXPWRTR) -I $(MDDIR)/$(INPUT) -O $(DOCX)

html: $(HTML)
$(HTML): $(TARGETDIR)/$(INPUT)
	$(PANDOC) $(PANFLAGS) --self-contained -thtml5 --template=$(MISC)/github.html \
		$(FILTERED) -o $(HTML)

pdf: $(TARGETDIR)/$(IMAGEDIR) $(TARGETDIR)/$(IMAGINEDIR) $(TARGETDIR)/$(TARGET).tex
	cd $(TARGETDIR);\
	xelatex --no-pdf $(TARGET).tex; \
	xelatex $(TARGET).tex


linking: $(TARGETDIR)/$(IMAGEDIR) $(TARGETDIR)/$(IMAGINEDIR)
$(TARGETDIR)/$(IMAGEDIR):
	rm -f $(TARGETDIR)/$(IMAGEDIR); \
	cd $(TARGETDIR);\
	ln -s ../$(IMAGEDIR)

$(TARGETDIR)/$(IMAGINEDIR):
	rm -f $(TARGETDIR)/$(IMAGINEDIR); \
	cd $(TARGETDIR);\
	ln -s ../$(IMAGINEDIR)

tex: $(TARGETDIR)/$(TARGET).tex
$(TARGETDIR)/$(TARGET).tex: $(FILTERED)
	$(PANDOC) $(PANFLAGS) $(TEXFLAGS) $(TEXFONTFLAGS) \
		$(FILTERED) -o $(TARGETDIR)/$(TARGET).tex

# merge: filtered $(TARGETDIR)/$(TARGET).md
# $(TARGETDIR)/$(TARGET).md: $(FILTERED)
# 	cat $(FILTERED) > $(TARGETDIR)/$(TARGET).md

filtered: $(FILTERED)
$(FILTERED): $(MDDIR)/$(INPUT) $(MARKDOWN) $(WAVEPNG) $(BITPNG) $(BIT16PNG) $(MFILTDIR) $(TABLES)
ifneq ($(OS),Windows_NT)
	$(GPP) $(GPPFLAGS) $< | $(PYTHON) $(FILTER) --mode tex --out $@
else
	$(GPP) $(GPPFLAGS) $< > $@
endif

tables: $(TABLES)
	echo $(TABLES)
$(TARGETDIR)/%.table.md: $(DATADIR)/%.csv
	$(CSV2TABLE) $< $@

wavedrom: $(WAVEDIR) $(WAVEPNG)
$(IMAGEDIR)/$(WAVEDIR)/%.png: $(TARGETDIR)/%.wavejson
ifneq ($(OS),Windows_NT)
	phantomjs $(WAVEDROM) -i $< -p $@
else
	cp $(MISC)/$(IMAGEDIR)/dummy.png $@
endif

bitfield: $(BITDIR) $(BITPNG) $(BIT16PNG)
$(IMAGEDIR)/$(BITDIR)/%.png: $(TARGETDIR)/%.bitjson
	$(BITFIELD) --input $< --vspace 80 --hspace 640 --lanes 1 --bits 8 \
	--fontfamily "source code pro" --fontsize 16 --fontweight normal> $<.svg
ifneq ($(OS),Windows_NT)
	$(RSVG) $<.svg --format=png --output=$@
else
	$(RSVG) $<.svg --output $@
endif

$(IMAGEDIR)/$(BIT16DIR)/%.png: $(TARGETDIR)/%.bit16json
	$(BITFIELD) --input $< --vspace 80 --hspace 640 --lanes 1 --bits 16 \
	--fontfamily "source code pro" --fontsize 16 --fontweight normal> $<.svg
ifneq ($(OS),Windows_NT)
	$(RSVG) $<.svg --format=png --output=$@
else
	$(RSVG) $<.svg --output $@
endif

yaml2json: $(WAVEDIR) $(BITDIR) $(WAVEJSON) $(BITJSON) $(BIT16JSON)
$(TARGETDIR)/%.wavejson: $(DATADIR)/$(WAVEDIR)/%.yaml
	if [ ! -e $(IMAGEDIR)/$(WAVEDIR) ]; then mkdir -p $(IMAGEDIR)/$(WAVEDIR); fi
	$(PYTHON) $(PYWAVEOPTS) < $< > $@

$(TARGETDIR)/%.bitjson: $(DATADIR)/$(BITDIR)/%.yaml
	if [ ! -e $(IMAGEDIR)/$(BITDIR) ]; then mkdir -p $(IMAGEDIR)/$(BITDIR); fi
	$(PYTHON) $(PYWAVEOPTS) < $< > $@

$(TARGETDIR)/%.bit16json: $(DATADIR)/$(BIT16DIR)/%.yaml
	if [ ! -e $(IMAGEDIR)/$(BIT16DIR) ]; then mkdir -p $(IMAGEDIR)/$(BIT16DIR); fi
	$(PYTHON) $(PYWAVEOPTS) < $< > $@

init:
	mkdir -p $(PREFIX)/
	cp Makefile.txt $(PREFIX)/Makefile
	mkdir -p $(PREFIX)/$(TARGETDIR)
	mkdir -p $(PREFIX)/$(DATADIR)
	mkdir -p $(PREFIX)/$(MDDIR)
	mkdir -p $(PREFIX)/$(IMAGEDIR)
	mkdir -p $(PREFIX)/$(IMAGEDIR)/$(WAVEDIR)
	mkdir -p $(PREFIX)/$(IMAGEDIR)/$(BITDIR)
	mkdir -p $(PREFIX)/$(IMAGEDIR)/$(BIT16DIR)
	mkdir -p $(PREFIX)/$(IMAGEDIR)/$(MFILTDIR)

$(TARGETDIR):
	mkdir -p $(TARGETDIR)
$(DATADIR):
	mkdir -p $(DATADIR)
$(MDDIR):
	mkdir -p $(MDDIR)
$(IMAGEDIR):
	mkdir -p $(IMAGEDIR)
$(WAVEDIR):
	mkdir -p $(IMAGEDIR)/$(WAVEDIR)
$(BITDIR):
	mkdir -p $(IMAGEDIR)/$(BITDIR)
$(BIT16DIR):
	mkdir -p $(IMAGEDIR)/$(BIT16DIR)
$(MFILTDIR):
	mkdir -p $(IMAGEDIR)/$(MFILTDIR)

clean: $(TARGETDIR)
	rm -rf $(TARGETDIR)/*
	rm -rf $(IMAGEDIR)/$(WAVEDIR)/
	rm -rf $(IMAGEDIR)/$(BITDIR)/
	rm -rf $(IMAGEDIR)/$(BIT16DIR)/
	rm -rf $(IMAGEDIR)/$(MFILTDIR)/
