class ReportDataBuilder:
    @staticmethod
    def build_sections(software_info, cpu_info, ram_info, slot_info, system_info, disks):
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
            "Informacion del Sistema": {
                "Fabricante": system_info["manufacturer"],
                "Modelo": system_info["model"],
                "Placa Base": system_info["baseboard"],
                "Fabricante Placa Base": system_info["baseboardManufacturer"],
                "Version de BIOS": system_info["biosVersion"],
                "Fecha de BIOS": system_info["biosDate"]
            },
        }

        for i, disk in enumerate(disks, start=1):
            sections[f"Informacion del Almacenamiento - Disco {i}"] = {
                "Modelo": disk["model"],
                "Tamaño": disk["size"],
                "Espacio Usado": disk["used"],
                "Espacio Libre": disk["free"],
                "Porcentaje de Uso": disk["usedPercent"],
                "Número de Serie": disk["serial"],
                "Tipo": disk["media_type"],
                "Particiones": disk["partitions"],
                "Tipo de Almacenamiento": disk["media_type"]
            }
        return sections