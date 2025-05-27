from core.software_info import SoftwareInfo
from core.cpu_info import CPUInfo
from core.memory_info import MemoryInfo
from core.storage_info import StorageInfo
from core.user_info import UserInfo
from core.peripherals_info import PeripheralsInfo
from core.system_info import SystemInfo
from core.process_info import ProcessInfo

from data.pdf_generator import PDFGenerator

def main():

    pdf = PDFGenerator()

    #Titulo PDF
    pdf.AddTitle()

    #Datos Usuario
    user_info = UserInfo()
    user_info.print()
    pdf.AddParagraph(user_info.getText())

    #Tabla de Sistema Operativo
    software_info = SoftwareInfo()
    software_info.print()
    info = software_info.getInfo()
    pdf.AddTable("Informacion del Usuario", 
        ["Sistema Operativo", "Arquitectura", "Fabricante", "Usuario Registrado"],
            [[info["os"], info["architecture"], info["manufacturer"], info["registered_user"]]])


    #Tabla de CPU
    cpu_info = CPUInfo()
    cpu_info.print()
    info = cpu_info.getInfo()
    pdf.AddTable("Informacion del CPU",
        ["Nombre", "Nucleos Fisicos", "Nucleos Logicos", "Frecuencia Maxima", "Uso Actual"],
            [[info["nameCPU"], info["physicalCore"], info["logicalCore"], info["maxClockSpeed"], info["currentUsage"]]])

    #Tabla de Memoria RAM
    memory_info = MemoryInfo()
    memory_info.print()
    info = memory_info.getInfo()
    pdf.AddTable("Informacion de Memoria RAM", 
        ["Memoria Total", "Memoria Disponible", "Porcentaje Usado", "Memoria Usada", "Memoria Libre"],
            [[info["totalMemory"], info["avaliableMemory"], info["percentUsedMemory"], info["usedMemory"], info["freeMemory"]]])


    #Tabla del Sistema
    system_info = SystemInfo()
    system_info.print()
    info = system_info.getInfo()
    pdf.AddKeyValueTable("Informacion del Sistema",{
        "Fabricante" : info["manufacturer"],
        "Modelo": info["model"],
        "Placa Base" : info["baseboard"],
        "Fabricante Placa Base" : info["baseboardManufacturer"],
        "Version de Bios" : info["biosVersion"],
        "Fecha de Bios" : info["biosDate"]

    })

    #Tabla de Almacenamiento
    storage_info = StorageInfo()
    storage_info.print()
    disks = storage_info.getInfo()
    for disk in disks:       
        pdf.AddKeyValueTable("Informacion de Almacenamiento",{
        "Modelo": disk["model"],
        "Tamaño": disk["size"],
        "Espacio Usado": disk["used"],
        "Espacio Libre": disk["free"],
        "Porcentaje de Uso": disk["usedPercent"],
        "Número de Serie": disk["serial"],
        "Particiones" : disk["partitions"],
        "Tipo": disk["media_type"]
    })
    
    #Tabla Perifericos
    peripherals_info = PeripheralsInfo()
    peripherals_info.print()

    # Usamos directamente el dict plano
    peripherals_data = peripherals_info.getInfo()

    # Limpieza opcional: convertir listas en strings separados por coma
    peripherals_data_str = {
        k: ", ".join(v) for k, v in peripherals_data.items()
    }

    pdf.AddKeyValueTable("Periféricos Conectados", peripherals_data_str)

    #Tabla de Procesos
    process_info = ProcessInfo()
    process_info.print()
    cabecera, filas = process_info.getInfo()
    pdf.AddTable("Procesos con Mayor Consumo de Recursos", cabecera, filas)


    #Guardar Tablas
    pdf.SaveTable()

if __name__ == "__main__":
    main()