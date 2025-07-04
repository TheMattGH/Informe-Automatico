from unittest.mock import patch, MagicMock
from core.process_info import ProcessInfo

@patch('core.process_info.psutil.process_iter')
def test_get_info_basic(mock_process_iter):
    # Simula dos procesos con el mismo nombre
    proc1 = MagicMock()
    proc1.info = {'name': 'chrome', 'pid': 1}
    proc1.cpu_percent.return_value = 10.0
    proc1.memory_percent.return_value = 5.0
    proc1.memory_info.return_value = MagicMock(rss=100 * 1024 * 1024)  # 100 MB

    proc2 = MagicMock()
    proc2.info = {'name': 'chrome', 'pid': 2}
    proc2.cpu_percent.return_value = 20.0
    proc2.memory_percent.return_value = 10.0
    proc2.memory_info.return_value = MagicMock(rss=200 * 1024 * 1024)  # 200 MB

    proc3 = MagicMock()
    proc3.info = {'name': 'python', 'pid': 3}
    proc3.cpu_percent.return_value = 5.0
    proc3.memory_percent.return_value = 2.0
    proc3.memory_info.return_value = MagicMock(rss=50 * 1024 * 1024)  # 50 MB

    mock_process_iter.return_value = [proc1, proc2, proc3]

    pi = ProcessInfo()
    header, rows = pi.get_info(top_n=2)

    assert header == ["Proceso", "Instancias", "CPU (%)", "RAM (%)", "Memoria Total (MB)"]
    assert any("chrome" in row for row in [r[0] for r in rows])
    assert any("python" in row for row in [r[0] for r in rows])
    # chrome debe tener 2 instancias, cpu 30.0, ram 15.0, memoria 300 MB
    chrome_row = next(row for row in rows if row[0] == "chrome")
    assert chrome_row[1] == "2"
    assert float(chrome_row[2]) == 30.0
    assert float(chrome_row[3]) == 15.0
    assert abs(float(chrome_row[4].replace(" MB", "")) - 300.0) < 0.1