import wmi

class SystemInfo:
    def __init__(self):
        self.c = wmi.WMI()
    
    def getInfo(self):
        system = self.c.Win32_ComputerSystem()[0]
        baseboard = self.c.Win32_BaseBoard()[0]
        bios = self.c.Win32_BIOS()[0]

        return {
            "manufacturer": system.Manufacturer.strip(),
            "model": system.Model.strip(),
            "baseboard": baseboard.Product.strip(),
            "baseboardManufacturer": baseboard.Manufacturer.strip(),
            "biosVersion": bios.SMBIOSBIOSVersion.strip(),
            "biosDate": bios.ReleaseDate.split('.')[0]  # solo fecha sin formato extendido
        }
    
    def print(self):
        info = self.getInfo()
        print("------ Informacion del Equipo ------")
        print(f"Fabricante: {info["manufacturer"]}")
        print(f"Modelo: {info["model"]}")
        print(f"Placa Base: {info["baseboard"]}")
        print(f"Fabricante de Placa Base: {info["baseboardManufacturer"]}")
        print(f"Version de la Bios: {info["biosVersion"]}")
        print(f"Fecha de la Bios: {info["biosDate"]}")


