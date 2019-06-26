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

tex:
	cd docs; \
	make tex

docx:
	cd docs; \
	make docx

pdf:
	cd docs; \
	make pdf
