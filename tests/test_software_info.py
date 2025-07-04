import pytest
from unittest.mock import patch, MagicMock
from core.software_info import SoftwareInfo

@patch("core.software_info.wmi.WMI")
def test_get_info_returns_expected_dict(mock_wmi):
    # Mock the OS info object
    mock_os_info = MagicMock()
    mock_os_info.Caption = "Microsoft Windows 10 Pro"
    mock_os_info.Version = "10.0.19045"
    mock_os_info.OSArchitecture = "64-bit"
    mock_os_info.Manufacturer = "Microsoft Corporation"
    mock_os_info.RegisteredUser = "Usuario"

    # Mock the WMI instance and its method
    mock_wmi_instance = MagicMock()
    mock_wmi_instance.Win32_OperatingSystem.return_value = [mock_os_info]
    mock_wmi.return_value = mock_wmi_instance

    # Instantiate and test
    si = SoftwareInfo()
    info = si.get_info()

    assert info == {
        "os": "Microsoft Windows 10 Pro 10.0.19045",
        "architecture": "64-bit",
        "manufacturer": "Microsoft Corporation",
        "registered_user": "Usuario"
    }