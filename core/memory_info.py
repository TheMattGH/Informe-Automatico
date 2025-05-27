import psutil

class MemoryInfo():
    def __init__(self):
        self.mem = psutil.virtual_memory()
    
    def getInfo(self):
        return{
            "totalMemory" : f"{self.mem.total / (1024**3):.2f} GB",
            "avaliableMemory" : f"{self.mem.available / (1024**3):.2f} GB",
            "percentUsedMemory" : f"{self.mem.percent}%",
            "usedMemory" : f"{self.mem.used / (1024**3):.2f} GB",
            "freeMemory" : f"{self.mem.free / (1024**3):.2f} GB"
        }
    def print(self):
        info = self.getInfo()
        print("------ Informacion de Memoria RAM ------")
        print(f"Memoria Total: {info["totalMemory"]}")
        print(f"Memoria Disponible: {info["avaliableMemory"]}")
        print(f"Porcentaje de uso: {info["percentUsedMemory"]}")
        print(f"Memoria Usada: {info["usedMemory"]}")
        print(f"Memoria Libre: {info["freeMemory"]}")
