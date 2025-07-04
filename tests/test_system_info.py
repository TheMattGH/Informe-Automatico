import pytest
from unittest.mock import patch, MagicMock
from core.system_info import SystemInfo

@patch("core.system_info.wmi.WMI")
def test_get_info_system_info(mock_wmi):
    # Mock system, baseboard, and bios objects
    mock_system = MagicMock()
    mock_system.Manufacturer = "Dell "
    mock_system.Model = "XPS 15 "
    mock_baseboard = MagicMock()
    mock_baseboard.Product = "0ABC123 "
    mock_baseboard.Manufacturer = "Dell Inc. "
    mock_bios = MagicMock()
    mock_bios.SMBIOSBIOSVersion = "1.2.3 "
    mock_bios.ReleaseDate = "20240101.000000+000"

    # Mock WMI instance
    mock_wmi_instance = MagicMock()
    mock_wmi_instance.Win32_ComputerSystem.return_value = [mock_system]
    mock_wmi_instance.Win32_BaseBoard.return_value = [mock_baseboard]
    mock_wmi_instance.Win32_BIOS.return_value = [mock_bios]
    mock_wmi.return_value = mock_wmi_instance

    si = SystemInfo()
    info = si.get_info()
    assert info == {
        "manufacturer": "Dell",
        "model": "XPS 15",
        "baseboard": "0ABC123",
        "baseboardManufacturer": "Dell Inc.",
        "biosVersion": "1.2.3",
        "biosDate": "20240101"
    }