import pytest
from unittest.mock import patch, MagicMock
from core.memory_info import MemoryInfo

@patch("core.memory_info.psutil.virtual_memory")
@patch("core.memory_info.wmi.WMI")
def test_get_info_memory(mock_wmi, mock_virtual_memory):
    # Mock psutil.virtual_memory
    mock_mem = MagicMock()
    mock_mem.total = 8 * 1024**3
    mock_mem.available = 4 * 1024**3
    mock_mem.percent = 50
    mock_mem.used = 4 * 1024**3
    mock_mem.free = 4 * 1024**3
    mock_virtual_memory.return_value = mock_mem

    mi = MemoryInfo()
    info = mi.get_info()
    assert info == {
        "totalMemory": "8.00 GB",
        "avaliableMemory": "4.00 GB",
        "percentUsedMemory": "50%",
        "usedMemory": "4.00 GB",
        "freeMemory": "4.00 GB"
    }

@patch("core.memory_info.wmi.WMI")
def test_get_slot_info_memory(mock_wmi):
    # Mock Win32_PhysicalMemoryArray
    mock_mem_array = MagicMock()
    mock_mem_array.MemoryDevices = 2
    # Mock Win32_PhysicalMemory
    mock_mem1 = MagicMock()
    mock_mem1.Capacity = str(4 * 1024**3)
    mock_mem1.DeviceLocator = "DIMM1"
    mock_mem2 = MagicMock()
    mock_mem2.Capacity = str(4 * 1024**3)
    mock_mem2.DeviceLocator = "DIMM2"

    mock_wmi_instance = MagicMock()
    mock_wmi_instance.Win32_PhysicalMemoryArray.return_value = [mock_mem_array]
    mock_wmi_instance.Win32_PhysicalMemory.return_value = [mock_mem1, mock_mem2]
    mock_wmi.return_value = mock_wmi_instance

    mi = MemoryInfo()
    result = mi.get_slot_info()
    assert result == {
        "totalSlots": 2,
        "usedSlots": 2,
        "freeSlots": 0,
        "detailSlots": ["DIMM1: 4.00 GB", "DIMM2: 4.00 GB"]
    }

@patch("core.memory_info.wmi.WMI")
def test_get_slot_info_memory_handles_exception(mock_wmi):
    mock_wmi_instance = MagicMock()
    mock_wmi_instance.Win32_PhysicalMemoryArray.side_effect = Exception("fail")
    mock_wmi.return_value = mock_wmi_instance

    mi = MemoryInfo()
    result = mi.get_slot_info()
    assert "Error" in result