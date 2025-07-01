import wmi
import psutil

class StorageInfo:
    """
    Clase para obtener información detallada de los discos de almacenamiento del sistema.
    """

    def __init__(self):
        self.c = wmi.WMI()
    
    def get_info(self):
        """
        Devuelve una lista de diccionarios con información relevante de cada disco.
        """
        disks = []

        for disk in self.c.Win32_DiskDrive():
            total_physical = int(disk.Size)
            model = disk.Model
            serial = disk.SerialNumber if disk.SerialNumber else "No disponible"
            media_type = disk.MediaType if disk.MediaType else "Desconocido"
            partitions = disk.Partitions

            # Buscar letras de unidad conectadas a este disco
            mountpoints = []
            for partition in disk.associators("Win32_DiskDriveToDiskPartition"):
                for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                    mountpoints.append(logical_disk.DeviceID + "\\")

            total_used = 0
            total_free = 0
            total_logical = 0

            for mount in mountpoints:
                try:
                    usage = psutil.disk_usage(mount)
                    total_used += usage.used
                    total_free += usage.free
                    total_logical += usage.total
                except Exception:
                    continue  # si alguna partición lanza error, ignorarla

            if total_logical > 0:
                used_percent = f"{(total_used / total_logical) * 100:.1f}%"
            else:
                used_percent = "No disponible"

            disk_data = {
                "model": model,
                "size": f"{total_physical / (1024**3):.2f} GB",
                "logical_total": f"{total_logical / (1024**3):.2f} GB",
                "used": f"{total_used / (1024**3):.2f} GB",
                "free": f"{total_free / (1024**3):.2f} GB",
                "usedPercent": used_percent,
                "partitions": partitions,
                "media_type": media_type,
                "serial": serial
            }

            disks.append(disk_data)

        return disks