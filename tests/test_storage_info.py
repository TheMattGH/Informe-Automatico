import pytest
from unittest.mock import patch, MagicMock
from core.storage_info import StorageInfo

@patch("core.storage_info.psutil.disk_usage")
@patch("core.storage_info.wmi.WMI")
def test_get_info_storage_info(mock_wmi, mock_disk_usage):
    # Mock disk object
    mock_disk = MagicMock()
    mock_disk.Size = str(500 * 1024**3)  # 500 GB
    mock_disk.Model = "Samsung SSD"
    mock_disk.SerialNumber = "123ABC"
    mock_disk.MediaType = "SSD"
    mock_disk.Partitions = 2

    # Mock partition and logical disk
    mock_partition = MagicMock()
    mock_logical_disk = MagicMock()
    mock_logical_disk.DeviceID = "C:"

    mock_partition.associators.return_value = [mock_logical_disk]
    mock_disk.associators.return_value = [mock_partition]

    # Mock WMI instance
    mock_wmi_instance = MagicMock()
    mock_wmi_instance.Win32_DiskDrive.return_value = [mock_disk]
    mock_wmi.return_value = mock_wmi_instance

    # Mock psutil.disk_usage
    mock_usage = MagicMock()
    mock_usage.used = 100 * 1024**3
    mock_usage.free = 400 * 1024**3
    mock_usage.total = 500 * 1024**3
    mock_disk_usage.return_value = mock_usage

    si = StorageInfo()
    disks = si.get_info()
    assert len(disks) == 1
    disk = disks[0]
    assert disk["model"] == "Samsung SSD"
    assert disk["size"] == "500.00 GB"
    assert disk["logical_total"] == "500.00 GB"
    assert disk["used"] == "100.00 GB"
    assert disk["free"] == "400.00 GB"
    assert disk["usedPercent"] == "20.0%"
    assert disk["partitions"] == 2
    assert disk["media_type"] == "SSD"
    assert disk["serial"] == "123ABC"