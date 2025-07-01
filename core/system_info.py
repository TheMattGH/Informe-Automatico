import wmi

class SystemInfo:
    """
    Clase para obtener información relevante del sistema, placa base y BIOS.
    """

    def __init__(self):
        self.c = wmi.WMI()
    
    def get_info(self):
        """
        Devuelve un diccionario con información del fabricante, modelo,
        placa base y BIOS del sistema.
        """
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