from core.report_data_builder import ReportDataBuilder

def test_build_sections_basic():
    software_info = {
        "os": "Windows 10",
        "architecture": "x64",
        "manufacturer": "Microsoft",
        "registered_user": "Juan"
    }
    cpu_info = {
        "nameCPU": "Intel i5",
        "physicalCore": "4",
        "logicalCore": "8",
        "maxClockSpeed": "3500 MHz",
        "currentUsage": "10%"
    }
    ram_info = {
        "totalMemory": "16 GB",
        "avaliableMemory": "8 GB",
        "percentUsedMemory": "50%",
        "usedMemory": "8 GB",
        "freeMemory": "8 GB"
    }
    slot_info = {
        "totalSlots": 2,
        "usedSlots": 2,
        "freeSlots": 0,
        "detailSlots": ["Slot1: 8 GB", "Slot2: 8 GB"]
    }
    system_info = {
        "manufacturer": "Dell",
        "model": "XPS",
        "baseboard": "Dell Board",
        "baseboardManufacturer": "Dell",
        "biosVersion": "1.0.0",
        "biosDate": "2023-01-01"
    }
    disks = [
        {
            "model": "Samsung SSD",
            "size": "500 GB",
            "used": "200 GB",
            "free": "300 GB",
            "usedPercent": "40%",
            "partitions": 2,
            "media_type": "SSD",
            "serial": "123ABC"
        }
    ]

    sections = ReportDataBuilder.build_sections(software_info, cpu_info, ram_info, slot_info, system_info, disks)
    assert "Información del Usuario" in sections
    assert "Información del CPU" in sections
    assert "Información de Memoria RAM" in sections
    assert "Informacion del Sistema" in sections
    assert "Informacion del Almacenamiento - Disco 1" in sections
    assert sections["Información del CPU"]["Nombre"] == "Intel i5"
    assert sections["Informacion del Almacenamiento - Disco 1"]["Modelo"] == "Samsung SSD"