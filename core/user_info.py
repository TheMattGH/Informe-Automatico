import socket
from datetime import datetime
import psutil

class UserInfo:
    def __init__(self):
        self.username = self.getLoggedUser()
        self.datetime_now = self.getDatetime()
        self.location = self.getLocation()
    
    def getLoggedUser(self):
        usuarios = psutil.users()
        return usuarios[0].name if usuarios else "Sin usuario"

    def getDatetime(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def getLocation(self):
        try:
            import geocoder
            g = geocoder.ip('me')
            return g.city if g.city else "No disponible"
        except:
            return "No disponible"
    
    def getInfo(self):
        return {
            "date": self.datetime_now,
            "user": self.username,
            "location": self.location
        }
    
    def getText(self):
        return (
            f"<b>Fecha y hora de generación del informe:</b> {self.datetime_now}<br/>"
            f"<b>Usuario logueado actualmente:</b> {self.username}<br/>"
            f"<b>Ubicación:</b> {self.location}"
        )
    
    def print(self):
        info = self.getInfo()
        print(f'Fecha y hora de generacion: {info["date"]}')
        print(f'Usuario Logueado: {info["user"]}')
        print(f'Ubicacion: {info["location"]}')