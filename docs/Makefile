ifeq ($(OS),Windows_NT)
HOME = C:/Users/$(USERNAME)
endif
PIPBASE= $(shell get-pip-base)
PANSTYLES= $(PIPBASE)/var
MISC= $(PANSTYLES)/pandoc_misc
include $(MISC)/system/Makefile.in
PROJECT= `pwd`

## userland: uncomment and replace
# MDDIR:= markdown
# DATADIR:= data
# TARGETDIR:= Out
# IMAGEDIR:= images

# CONFIG:= config.yaml
# INPUT:= TITLE.md
# TARGET:= TARGET-$(DATE)-$(HASH)
# REVERSE_INPUT:= reverse-input.docx
# REFERENCE:= $(MISC)/ref.docx
# COREPROPFLAGS := --table "Normal Table=Centered"
# COREPROPFLAGS += --paragraph "Normal=Body Text"
##
include $(MISC)/system/Makefile
