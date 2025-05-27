import wmi
import psutil

class CPUInfo:
    def __init__(self):
        self.c = wmi.WMI()
        self.cpu_info = self.c.Win32_Processor()[0]
   
    def getInfo(self):
        return{
            "nameCPU" : f"{self.cpu_info.Name}",
            "physicalCore" : f"{psutil.cpu_count(logical=False)}",
            "logicalCore" : f"{psutil.cpu_count(logical=True)}",
            "maxClockSpeed" : f"{self.cpu_info.MaxClockSpeed} MHz",
            "currentUsage" : f"{psutil.cpu_percent(interval=1)}%"
        }
    def print(self):
        info = self.getInfo()
        print("------ Informacion CPU ------")
        print(f"Nombre: {info["nameCPU"]}")
        print(f"Nucleos Fisicos: {info["physicalCore"]}")
        print(f"Nucleos Logicos: {info["logicalCore"]}")
        print(f"Frecuencia Actual: {info["maxClockSpeed"]}")
        print(f"Uso Actual: {info["currentUsage"]}")

