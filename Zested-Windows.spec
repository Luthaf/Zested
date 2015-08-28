# -*- mode: python -*-

block_cipher = None

a = Analysis(['Zested.py'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             cipher=block_cipher)

pyz = PYZ(a.pure, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Zested.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False,
          icon='zested\\assets\\img\\clem.ico')

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               Tree('zested/assets', prefix='assets'),
               strip=None,
               upx=True,
               name='Zested-Windows')
