from core.software_info import SoftwareInfo
from core.cpu_info import CPUInfo
from core.memory_info import MemoryInfo
from core.storage_info import StorageInfo
from core.user_info import UserInfo
from core.peripherals_info import PeripheralsInfo
from core.system_info import SystemInfo
from core.process_info import ProcessInfo 
from core.recomendations import generar_recomendaciones

import time
from data.pdf_generator import PDFGenerator
from pdfrw import PdfReader, PdfWriter, PageMerge

start_time = time.time()

def main():

    #Generar pdf
    pdf = PDFGenerator(document_name="informe_contenido.pdf")
    pdf.add_tittle("INFORME TECNICO DEL SISTEMA")

    #Datos Informe
    user_info = UserInfo()
    user_info.print()
    pdf.add_paragraph(user_info.getText(), "Datos del Informe")

    #Creacion de las tablas de Informacion
    software_info = SoftwareInfo().getInfo()
    cpu_info = CPUInfo().getInfo()
    memory_info = MemoryInfo()
    ram_info = memory_info.getInfo()
    slot_info = memory_info.getSlotInfo()
    system_info = SystemInfo().getInfo()   
    process_info = ProcessInfo()
    header, rows = process_info.getInfo() 
    
    sections = {
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
    disks = storage.getInfo()

    for i, disk in enumerate(disks, start=1):
        sections[f"Informacion del Almacenamiento - Disco {i}"] = {
            "Modelo": disk["model"],
            "Tamaño": disk["size"],
            "Espacio Usado":disk["used"],
            "Espacio Libre": disk["free"],
            "Porcentaje de Uso": disk["usedPercent"],
            "Número de Serie": disk["serial"],
            "Tipo": disk["media_type"],
            "Particiones": disk["partitions"],
            "Tipo de Almacenamiento" : disk["media_type"]
        }
    
    peripherals_info = PeripheralsInfo()
    peripherals_info.print()

    peripherals_data = peripherals_info.getInfo()

    peripherals_data_formatted = {}
    for k, v in peripherals_data.items():
        if isinstance(v, list):
            peripherals_data_formatted[k] = v 
        else:
            peripherals_data_formatted[k] = str(v)

    pdf.generate_blocks(sections)
    pdf.add_peripherals_block(peripherals_data_formatted)
    pdf.add_processes_block(header, rows)
    recomendaciones = generar_recomendaciones(cpu_info, ram_info, disks, rows)
    recomendaciones_html = "<br/>".join(f"• {r}" for r in recomendaciones)
    pdf.add_paragraph(recomendaciones_html, "Recomendaciones del Sistema")


    #Aplicar la plantilla sobre el informe generado
    def apply_template(plantilla_path, informe_path, salida_path):
            plantilla = PdfReader(plantilla_path).pages
            informe = PdfReader(informe_path).pages

            for i, page in enumerate(informe):
                fondo = plantilla[0]  # Usa la primera pagina como fondo para todas
                merger = PageMerge(page)
                merger.add(fondo, prepend=True).render()

            writer = PdfWriter()
            writer.addpages(informe)
            writer.write(salida_path)

    #Guardar pdf
    pdf.save_document()
    apply_template("plantilla.pdf", "informe_contenido.pdf", "informe_final.pdf")


if __name__ == "__main__":
    main()

end_time = time.time()
print(f"\n🕒 Tiempo de ejecución: {end_time - start_time:.2f} segundos")