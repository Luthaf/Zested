all: release

ressources=zested/ressources.py

release: ressources

ressources: $(ressources)
$(ressources): zested.qrc
	pyside-rcc -py3 $^ -o $@
