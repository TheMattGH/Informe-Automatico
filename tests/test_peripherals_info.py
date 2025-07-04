import pytest
from unittest.mock import patch, MagicMock
from core.peripherals_info import PeripheralsInfo

@patch("core.peripherals_info.get_monitors")
@patch("core.peripherals_info.wmi.WMI")
def test_get_info_peripherals(mock_wmi, mock_get_monitors):
    # Mock monitors
    mock_monitor = MagicMock()
    mock_monitor.width = 1920
    mock_monitor.height = 1080
    mock_get_monitors.return_value = [mock_monitor]

    # Mock WMI instance and entities
    mock_wmi_instance = MagicMock()
    # Monitores
    mock_pnp_entity = MagicMock()
    mock_pnp_entity.Name = "Generic Monitor"
    mock_wmi_instance.Win32_PnPEntity.return_value = [mock_pnp_entity]
    # Impresoras
    mock_printer = MagicMock()
    mock_printer.Name = "HP LaserJet"
    mock_printer.DriverName = "HP Driver"
    mock_printer.PortName = "USB001"
    mock_printer.WorkOffline = False
    mock_wmi_instance.Win32_Printer.return_value = [mock_printer]
    # Teclados
    mock_keyboard = MagicMock()
    mock_keyboard.Description = "Standard Keyboard"
    mock_wmi_instance.Win32_Keyboard.return_value = [mock_keyboard]
    # Ratones
    mock_mouse = MagicMock()
    mock_mouse.Description = "USB Mouse"
    mock_wmi_instance.Win32_PointingDevice.return_value = [mock_mouse]
    # Cámaras
    mock_cam = MagicMock()
    mock_cam.Name = "USB Camera"
    mock_cam.Manufacturer = "Logitech"
    mock_wmi_instance.Win32_PnPEntity.return_value = [mock_pnp_entity, mock_cam]
    # Sonido
    mock_sound = MagicMock()
    mock_sound.Name = "Realtek Audio"
    mock_sound.Manufacturer = "Realtek"
    mock_wmi_instance.Win32_SoundDevice.return_value = [mock_sound]
    # USB
    mock_disk = MagicMock()
    mock_disk.InterfaceType = "USB"
    mock_disk.Size = str(16 * 1024**3)
    mock_disk.Model = "SanDisk USB"
    mock_wmi_instance.Win32_DiskDrive.return_value = [mock_disk]
    mock_wmi.return_value = mock_wmi_instance

    pi = PeripheralsInfo()
    info = pi.get_info()
    assert "Monitores" in info
    assert "Impresoras" in info
    assert "Teclados" in info
    assert "Ratones" in info
    assert "Cámaras" in info
    assert "Audio" in info
    assert "Dispositivos USB" in info
    assert info["Monitores"][0].endswith("(1920x1080)")
    assert "HP LaserJet" in info["Impresoras"][0]
    assert "Standard Keyboard" in info["Teclados"][0]
    assert "USB Mouse" in info["Ratones"][0]
    assert "USB Camera" in info["Cámaras"][0]
    assert "Realtek Audio" in info["Audio"][0]
    assert "SanDisk USB" in info["Dispositivos USB"][0]

def test_format_for_report():
    data = {
        "Monitores": ["Monitor1"],
        "Impresoras": ["Printer1"],
        "Teclados": ["Keyboard1"],
        "Ratones": ["Mouse1"],
        "Cámaras": ["Cam1"],
        "Audio": ["Audio1"],
        "Dispositivos USB": ["USB1"]
    }
    formatted = PeripheralsInfo.format_for_report(data)
    assert formatted == data