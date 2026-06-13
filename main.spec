# -*- mode: python ; coding: utf-8 -*-

import os
import sys

# 获取项目根目录
# SPECPATH 是 PyInstaller 内置变量，指向 .spec 文件所在目录
try:
    project_root = os.path.abspath(SPECPATH)
except NameError:
    project_root = os.getcwd()

# 动态获取 customtkinter 路径
import customtkinter
ctk_path = os.path.dirname(customtkinter.__file__)

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[(ctk_path, 'customtkinter/'), (os.path.join(project_root, 'resources/images'), 'resources/images/')],
    hiddenimports=['customtkinter'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes = [],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[os.path.join(project_root, 'resources/icons/mytool.ico')],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PyTools',
)
