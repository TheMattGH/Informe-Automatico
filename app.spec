import os
from PyInstaller.utils.hooks import collect_all

# Configuración de cifrado para PyInstaller (usualmente None)
block_cipher = None

# Inicialización de listas para recursos y binarios
datas = []
binaries = []

# Recopila todos los archivos, binarios y módulos de los paquetes personalizados
core_a, core_b, core_c = collect_all('core')
src_a, src_b, src_c = collect_all('src')
utils_a, utils_b, utils_c = collect_all('utils')

# Agrega los recursos y binarios recopilados a las listas principales
datas += core_a + src_a + utils_a
binaries += core_b + src_b + utils_b
hiddenimports = core_c + src_c + utils_c

a = Analysis(
    ['src/app.py'],  # Archivo principal de entrada de la app
    pathex=['C:\\Proyecto'],  # Ruta base del proyecto
    binaries=binaries,        # Binarios a incluir
    datas=datas + [           # Recursos adicionales a incluir en el bundle
        ('data/plantilla.pdf', 'data'),
        ('data/assets/app_icon.ico', 'data/assets'),
        ('data/assets/LOGOBA.png', 'data/assets'),
        ('reports', 'reports'),
    ],
    hiddenimports=hiddenimports + [  # Módulos que PyInstaller debe incluir aunque no detecte automáticamente
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
    name='Generador de Informes',  # Nombre del ejecutable
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # False: no muestra consola al ejecutar (aplicación GUI)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join('data', 'assets', 'app_icon.ico')  # Icono del ejecutable
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Generador de Informes Automático',  # Nombre de la carpeta final en dist/
)