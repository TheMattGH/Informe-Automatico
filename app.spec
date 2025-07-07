import os
from PyInstaller.utils.hooks import collect_all

# Nombre del archivo principal que inicia tu aplicación
block_cipher = None

# Recopilar archivos y recursos necesarios
datas = []
binaries = []

# Incluir tus módulos personalizados
core_a, core_b, core_c = collect_all('core')
src_a, src_b, src_c = collect_all('src')
utils_a, utils_b, utils_c = collect_all('utils')

# Agregar todos los datos recopilados
datas += core_a + src_a + utils_a
binaries += core_b + src_b + utils_b
hiddenimports = core_c + src_c + utils_c

a = Analysis(
    ['src/app.py'],  # El punto de entrada de tu app
    pathex=['C:\\Proyecto'],
    binaries=binaries,
    datas=datas + [
    ('data/plantilla.pdf', 'data'),
    ('data/assets/app_icon.ico', 'data/assets'),
    ('data/assets/LOGOBA.png', 'data/assets'),  # <-- Asegúrate de incluir esto
    ('reports', 'reports'),
],
    hiddenimports=hiddenimports + [
        'wmi', 'psutil', 'PySide6.QtCore', 'PySide6.QtGui',
        'PySide6.QtWidgets', 'pdfrw', 'pathlib'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Generador de Informes',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # False para aplicación GUI sin consola
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join('data', 'assets', 'app_icon.ico')
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Generador de Informes Automático',
)