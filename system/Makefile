ifeq ($(OS),Windows_NT)
HOME = C:/Users/$(USERNAME)
endif
PIPBASE= $(shell get-pip-base)
PANSTYLES= $(PIPBASE)/var
MISC= $(PANSTYLES)/pandoc_misc
MISC_SYS = $(MISC)/system
MISC_USER = $(MISC)/user

ifeq ($(PROJECT),)
include $(MISC_SYS)/Makefile.in
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

docx: coreprop

coreprop: $(DOCX)
	$(DOCXPWRTR) -I $(MDDIR)/$(CONFIG) $(COREPROPFLAGS) -O $(DOCX)

$(DOCX): $(FILTERED)
	$(PANDOC) $(PANFLAGS) $(PANDOCXFLAGS) --reference-doc=$(REFERENCE) $(FILTERED) -o $(DOCX)

reverse-docx:
	$(PANDOC) $(PANREVERSEDOCX) $(TARGETDIR)/$(REVERSE_INPUT) -o $(MDDIR)/$(INPUT)

html: $(HTML) $(MDDIR)/$(CONFIG)
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
$(TARGETDIR)/$(TEXTEMPLATE_EXTRA): $(MISC_SYS)/$(TEXTEMPLATE_EXTRA) $(MDDIR)/$(CONFIG)
	$(PANDOC) -f markdown -t latex -M short-hash=$(HASH) --template $< $(MISC_SYS)/$(CONFIG) $(MDDIR)/$(CONFIG) -o $@
$(TARGETDIR)/$(TEXTEMPLATE_COVER): $(MISC_SYS)/$(TEXTEMPLATE_COVER) $(MDDIR)/$(CONFIG)
	$(PANDOC) -f markdown -t latex -M short-hash=$(HASH) --template $< $(MISC_SYS)/$(CONFIG) $(MDDIR)/$(CONFIG) -o $@
$(TARGETDIR)/$(TEXTEMPLATE_TAIL): $(MISC_SYS)/$(TEXTEMPLATE_TAIL) $(MDDIR)/$(CONFIG)
	$(PANDOC) -f markdown -t latex -M short-hash=$(HASH) --template $< $(MISC_SYS)/$(CONFIG) $(MDDIR)/$(CONFIG) -o $@
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
	mkdir -p $(PREFIX)/$(SVGDIR)

init: initdir
	cp -i $(MISC_USER)/Makefile $(PREFIX)/Makefile
	cp -i $(MISC_USER)/config.yaml $(PREFIX)/$(MDDIR)/$(CONFIG)
	cp -i $(MISC_USER)/.gitignore $(PREFIX)/.gitignore
	cp -i $(MISC_USER)/circleci.yml $(PREFIX)/$(CIDIR)/config.yml
	touch $(PREFIX)/$(MDDIR)/$(INPUT)

$(TARGETDIR):
	mkdir -p $(TARGETDIR)
$(DATADIR):
	mkdir -p $(DATADIR)
$(MDDIR):
	mkdir -p $(MDDIR)
$(IMAGEDIR):
	mkdir -p $(IMAGEDIR)
$(SVGDIR):
	mkdir -p $(SVGDIR)

clean: $(TARGETDIR) $(SVGDIR)
	rm -rf $(TARGETDIR)/*
	rm -rf $(SVGDIR)/*
