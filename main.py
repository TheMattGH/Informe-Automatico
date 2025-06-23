from core.software_info import SoftwareInfo
from core.cpu_info import CPUInfo
from core.memory_info import MemoryInfo
from core.storage_info import StorageInfo
from core.user_info import UserInfo
from core.peripherals_info import PeripheralsInfo
from core.system_info import SystemInfo
from core.process_info import ProcessInfo 
from core.smart_status import DiskSmartInfo

import time
from data.pdf_generator import PDFGenerator

start_time = time.time()

def main():

    pdf = PDFGenerator()

    #Datos Usuario
    user_info = UserInfo()
    user_info.print()
    pdf.AddParagraph(user_info.getText())

    # #Tabla de Sistema Operativo
    # software_info = SoftwareInfo()
    # software_info.print()
    # info = software_info.getInfo()
    # pdf.AddTable("Informacion del Usuario", 
    #     ["Sistema Operativo", "Arquitectura", "Fabricante", "Usuario Registrado"],
    #         [[info["os"], info["architecture"], info["manufacturer"], info["registered_user"]]])

    software_info = SoftwareInfo().getInfo()
    cpu_info = CPUInfo().getInfo()
    memory_info = MemoryInfo()
    ram_info = memory_info.getInfo()
    slot_info = memory_info.getSlotInfo()
    system_info = SystemInfo().getInfo()   
    process_info = ProcessInfo()
    cabecera, filas = process_info.getInfo() 
    
    secciones = {
    "Información del Usuario": {
        "Sistema Operativo": software_info["os"],
        "Arquitectura": software_info["architecture"],
        "Fabricante": software_info["manufacturer"],
        "Usuario Registrado": software_info["registered_user"]
    },
    "Información del CPU": {
        "Nombre": cpu_info["nameCPU"],
        "Núcleos Físicos": cpu_info["physicalCore"],
        "Núcleos Lógicos": cpu_info["logicalCore"],
        "Frecuencia Máxima": cpu_info["maxClockSpeed"],
        "Uso Actual": cpu_info["currentUsage"]
    },
    "Información de Memoria RAM": {
        "Memoria Total": ram_info["totalMemory"],
        "Memoria Disponible": ram_info["avaliableMemory"],
        "Porcentaje Usado": ram_info["percentUsedMemory"],
        "Memoria Usada": ram_info["usedMemory"],
        "Memoria Libre": ram_info["freeMemory"],
        "Total Slots": slot_info["totalSlots"],
        "Slots Usados": slot_info["usedSlots"],
        "Slots Libres": slot_info["freeSlots"],
        "Detalles por Slot": slot_info["detailSlots"]
    }, 
    "Informacion del Sistema" : {
        "Fabricante" : system_info["manufacturer"],
        "Modelo" : system_info["model"],
        "Placa Base" : system_info["baseboard"],
        "Fabricante Placa Base" : system_info["baseboardManufacturer"],
        "Version de BIOS" : system_info["biosVersion"],
        "Fecha de BIOS" : system_info["biosDate"]
    },
}
    storage = StorageInfo()
    discos = storage.getInfo()

    for i, disco in enumerate(discos, start=1):
        secciones[f"Informacion del Almacenamiento - Disco {i}"] = {
            "Modelo": disco["model"],
            "Tamaño": disco["size"],
            "Espacio Usado": disco["used"],
            "Espacio Libre": disco["free"],
            "Porcentaje de Uso": disco["usedPercent"],
            "Número de Serie": disco["serial"],
            "Tipo": disco["media_type"],
            "Particiones": disco["partitions"],
            "Tipo de Almacenamiento" : disco["media_type"]
        }
    
    # smart = DiskSmartInfo()
    # smart.print()
    # smart_data = smart.getInfo()

    # for nombre_disco, estado in smart_data.items():
    #     if isinstance(estado, dict):
    #         secciones[f"Estado SMART - {nombre_disco}"] = {
    #             "Estado General": estado.get("estado", "Desconocido"),
    #             "Detalles": estado.get("detalles", [])
    #         }
    #     else:
    #         # En caso de error o estado como string directo
    #         secciones[f"Estado SMART - {nombre_disco}"] = {
    #             "Estado General": "No disponible",
    #             "Detalles": [estado]  # lo convertimos en lista para que se vea como viñeta
    #         }
    peripherals_info = PeripheralsInfo()
    peripherals_info.print()

    peripherals_data = peripherals_info.getInfo()

    # Convertimos listas a texto tipo viñetas (o separados por coma si prefieres)
    peripherals_data_formateado = {}
    for k, v in peripherals_data.items():
        if isinstance(v, list):
            peripherals_data_formateado[k] = v  # Lista, se mostrará como viñetas
        else:
            peripherals_data_formateado[k] = str(v)



    
    pdf.generar_bloques_formato_fijo(secciones)
    pdf.agregar_perifericos_formato_tabla(peripherals_data_formateado)
    pdf.agregar_tabla_procesos_texto(cabecera, filas)









    # #Tabla de CPU
    # cpu_info = CPUInfo()
    # cpu_info.print()
    # info = cpu_info.getInfo()
    # pdf.AddTable("Informacion del CPU",
    #     ["Nombre", "Nucleos Fisicos", "Nucleos Logicos", "Frecuencia Maxima", "Uso Actual"],
    #         [[info["nameCPU"], info["physicalCore"], info["logicalCore"], info["maxClockSpeed"], info["currentUsage"]]])

    # #Tabla de Memoria RAM
    # memory_info = MemoryInfo()
    # memory_info.print()
    # info = memory_info.getInfo()
    # pdf.AddTable("Informacion de Memoria RAM", 
    #     ["Memoria Total", "Memoria Disponible", "Porcentaje Usado", "Memoria Usada", "Memoria Libre"],
    #         [[info["totalMemory"], info["avaliableMemory"], info["percentUsedMemory"], info["usedMemory"], info["freeMemory"]]])
    # slotInfo = memory_info.getSlotInfo()
    # detalles_slot_multilinea = "\n".join(slotInfo["detailSlots"])
    # pdf.AddTable("Slots de Memoria RAM", 
    #     ["Total Slots", "Slots Usados", "Slots Libres", "Detalles de Slots"], 
    #              [[slotInfo["totalSlots"], slotInfo["usedSlots"], slotInfo["freeSlots"], detalles_slot_multilinea]])

    # #Tabla del Sistema
    # system_info = SystemInfo()
    # system_info.print()
    # info = system_info.getInfo()
    # pdf.AddKeyValueTable("Informacion del Sistema",{
    #     "Fabricante" : info["manufacturer"],
    #     "Modelo": info["model"],
    #     "Placa Base" : info["baseboard"],
    #     "Fabricante Placa Base" : info["baseboardManufacturer"],
    #     "Version de Bios" : info["biosVersion"],
    #     "Fecha de Bios" : info["biosDate"]

    # })

    #Tabla de Almacenamiento
    # storage_info = StorageInfo()
    # storage_info.print()
    # disks = storage_info.getInfo()
    # for disk in disks:       
    #     pdf.AddKeyValueTable("Informacion de Almacenamiento",{
    #     "Modelo": disk["model"],
    #     "Tamaño": disk["size"],
    #     "Espacio Usado": disk["used"],
    #     "Espacio Libre": disk["free"],
    #     "Porcentaje de Uso": disk["usedPercent"],
    #     "Número de Serie": disk["serial"],
    #     "Particiones" : disk["partitions"],
    #     "Tipo": disk["media_type"]
    # })
    
    # smart = DiskSmartInfo()
    # smart.print() 
    # data = smart.getInfo()
    # pdf.AddSmartStatus(data)        

    # #Tabla Perifericos
    # peripherals_info = PeripheralsInfo()
    # peripherals_info.print()

    # # Usamos directamente el dict plano
    # peripherals_data = peripherals_info.getInfo()

    # # Limpieza opcional: convertir listas en strings separados por coma
    # peripherals_data_str = {
    #     k: ", ".join(v) for k, v in peripherals_data.items()
    # }

    # pdf.AddKeyValueTable("Periféricos Conectados", peripherals_data_str)

    #Tabla de Procesos
    # process_info = ProcessInfo()
    # process_info.print()
    # cabecera, filas = process_info.getInfo()
    # pdf.AddTable("Procesos con Mayor Consumo de Recursos", cabecera, filas)


    #Guardar Tablas
    pdf.SaveTable()

if __name__ == "__main__":
    main()

end_time = time.time()
print(f"\n🕒 Tiempo de ejecución: {end_time - start_time:.2f} segundos")