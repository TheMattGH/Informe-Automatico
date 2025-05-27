import psutil

class ProcessInfo:
    def __init__(self):
        pass

    def getInfo(self, topN = 10):
        processes = []

        for proc in psutil.process_iter(['name', 'pid', 'cpu_percent', 'memory_percent']):
            try:
                info = proc.info
                processes.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        processes.sort(key=lambda x: (x['cpu_percent'], x['memory_percent']), reverse=True)
        top_processes = processes[:topN]

        cabecera = ["Nombre", "CPU (%)", "RAM (%)"]
        filas = []

        for p in top_processes:
            nombre = f"{p['name']} (PID: {p['pid']})"
            cpu = f"{p['cpu_percent']:.1f}"
            ram = f"{p['memory_percent']:.1f}"
            filas.append([nombre, cpu, ram])

        return cabecera, filas
    
    def print(self):
        print("------ Procesos con Mayor Consumo de Recursos ------")
        cabecera, filas = self.getInfo()
        
        print(f"{cabecera[0]:<45} {cabecera[1]:<10} {cabecera[2]}")
        for fila in filas:
            print(f"{fila[0]:<45} {fila[1]:<10} {fila[2]}")
        print()