def generate_recommendations(cpu_info, ram_info, storage_info, processes):
    recommendations = []
    # Recomendaciones sobre CPU
    try:
        cpu_usage = float(cpu_info.get("currentUsage", "0").replace('%', ''))
        if cpu_usage > 90:
            recommendations.append("El uso del CPU es extremadamente alto (>90%). Se recomienda cerrar aplicaciones pesadas, revisar procesos en segundo plano y considerar una actualización del procesador si es recurrente.")
        elif cpu_usage > 75:
            recommendations.append("El CPU está siendo utilizado intensamente (>75%). Supervise los procesos activos y considere optimizar el arranque del sistema.")
        # No mostrar mensaje si el uso es bajo
    except Exception:
        recommendations.append("No se pudo analizar el uso del CPU.")

    # Recomendaciones sobre RAM
    try:
        ram_available = float(ram_info.get("avaliableMemory", "0").replace(' GB', ''))
        ram_total = float(ram_info.get("totalMemory", "0").replace(' GB', ''))
        ram_percent = float(ram_info.get("percentUsedMemory", "0").replace('%', ''))
        if ram_available < 2:
            recommendations.append("La memoria RAM disponible es muy baja (<2 GB). Cierre aplicaciones o considere ampliar la memoria RAM.")
        elif ram_percent > 85:
            recommendations.append("La RAM está siendo utilizada en más del 85%. Considere optimizar el uso de programas o ampliar la capacidad de RAM.")
        elif ram_total < 4:
            recommendations.append("La memoria RAM total es baja (<4 GB). Se recomienda actualizar la RAM para un mejor rendimiento.")
        # No mostrar mensaje si el uso es bajo
    except Exception:
        recommendations.append("No se pudo analizar el uso de la memoria RAM.")

    # Recomendaciones sobre almacenamiento (solo si hay alerta)
    try:
        for disk in storage_info:
            usage = float(disk.get("usedPercent", "0").replace('%', ''))
            free = float(disk.get("free", "0").replace(' GB', ''))
            model = disk.get('model', 'Desconocido')
            if usage > 90:
                recommendations.append(f"El disco '{model}' está casi lleno (>90% usado). Libere espacio eliminando archivos temporales o transfiriendo datos a otro medio.")
            elif free < 10:
                recommendations.append(f"El disco '{model}' tiene menos de 10 GB disponibles. Considere liberar espacio o agregar una unidad de almacenamiento adicional.")
            if disk.get("media_type", "").lower().startswith("hdd"):
                recommendations.append(f"El disco '{model}' es un HDD. Considere migrar a un SSD para mejorar el rendimiento.")
        # No mostrar mensaje si el disco tiene suficiente espacio
    except Exception:
        recommendations.append("No se pudo analizar el estado de los discos de almacenamiento.")

    # Recomendaciones sobre procesos (filtra procesos del sistema y solo muestra los relevantes)
    try:
        high_cpu_processes = []
        high_mem_processes = []
        multiple_instances_processes = []
        system_processes = {"svchost.exe", "MemCompression", "WmiPrvSE.exe"}
        for process in processes:
            name, instances, cpu, ram, memory = process
            if name in system_processes:
                continue  # omitir procesos del sistema conocidos
            try:
                cpu_val = float(cpu)
                mem_val = float(memory.replace(' MB', ''))
                inst = int(instances)
                if cpu_val > 30:
                    high_cpu_processes.append((name, cpu_val))
                if mem_val > 500:
                    high_mem_processes.append((name, mem_val))
                if inst > 5:
                    multiple_instances_processes.append((name, inst))
            except Exception:
                continue

        if high_cpu_processes:
            for name, cpu_val in high_cpu_processes:
                recommendations.append(f"El proceso '{name}' está consumiendo mucha CPU ({cpu_val}%). Revise si es necesario o puede ser optimizado.")
        if high_mem_processes:
            for name, mem_val in high_mem_processes:
                recommendations.append(f"El proceso '{name}' está consumiendo mucha memoria ({mem_val:.1f} MB). Considere cerrarlo si no es esencial.")
        if multiple_instances_processes:
            for name, inst in multiple_instances_processes:
                recommendations.append(f"Hay múltiples instancias del proceso '{name}' ({inst} instancias). Esto puede indicar un problema o un uso intensivo.")
        # No mostrar mensaje si no hay procesos problemáticos
    except Exception:
        recommendations.append("No se pudo analizar el consumo de recursos por procesos.")

    # Recomendaciones generales
    recommendations.append("Recuerde mantener su sistema operativo y programas actualizados para mayor seguridad y rendimiento.")
    recommendations.append("Realice mantenimientos periódicos: limpieza de archivos temporales, desfragmentación (si usa HDD) y revisión de programas de inicio.")