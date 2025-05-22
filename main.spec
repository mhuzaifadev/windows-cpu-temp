# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('WinTmp/LibreHardwareMonitorLib.dll', 'WinTmp'),
        ('WinTmp/System.IO.FileSystem.AccessControl.dll', 'WinTmp'),
        ('WinTmp/System.Security.Principal.Windows.dll', 'WinTmp'),
        ('WinTmp/System.Security.AccessControl.dll', 'WinTmp'),
        ('WinTmp/Microsoft.Win32.Registry.dll', 'WinTmp')
    ],
    hiddenimports=[],
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
    name='WindowsTempMonitor',
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
    icon=['assets\\icon.ico'],
)
