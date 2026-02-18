# -*- mode: python ; coding: utf-8 -*-

import sys

# Base hidden imports (cross-platform)
base_hiddenimports = [
    'PySide6', 'PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets',
    'yt_dlp', 'secretstorage', 'cryptography', 'cffi', 'jeepney'
]

# Windows-specific hidden imports
if sys.platform == 'win32':
    base_hiddenimports.extend(['win32api', 'win32con', 'win32gui', 'win32process'])

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[('src/app/style.qss', 'app'), ('src/app/style_light.qss', 'app'), ('horse2026.jpeg', '.')],
    hiddenimports=base_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Fast-Horse-2026',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
