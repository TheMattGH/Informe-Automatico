from pathlib import Path
import sys

def get_bundle_base():
    """
    Devuelve la ruta base para recursos y carpetas, compatible con desarrollo y PyInstaller.
    """
    if getattr(sys, 'frozen', False):
        return Path(getattr(sys, '_MEIPASS'))
    else:
        return Path(__file__).resolve().parent.parent