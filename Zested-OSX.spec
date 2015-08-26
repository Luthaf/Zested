import os

a = Analysis(['zested/main.py'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)

pyz = PYZ(a.pure)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Zested',
          debug=False,
          strip=None,
          upx=True,
          console=False)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               Tree('zested/assets', prefix='assets'),
               strip=None,
               upx=True,
               name='Zested')

app = BUNDLE(coll,
             name='Zested.app',
             icon='zested/assets/img/clem.icns')
