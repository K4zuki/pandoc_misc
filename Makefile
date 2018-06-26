ifeq ($(OS),Windows_NT)
HOME = C:/Users/$(USERNAME)
endif
PANSTYLES= /var
MISC= $(PANSTYLES)/pandoc_misc

ifeq ($(PROJECT),)
include $(MISC)/Makefile.in
endif

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

FILTERED:= $(INPUT:%.md=$(TARGETDIR)/%.md)
HTML:=$(TARGETDIR)/$(TARGET).html
DOCX:=$(TARGETDIR)/$(TARGET).docx

MARKDOWN = $(shell ls $(MDDIR)/*.md)

.PHONY: docx html filtered pdf tex merge clean linking

all: html

help:
	@echo $(REQ)"\033[0m"

docx: $(DOCX)
$(DOCX): $(FILTERED)
	$(PANDOC) $(PANFLAGS) $(PANDOCXFFLAGS) $(FILTERED) -o $(DOCX); \
	$(PYTHON) $(DOCXPWRTR) -I $(MDDIR)/$(INPUT) -O $(DOCX)

html: $(HTML)
$(HTML): $(FILTERED) $(TARGETDIR)/$(INPUT) $(MDDIR)/$(CONFIG)
	$(PANDOC) $(PANFLAGS) $(PANHTMLFLAGS) $(FILTERED) -o $(HTML)

pdf: $(TARGETDIR)/$(IMAGEDIR) $(TARGETDIR)/$(IMAGINEDIR) $(TARGETDIR)/$(TARGET).tex
	cd $(TARGETDIR);\
	xelatex --no-pdf $(TARGET).tex && xelatex $(TARGET).tex

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
$(TARGETDIR)/$(TEXTEMPLATE_EXTRA): $(MISC)/$(TEXTEMPLATE_EXTRA) $(MDDIR)/$(CONFIG)
	$(PANDOC) -f markdown -t latex -M short-hash=$(HASH) --template $< $(MISC)/$(CONFIG) $(MDDIR)/$(CONFIG) -o $@
$(TARGETDIR)/$(TEXTEMPLATE_COVER): $(MISC)/$(TEXTEMPLATE_COVER) $(MDDIR)/$(CONFIG)
	$(PANDOC) -f markdown -t latex -M short-hash=$(HASH) --template $< $(MISC)/$(CONFIG) $(MDDIR)/$(CONFIG) -o $@
$(TARGETDIR)/$(TEXTEMPLATE_TAIL): $(MISC)/$(TEXTEMPLATE_TAIL) $(MDDIR)/$(CONFIG)
	$(PANDOC) -f markdown -t latex -M short-hash=$(HASH) --template $< $(MISC)/$(CONFIG) $(MDDIR)/$(CONFIG) -o $@
$(TARGETDIR)/$(TARGET).tex: $(FILTERED) $(MDDIR)/$(CONFIG) $(TARGETDIR)/$(TEXTEMPLATE_EXTRA) $(TARGETDIR)/$(TEXTEMPLATE_COVER) $(TARGETDIR)/$(TEXTEMPLATE_TAIL)
	$(PANDOC) $(PANFLAGS) $(TEXFLAGS) $(TEXFONTFLAGS) \
		$(FILTERED) -o $(TARGETDIR)/$(TARGET).tex

filtered: $(FILTERED)
$(FILTERED): $(MDDIR)/$(INPUT) $(MARKDOWN)
	$(GPP) $(GPPFLAGS) $< > $@

initdir:
	mkdir -p $(PREFIX)/
	mkdir -p $(PREFIX)/$(CIDIR)
	mkdir -p $(PREFIX)/$(TARGETDIR)
	mkdir -p $(PREFIX)/$(DATADIR)
	mkdir -p $(PREFIX)/$(MDDIR)
	mkdir -p $(PREFIX)/$(IMAGEDIR)

init: initdir
	cp -i $(MISC)/Makefile.txt $(PREFIX)/Makefile
	cp -i $(MISC)/config.txt $(PREFIX)/$(MDDIR)/$(CONFIG)
	cp -i $(MISC)/gitignore.txt $(PREFIX)/.gitignore
	cp -i $(MISC)/circleci.yml $(PREFIX)/$(CIDIR)/config.yml
	touch $(PREFIX)/$(MDDIR)/$(INPUT)

$(TARGETDIR):
	mkdir -p $(TARGETDIR)
$(DATADIR):
	mkdir -p $(DATADIR)
$(MDDIR):
	mkdir -p $(MDDIR)
$(IMAGEDIR):
	mkdir -p $(IMAGEDIR)

clean: $(TARGETDIR)
	rm -rf $(TARGETDIR)/*
