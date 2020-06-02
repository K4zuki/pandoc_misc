PIPBASE := $(shell get-pip-base)
PANSTYLES := $(PIPBASE)/var
MISC := $(PANSTYLES)/pandoc_misc
MISC_SYS := $(MISC)/system
MISC_USER := $(MISC)/user

html:
	cd docs; \
	make html

install:
	pip3 install .

uninstall:
	pip3 uninstall -y pandoc-misc

reinstall: uninstall install
#	pip3 install .

clean:
	cd docs; \
	make clean

copy:
	cp -R system/* $(MISC_SYS)/
	cp -R user/* $(MISC_USER)/

tex: copy
	cd docs; \
	make tex

docx: copy
	cd docs; \
	make docx

reverse-docx: copy
	cd docs; \
	make reverse-docx

pdf: copy
	cd docs; \
	make pdf
