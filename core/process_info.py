import psutil
from collections import defaultdict

class ProcessInfo:
    def __init__(self):
        pass

    def get_info(self, top_n=10):
        """
        Devuelve una tabla con los procesos que más recursos consumen.
        """
        grouped = defaultdict(lambda: {'cpu': 0.0, 'ram': 0.0, 'count': 0, 'mem_real': 0.0})

        for proc in psutil.process_iter(['name', 'pid']):
            try:
                name = proc.info['name']
                if not name or "idle" in name.lower():
                    continue

                cpu = proc.cpu_percent(interval=0.1)
                mem_percent = proc.memory_percent()
                mem_real = proc.memory_info().rss / (1024 ** 2)  # en MB

                g = grouped[name]
                g['cpu'] += cpu
                g['ram'] += mem_percent
                g['mem_real'] += mem_real
                g['count'] += 1

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # Convertir a lista y ordenar por RAM y CPU combinadas
        summary = sorted(grouped.items(), key=lambda x: (x[1]['mem_real'], x[1]['cpu']), reverse=True)

        header = ["Proceso", "Instancias", "CPU (%)", "RAM (%)", "Memoria Total (MB)"]
        rows = []

        for name, stats in summary[:top_n]:
            rows.append([
                name,
                str(stats['count']),
                f"{stats['cpu']:.1f}",
                f"{stats['ram']:.1f}",
                f"{stats['mem_real']:.1f} MB"
            ])

        return header, rows