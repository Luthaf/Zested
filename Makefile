version=$(shell python3 -c "import zested; print(zested.__version__)")
ressources=zested/ressources.py

OsX_app=dist/ZestEd.app
OsX_zip=dist/ZestEd-OsX-$(version).zip

Win_app=dist/windows/ZestEd.exe
Win_zip=dist/ZestEd-Windows-$(version).zip

all: release
release: $(ressources) $(OsX_zip) $(Win_zip)

$(OsX_zip):$(OsX_app)
	@echo "Ziping ZestEd.app"
	@zip -r $(OsX_zip) $(OsX_app) > /dev/null

$(OsX_app):
	@echo "Building ZestEd.app"
	@python3 setup.py py2app > /dev/null

$(Win_zip): $(Win_app)
	@echo "Ziping Windows version"
	@zip -r $(Win_zip) dist/windows > /dev/null

$(ressources): zested.qrc
	pyside-rcc -py3 $^ -o $@

.PHONY: clean

clean:
	rm -rf build dist