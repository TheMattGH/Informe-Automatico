import wmi

class SoftwareInfo:
    """
    Clase para obtener información del sistema operativo instalado.
    """

    def __init__(self):
        """
        Inicializa la conexión WMI y obtiene la información del sistema operativo.
        """
        self.c = wmi.WMI()
        self.os_info = self.c.Win32_OperatingSystem()[0]

    def get_info(self):
        """
        Devuelve un diccionario con información relevante del sistema operativo.
        """
        return {
            "os": f"{self.os_info.Caption} {self.os_info.Version}",
            "architecture": self.os_info.OSArchitecture,
            "manufacturer": self.os_info.Manufacturer,
            "registered_user": self.os_info.RegisteredUser
        }