import subprocess
import platform
import re

class DiskSmartInfo:
    def __init__(self):
        self.os = platform.system()

    def run_smartctl(self, device):
        try:
            result = subprocess.run(["smartctl", "-H", device], capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return str(e)

    def get_disks(self):
        if self.os == "Windows":
            # Ejemplo para Windows
            return ["PhysicalDrive0", "PhysicalDrive1"]
        else:
            # Ejemplo en Linux
            return ["/dev/sda", "/dev/sdb"]

    def parse_health(self, output):
        match = re.search(r"SMART overall-health self-assessment test result:\s*(\w+)", output)
        return match.group(1) if match else "Desconocido"

    def getInfo(self):
        disks = self.get_disks()
        smart_data = {}

        for disk in disks:
            device = f"\\\\.\\{disk}" if self.os == "Windows" else disk
            try:
                output = self.run_smartctl(device)

                vida = re.search(r"Percentage Used.*?(\d+)", output)
                horas = re.search(r"Power_On_Hours.*?(\d+)", output)
                sectores = re.search(r"Reallocated_Sector_Ct.*?(\d+)", output)

                estado = {}
                if vida:
                    estado["Vida útil estimada"] = f"{100 - int(vida.group(1))}%"
                if horas:
                    estado["Horas encendido"] = f"{int(horas.group(1))} h"
                if sectores:
                    estado["Sectores reasignados"] = sectores.group(1)

                if estado:
                    smart_data[disk] = estado
                else:
                    smart_data[disk] = "Desconocido"
            except Exception:
                smart_data[disk] = "Desconocido"

        return smart_data
    
    def print(self):
        print("\n------ Estado SMART de los Discos ------")
        info = self.getInfo()
        for disk, estado in info.items():
            print(f"🖴 {disk}")
            if isinstance(estado, dict):
                for k, v in estado.items():
                    print(f"   {k}: {v}")
            else:
                print("   No se pudo obtener información SMART.")