import socket
from datetime import datetime
import psutil
import geocoder

class UserInfo:
    """
    Clase para recopilar y estructurar la información del usuario y del entorno
    """

    def __init__(self, names=None, department=None):
        """
        Inicializa la información del usuario.
        """
        self.names = names
        self.department = department
        self.username = self.get_logged_user()
        self.datetime_now = self.get_datetime()
        self.location = self.get_location()

    def get_logged_user(self):
        """
        Obtiene el nombre del usuario actualmente logueado en el sistema.
        """
        try:
            usuarios = psutil.users()
            return usuarios[0].name if usuarios else "Sin usuario"
        except Exception as e:
            return f"Error obteniendo usuario: {e}"

    def get_datetime(self):
        """
        Obtiene la fecha y hora actual en formato legible.
        """
        try:
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            return f"Error obteniendo fecha/hora: {e}"

    def get_location(self):
        """
        Obtiene la ubicación aproximada del usuario mediante su IP pública.
        """
        try:
            g = geocoder.ip('me')
            return g.city if g.city else "No disponible"
        except Exception as e:
            return f"No disponible ({e})"

    def get_info(self):
        """
        Devuelve un diccionario con toda la información relevante del usuario.
        """
        return {
            "names": self.names,
            "department": self.department,
            "date": self.datetime_now,
            "user": self.username,
            "location": self.location
        }

    def get_text(self):
        """
        Devuelve la información del usuario en formato HTML para el informe.
        """
        return (
            f"<b>Nombre:</b> {self.names}<br/>"
            f"<b>Departamento:</b> {self.department}<br/>"
            f"<b>Fecha y hora de generación del informe:</b> {self.datetime_now}<br/>"
            f"<b>Usuario logueado actualmente:</b> {self.username}<br/>"
            f"<b>Ubicación:</b> {self.location}"
        )