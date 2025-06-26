
def generate_recomendations(cpu_info, ram_info, storage_info, processes):
    recomendaciones = []

    # Recomendaciones sobre CPU
    uso_cpu = float(cpu_info["currentUsage"].replace('%', ''))
    if uso_cpu > 85:
        recomendaciones.append("🔧 Alto uso del CPU detectado (>85%). Se recomienda cerrar aplicaciones en segundo plano innecesarias o considerar una actualización del procesador si el problema persiste.")
    elif uso_cpu > 60:
        recomendaciones.append("⚠️ Uso moderado del CPU detectado (>60%). Supervise los procesos activos que pueden estar generando carga.")

    # Recomendaciones sobre RAM
    ram_disponible = float(ram_info["avaliableMemory"].replace(' GB', ''))
    if ram_disponible < 2:
        recomendaciones.append("🔧 La memoria RAM disponible es muy baja (<2 GB). Se recomienda cerrar aplicaciones o aumentar la memoria RAM del sistema.")
    elif float(ram_info["percentUsedMemory"].replace('%', '')) > 80:
        recomendaciones.append("⚠️ La RAM está siendo usada en más del 80%. Se sugiere optimizar el uso de programas o ampliar la capacidad de RAM.")

    # Recomendaciones sobre almacenamiento
    for disk in storage_info:
        uso = float(disk["usedPercent"].replace('%', ''))
        libre = float(disk["free"].replace(' GB', ''))
        if uso > 90:
            recomendaciones.append(f"🔧 El disco '{disk['model']}' está casi lleno (>90% usado). Libere espacio eliminando archivos temporales o transfiriendo datos a otro medio.")
        elif libre < 10:
            recomendaciones.append(f"⚠️ El disco '{disk['model']}' tiene menos de 10 GB disponibles. Considere liberar espacio o agregar una unidad de almacenamiento adicional.")

    # Recomendaciones sobre procesos
    for proceso in processes:
        nombre, instancias, cpu, ram, memoria = proceso
        if float(cpu) > 30 or float(memoria.replace(' MB', '')) > 500:
            recomendaciones.append(f"🔎 El proceso '{nombre}' consume recursos significativamente (CPU: {cpu}%, Memoria: {memoria}). Verifique si es necesario o puede ser optimizado.")

    return recomendaciones
