version=$(shell python3 -c "import zested; print(zested.__version__)")
ressources=zested/ressources.py

OsX_app=dist/ZestEd.app
OsX_dmg=dist/ZestEd-$(version).dmg

Win_app=dist/windows/ZestEd.exe
Win_zip=dist/ZestEd-Windows-$(version).zip

all: release
release: $(ressources) $(OsX_dmg) $(Win_zip)

$(OsX_dmg):$(OsX_app)
	@echo "==================  Creating ZestEd.dmg  =================="
	@hdiutil create dist/Zested-$(version).dmg -srcfolder dist/Zested.app -ov

$(OsX_app):
	@echo "==================  Building ZestEd.app  =================="
	@pyinstaller --clean -y Zested-OSX.spec

$(Win_zip): $(Win_app)
	@echo "==================  Ziping Windows version  =================="
	@zip -r $(Win_zip) dist/windows > /dev/null

$(ressources): zested/assets/zested.qrc
	pyside-rcc -py3 $^ -o $@

.PHONY: clean

clean:
	rm -rf build dist
