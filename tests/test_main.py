import pytest
from unittest.mock import patch, MagicMock
from src.main import main

@patch("src.main.PDFGenerator")
@patch("src.main.apply_template")
@patch("src.main.ReportDataBuilder")
@patch("src.main.UserInfo")
@patch("src.main.SoftwareInfo")
@patch("src.main.CPUInfo")
@patch("src.main.MemoryInfo")
@patch("src.main.SystemInfo")
@patch("src.main.ProcessInfo")
@patch("src.main.StorageInfo")
@patch("src.main.PeripheralsInfo")
@patch("src.main.generate_recommendations")
def test_main_success(mock_generate_recommendations, mock_PeripheralsInfo, mock_StorageInfo, mock_ProcessInfo,
                      mock_SystemInfo, mock_MemoryInfo, mock_CPUInfo, mock_SoftwareInfo, mock_UserInfo,
                      mock_ReportDataBuilder, mock_apply_template, mock_PDFGenerator):
    # Configura el mock para ProcessInfo.get_info()
    mock_process_info_instance = MagicMock()
    mock_process_info_instance.get_info.return_value = (
        ["Proceso", "Instancias", "CPU (%)", "RAM (%)", "Memoria Total (MB)"],
        [["explorer.exe", "1", "10.0", "5.0", "100.0 MB"]]
        )
    mock_ProcessInfo.return_value = mock_process_info_instance

    result = main("Test User", "IT")
    assert result is None or result is True

@patch("src.main.PDFGenerator")
@patch("src.main.apply_template", side_effect=Exception("fail"))
@patch("src.main.ReportDataBuilder")
@patch("src.main.UserInfo")
@patch("src.main.SoftwareInfo")
@patch("src.main.CPUInfo")
@patch("src.main.MemoryInfo")
@patch("src.main.SystemInfo")
@patch("src.main.ProcessInfo")
@patch("src.main.StorageInfo")
@patch("src.main.PeripheralsInfo")
@patch("src.main.generate_recommendations")

def test_main_error(*mocks):
    result = main("Test User", "IT")
    assert result is None or result is False