# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['../src/rebel.py'],
             pathex=['/Users/sms1n16/ReBell/build'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='ReBel',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='../img/ReBel_Icon.ico' )
app = BUNDLE(exe,
             name='ReBel.app',
             icon='../img/ReBel_Icon.icns',
             bundle_identifier=None)
