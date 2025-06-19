import psutil
import wmi

class MemoryInfo():
    def __init__(self):
        self.mem = psutil.virtual_memory()
        self.c = wmi.WMI()
    
    def getInfo(self):
        return{
            "totalMemory" : f"{self.mem.total / (1024**3):.2f} GB",
            "avaliableMemory" : f"{self.mem.available / (1024**3):.2f} GB",
            "percentUsedMemory" : f"{self.mem.percent}%",
            "usedMemory" : f"{self.mem.used / (1024**3):.2f} GB",
            "freeMemory" : f"{self.mem.free / (1024**3):.2f} GB"
        }
    
    def getSlotInfo(self):
        total_slots = 0
        used_slots = 0
        slot_details = []

        try:
            for mem in self.c.Win32_PhysicalMemory():
                total_slots += 1
                used_slots += 1
                capacity = int(mem.Capacity) / (1024**3)
                slot_details.append(f"{mem.DeviceLocator}: {capacity:.2f} GB")

            # Asumimos 4 slots totales como valor máximo estimado
            total_slots = max(used_slots, 4)
            free_slots = total_slots - used_slots

            return {
                "totalSlots": total_slots,
                "usedSlots": used_slots,
                "freeSlots": free_slots,
                "detailSlots": slot_details
            }

        except Exception as e:
            return {"Error": f"No se pudo obtener la información de slots: {e}"}

    def print(self):
        info = self.getInfo()
        print("------ Informacion de Memoria RAM ------")
        print(f"Memoria Total: {info["totalMemory"]}")
        print(f"Memoria Disponible: {info["avaliableMemory"]}")
        print(f"Porcentaje de uso: {info["percentUsedMemory"]}")
        print(f"Memoria Usada: {info["usedMemory"]}")
        print(f"Memoria Libre: {info["freeMemory"]}")

        slot_info = self.getSlotInfo()
        print("------ Información de Slots de Memoria ------")
        print(f"Total de Slots: {slot_info['totalSlots']}")
        print(f"Slots Usados: {slot_info['usedSlots']}")
        print(f"Slots Libres: {slot_info['freeSlots']}")
        for detail in slot_info['detailSlots']:
            print(f"- {detail}")

