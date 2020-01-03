FILTERED := $(INPUT:%.md=$(TARGETDIR)/%.md)
HTML := $(TARGETDIR)/$(TARGET).html
DOCX := $(TARGETDIR)/$(TARGET).docx

MARKDOWN = $(shell ls $(MDDIR)/*.md)

PANFLAGS += --resource-path=.:$(DATADIR):$(IMAGEDIR):$(MDDIR):$(TARGETDIR)
PANFLAGS += $(MDDIR)/$(CONFIG)
PANFLAGS += $(MISC_SYS)/$(CONFIG)

PANDOCXFLAGS += --template=$(SYSTEM_DOCXFRONTPAGE)
PANDOCXFLAGS += $(MDDIR)/$(CONFIG)
PANDOCXFLAGS += $(MISC_SYS)/$(CONFIG)

TARGET_TEXTEMPLATE_EXTRA := $(TARGETDIR)/$(TEXTEMPLATE_EXTRA)
TARGET_TEXTEMPLATE_COVER := $(TARGETDIR)/$(TEXTEMPLATE_COVER)
TARGET_TEXTEMPLATE_TAIL := $(TARGETDIR)/$(TEXTEMPLATE_TAIL)
TARGET_DOCXFRONTPAGE := $(TARGETDIR)/$(DOCXFRONTPAGE)

TEXFLAGS += --include-in-header=$(TARGET_TEXTEMPLATE_EXTRA)
TEXFLAGS += --include-before-body=$(TARGET_TEXTEMPLATE_COVER)
TEXFLAGS += --include-after-body=$(TARGET_TEXTEMPLATE_TAIL)

.PHONY: docx html pdf tex merge clean linking

all: html

docx: coreprop

coreprop: $(DOCX)
	$(DOCXPWRTR) -I $(MDDIR)/$(CONFIG) $(COREPROPFLAGS) -O $(DOCX)

$(DOCX): $(MDDIR)/$(INPUT)
	$(PANDOC) $(PANDOCXFLAGS) -o $(TARGET_DOCXFRONTPAGE)
	$(PANDOC) $(PANFLAGS) -M linkReferences=true --reference-doc=$(REFERENCE) -Mtitle= -Msubtitle= -Mauthor= \
	$(TARGET_DOCXFRONTPAGE) $(MDDIR)/$(INPUT) -o $(DOCX)

reverse-docx:
	$(PANDOC) $(PANREVERSEDOCX) $(TARGETDIR)/$(REVERSE_INPUT) -o $(MDDIR)/$(INPUT)

html: $(HTML) $(MDDIR)/$(CONFIG)
$(HTML): $(MDDIR)/$(INPUT) $(MDDIR)/$(CONFIG)
	$(PANDOC) $(PANFLAGS) $(PANHTMLFLAGS) $(MDDIR)/$(INPUT) -o $(HTML)

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

$(TARGET_TEXTEMPLATE_EXTRA): $(SYSTEM_TEXTEMPLATE_EXTRA) $(MDDIR)/$(CONFIG)
	$(PANDOC) -f markdown -t latex -M short-hash=$(HASH) -M envversion=$(ENV_VERSION) \
	--template $< $(MDDIR)/$(CONFIG) $(MISC_SYS)/$(CONFIG) -o $@

$(TARGET_TEXTEMPLATE_COVER): $(SYSTEM_TEXTEMPLATE_COVER) $(MDDIR)/$(CONFIG)
	$(PANDOC) -f markdown -t latex -M short-hash=$(HASH) -M envversion=$(ENV_VERSION) \
	--template $< $(MDDIR)/$(CONFIG) $(MISC_SYS)/$(CONFIG) -o $@

$(TARGET_TEXTEMPLATE_TAIL): $(SYSTEM_TEXTEMPLATE_TAIL) $(MDDIR)/$(CONFIG)
	$(PANDOC) -f markdown -t latex -M short-hash=$(HASH) -M envversion=$(ENV_VERSION) \
	--template $< $(MDDIR)/$(CONFIG) $(MISC_SYS)/$(CONFIG) -o $@

$(TARGETDIR)/$(TARGET).tex: $(MDDIR)/$(INPUT) $(MDDIR)/$(CONFIG) \
							$(TARGET_TEXTEMPLATE_EXTRA) \
							$(TARGET_TEXTEMPLATE_COVER) \
							$(TARGET_TEXTEMPLATE_TAIL)
	$(PANDOC) $(PANFLAGS) $(TEXFLAGS) $(TEXFONTFLAGS) $(MDDIR)/$(INPUT) -o $(TARGETDIR)/$(TARGET).tex

initdir:
	mkdir -p $(PREFIX)/
	mkdir -p $(PREFIX)/$(CIDIR)
	mkdir -p $(PREFIX)/$(TARGETDIR)
	mkdir -p $(PREFIX)/$(DATADIR)
	mkdir -p $(PREFIX)/$(MDDIR)
	mkdir -p $(PREFIX)/$(IMAGEDIR)
	mkdir -p $(PREFIX)/$(SVGDIR)
	mkdir -p $(PREFIX)/$(IMAGINEDIR)

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

$(IMAGINEDIR):
	mkdir -p $(IMAGINEDIR)

clean: $(TARGETDIR) $(SVGDIR) $(IMAGINEDIR)
	rm -rf $(TARGETDIR)/*
	rm -rf $(SVGDIR)/*
	rm -rf $(IMAGINEDIR)/*
