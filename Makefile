all: release

ressources=zested/ressources.py

release: ressources

release:
	python3 setup.py py2app
	zip -r dist/ZestEd.app.zip dist/ZestEd.app

ressources: $(ressources)
$(ressources): zested.qrc
	pyside-rcc -py3 $^ -o $@
