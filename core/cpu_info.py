import wmi
import psutil

class CPUInfo:
    """
    Clase para obtener información detallada del procesador (CPU) del sistema.
    """

    def __init__(self):
        """
        Inicializa la conexión WMI y obtiene el objeto de información del procesador.
        """
        try:
            self.c = wmi.WMI()
            self.cpu_info = self.c.Win32_Processor()[0]
        except Exception as e:
            self.c = None
            self.cpu_info = None
            self.init_error = f"Error inicializando WMI: {e}"
        else:
            self.init_error = None

    def get_info(self):
        """
        Devuelve un diccionario con la información relevante del CPU.
        """
        if self.init_error:
            return {
                "nameCPU": self.init_error,
                "physicalCore": "No disponible",
                "logicalCore": "No disponible",
                "maxClockSpeed": "No disponible",
                "currentUsage": "No disponible"
            }
        try:
            name_cpu = f"{self.cpu_info.Name}"
        except Exception as e:
            name_cpu = f"Error: {e}"
        try:
            physical_core = f"{psutil.cpu_count(logical=False)}"
        except Exception as e:
            physical_core = f"Error: {e}"
        try:
            logical_core = f"{psutil.cpu_count(logical=True)}"
        except Exception as e:
            logical_core = f"Error: {e}"
        try:
            max_clock_speed = f"{self.cpu_info.MaxClockSpeed} MHz"
        except Exception as e:
            max_clock_speed = f"Error: {e}"
        try:
            current_usage = f"{psutil.cpu_percent(interval=1)}%"
        except Exception as e:
            current_usage = f"Error: {e}"

        return {
            "nameCPU": name_cpu,
            "physicalCore": physical_core,
            "logicalCore": logical_core,
            "maxClockSpeed": max_clock_speed,
            "currentUsage": current_usage
        }