import wmi
from screeninfo import get_monitors

class PeripheralsInfo:
    def __init__(self):
        self.c = wmi.WMI()
    def getInfo(self):
        data = {}
        
        monitors = []
        try:
            screen_monitors = get_monitors()
        except Exception:
            screen_monitors = []

        pnp_entities = self.c.Win32_PnPEntity()
        pnp_monitor_names = [dev.Name for dev in pnp_entities if dev.Name and "monitor" in dev.Name.lower()]

        for i, m in enumerate(screen_monitors):
            name = pnp_monitor_names[i] if i < len(pnp_monitor_names) else "Monitor desconocido"
            resolution = f"{m.width}x{m.height}"
            monitors.append(f"{name} ({resolution})")

        data["Monitores"] = monitors or ["No detectados"]

        # Impresoras
        printers = [
            f"{p.Name} | Driver: {p.DriverName} | Puerto: {p.PortName} | Estado: {'Offline' if p.WorkOffline else 'Online'}"
            for p in self.c.Win32_Printer()
        ]
        data["Impresoras"] = printers or ["No detectadas"]

        # Teclados
        keyboards = [
            f"{k.Description}" for k in self.c.Win32_Keyboard()
        ]
        data["Teclados"] = keyboards or ["No detectados"]

        # Ratones
        mouses = [
            f"{m.Description}" for m in self.c.Win32_PointingDevice()
        ]
        data["Ratones"] = mouses or ["No detectados"]

        # Cámaras 
        cams = []
        for cam in self.c.Win32_PnPEntity():
            if cam.Name and "camera" in cam.Name.lower():
                cams.append(f"{cam.Name} | Fabricante: {cam.Manufacturer}")
        data["Cámaras"] = cams or ["No detectadas"]

        # Sonido
        sounds = [
            f"{s.Name} | Fabricante: {s.Manufacturer}" for s in self.c.Win32_SoundDevice()
        ]
        data["Audio"] = sounds or ["No detectados"]

        # Unidades USB
        usbs = []
        for disk in self.c.Win32_DiskDrive():
            if "USB" in disk.InterfaceType:
                size = f"{int(disk.Size) / (1024**3):.2f} GB"
                usbs.append(f"{disk.Model} ({size}) | Interfaz: {disk.InterfaceType}")
        data["Dispositivos USB"] = usbs or ["No conectados"]

        return data

    def getKeyValueTable(self):
        info = self.getInfo()
        cabecera = ["Categoría", "Dispositivos"]
        filas = []

        for categoria, dispositivos in info.items():
            dispositivos_str = ", ".join(dispositivos)
            filas.append([categoria, dispositivos_str])

        return cabecera, filas
    
    def print(self):
        data = self.getInfo()
        print("------ Periféricos Conectados ------")
        for categoria, elementos in data.items():
            print(f"\n{categoria}:")
            for e in elementos:
                print(f"- {e}")
