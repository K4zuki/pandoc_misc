include Makefile.win
# include Makefile.in

INPUT= source.md
OUTPUT= $(shell basename $(INPUT) .md)
CSV= $(shell ls *.csv)
TABLES= $(CSV:.csv=_t.md)
TARGETDIR= ./Out

SRC= $(filter-out f_%.md, $(INPUT))
FILTERED= $(SRC:%=$(TARGETDIR)/f_%)

all: docx

docx: html
	$(PANDOC) --reference-docx=$(REFERENCE) $(OUTPUT).html -o $(OUTPUT).docx; \
	$(PYTHON) $(DOCXPWRTR) -I $(INPUT) -O $(OUTPUT).docx

html: filtered
	$(PANDOC) $(PANFLAGS) --self-contained -thtml5 --template=$(MISC)/github.html \
		$(FILTERED) -o $(TARGETDIR)/$(OUTPUT).html

filtered: tables
	for src in $(SRC); do \
		cat "$$src" | $(PYTHON) $(FILTER) --out f_"$$src" --basedir $(TARGETDIR) \
	;done

tables: $(CSV)
	mkdir -p $(TARGETDIR); \
	for csv in $(CSV); do \
		echo "$$csv"; \
		$(PYTHON) $(CSV2TABLE) --file "$$csv" --out $(TARGETDIR)/`baseneme "$$csv" .csv`_t.md --delimiter ','; \
	done

clean:
	rm -rf $(TARGETDIR)
