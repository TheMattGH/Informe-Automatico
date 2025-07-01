import psutil
import wmi

class MemoryInfo:
    """
    Clase para obtener información detallada de la memoria RAM del sistema.
    """

    def __init__(self):
        """
        Inicializa los objetos necesarios para obtener información de memoria.
        """
        self.mem = psutil.virtual_memory()
        self.c = wmi.WMI()
    
    def get_info(self):
        """
        Devuelve un diccionario con información general de la memoria RAM.
        """
        return {
            "totalMemory": f"{self.mem.total / (1024**3):.2f} GB",
            "avaliableMemory": f"{self.mem.available / (1024**3):.2f} GB",
            "percentUsedMemory": f"{self.mem.percent}%",
            "usedMemory": f"{self.mem.used / (1024**3):.2f} GB",
            "freeMemory": f"{self.mem.free / (1024**3):.2f} GB"
        }
    
    def get_slot_info(self):
        """
        Devuelve un diccionario con información sobre los slots de memoria RAM.
        Incluye total de slots, usados, libres y detalles por slot.
        """
        slot_details = []
        used_slots = 0

        try:
            # Detectar número real de slots usando Win32_PhysicalMemoryArray
            total_slots = 0
            for mem_array in self.c.Win32_PhysicalMemoryArray():
                total_slots += int(mem_array.MemoryDevices)

            # Si no se pudo detectar, fallback a 4
            if total_slots == 0:
                total_slots = 4

            # Recorrer módulos de memoria instalados
            for mem in self.c.Win32_PhysicalMemory():
                used_slots += 1
                capacity = int(mem.Capacity) / (1024**3)
                slot_details.append(f"{mem.DeviceLocator}: {capacity:.2f} GB")

            free_slots = total_slots - used_slots

            return {
                "totalSlots": total_slots,
                "usedSlots": used_slots,
                "freeSlots": free_slots,
                "detailSlots": slot_details
            }

        except Exception as e:
            return {"Error": f"No se pudo obtener la información de slots {e}"}