import wmi
from screeninfo import get_monitors

class PeripheralsInfo:
    """
    Clase para obtener información de los periféricos conectados al sistema.
    """

    def __init__(self):
        """
        Inicializa la conexión WMI.
        """
        self.c = wmi.WMI()

    def get_info(self):
        """
        Devuelve un diccionario con la información de monitores, impresoras,
        teclados, ratones, cámaras, audio y dispositivos USB conectados.
        """
        data = {}

        # Monitores
        monitors = []
        try:
            screen_monitors = get_monitors()
        except Exception:
            screen_monitors = []
        try:
            pnp_entities = self.c.Win32_PnPEntity()
            pnp_monitor_names = [dev.Name for dev in pnp_entities if dev.Name and "monitor" in dev.Name.lower()]
        except Exception:
            pnp_monitor_names = []

        for i, m in enumerate(screen_monitors):
            name = pnp_monitor_names[i] if i < len(pnp_monitor_names) else "Monitor desconocido"
            resolution = f"{m.width}x{m.height}"
            monitors.append(f"{name} ({resolution})")
        data["Monitores"] = monitors or ["No detectados"]

        # Impresoras
        try:
            printers = [
                f"{p.Name} | Driver: {p.DriverName} | Puerto: {p.PortName} | Estado: {'Offline' if p.WorkOffline else 'Online'}"
                for p in self.c.Win32_Printer()
            ]
        except Exception:
            printers = []
        data["Impresoras"] = printers or ["No detectadas"]

        # Teclados
        try:
            keyboards = [f"{k.Description}" for k in self.c.Win32_Keyboard()]
        except Exception:
            keyboards = []
        data["Teclados"] = keyboards or ["No detectados"]

        # Ratones
        try:
            mouses = [f"{m.Description}" for m in self.c.Win32_PointingDevice()]
        except Exception:
            mouses = []
        data["Ratones"] = mouses or ["No detectados"]

        # Cámaras
        cams = []
        try:
            for cam in self.c.Win32_PnPEntity():
                if cam.Name and "camera" in cam.Name.lower():
                    cams.append(f"{cam.Name} | Fabricante: {cam.Manufacturer}")
        except Exception:
            pass
        data["Cámaras"] = cams or ["No detectadas"]

        # Sonido
        try:
            sounds = [f"{s.Name} | Fabricante: {s.Manufacturer}" for s in self.c.Win32_SoundDevice()]
        except Exception:
            sounds = []
        data["Audio"] = sounds or ["No detectados"]

        # Unidades USB
        usbs = []
        try:
            for disk in self.c.Win32_DiskDrive():
                if "USB" in disk.InterfaceType:
                    size = f"{int(disk.Size) / (1024**3):.2f} GB"
                    usbs.append(f"{disk.Model} ({size}) | Interfaz: {disk.InterfaceType}")
        except Exception:
            pass
        data["Dispositivos USB"] = usbs or ["No conectados"]

        return data
    
    @staticmethod
    def format_for_report(peripherals_data):
        """
        Devuelve un diccionario con los valores listos para el reporte.
        Convierte los valores no-lista a string.
        """
        return {k: v if isinstance(v, list) else str(v) for k, v in peripherals_data.items()}