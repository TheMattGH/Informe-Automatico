from core.recommendations import generate_recommendations

def test_generate_recommendations_high_cpu():
    cpu_info = {"currentUsage": "95%"}
    ram_info = {"avaliableMemory": "8", "totalMemory": "16", "percentUsedMemory": "50"}
    storage_info = [{"usedPercent": "50", "free": "100", "model": "Disco1", "media_type": "SSD"}]
    processes = []

    recs = generate_recommendations(cpu_info, ram_info, storage_info, processes)
    assert any("CPU" in r for r in recs)

def test_generate_recommendations_low_ram():
    cpu_info = {"currentUsage": "10%"}
    ram_info = {"avaliableMemory": "1", "totalMemory": "4", "percentUsedMemory": "90"}
    storage_info = [{"usedPercent": "50", "free": "100", "model": "Disco1", "media_type": "SSD"}]
    processes = []

    recs = generate_recommendations(cpu_info, ram_info, storage_info, processes)
    assert any("RAM disponible es muy baja" in r or "RAM está siendo utilizada" in r for r in recs)