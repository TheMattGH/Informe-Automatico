import wmi

class SoftwareInfo :
 
    def __init__(self):
        self.c = wmi.WMI()
        self.os_info = self.c.Win32_OperatingSystem()[0]

    def getInfo(self):
        return{
            "os" : f"{self.os_info.Caption} {self.os_info.Version}",
            "architecture" : self.os_info.OSArchitecture,
            "manufacturer" : self.os_info.Manufacturer,
            "registered_user" : self.os_info.RegisteredUser
        }
    def print(self):
        info = self.getInfo()
        print("------ Informacion Sistema Operativo ------")
        print(f"Sistema Operativo: {info['os']}")
        print(f"Arquitectura: {info['architecture']}")
        print(f"Fabricante: {info['manufacturer']}")
        print(f"Usuario Registrado: {info['registered_user']}")

