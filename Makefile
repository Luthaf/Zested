version=$(shell python3 -c "import zested; print(zested.__version__)")
ressources=zested/ressources.py

osx_app=dist/Zested.app
osx_dmg=dist/Zested-OSX-$(version).dmg

win_app=dist/Zested-windows/Zested.exe
win_zip=dist/Zested-Windows-$(version).zip

all: $(osx_app)
dist: $(ressources) $(osx_dmg) $(win_zip)

$(osx_dmg):$(osx_app)
	@echo "==================  Creating OSX disk image  =================="
	@hdiutil create $@ -srcfolder $^ -ov

$(osx_app):
	@echo "==================  Building OSX App  =================="
	@pyinstaller --clean -y Zested-OSX.spec

$(win_zip): $(win_app)
	@echo "==================  Ziping Windows version  =================="
	@zip -r $@ dist/Zested-windows/ > /dev/null

$(ressources): zested/assets/zested.qrc
	pyside-rcc -py3 $^ -o $@

.PHONY: clean, all, dist

clean:
	rm -rf build dist
