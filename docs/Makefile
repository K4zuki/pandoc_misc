ifeq ($(OS),Windows_NT)
HOME = C:/Users/$(USERNAME)
endif
PIPBASE= $(shell get-pip-base)
PANSTYLES= $(PIPBASE)/var
MISC= ..
MISC_SYS = $(MISC)/system
MISC_USER = $(MISC)/user
include $(MISC_SYS)/Makefile.in
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
MISC:= ..
MISC_SYS:= $(MISC)/system
MISC_USER:= $(MISC)/user
SYSTEM_TEXTEMPLATE_EXTRA := $(MISC_SYS)/$(TEXTEMPLATE_EXTRA)
SYSTEM_TEXTEMPLATE_COVER := $(MISC_SYS)/$(TEXTEMPLATE_COVER)
SYSTEM_TEXTEMPLATE_TAIL := $(MISC_SYS)/$(TEXTEMPLATE_TAIL)

include $(MISC_SYS)/Makefile
