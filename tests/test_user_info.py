import pytest
from unittest.mock import patch, MagicMock
from core.user_info import UserInfo

@patch('core.user_info.psutil.users')
@patch('core.user_info.geocoder.ip')
def test_get_info(mock_geocoder_ip, mock_psutil_users):
    # Simula usuario y ciudad
    mock_user = MagicMock()
    mock_user.name = 'testuser'
    mock_psutil_users.return_value = [mock_user]
    mock_geocoder_ip.return_value.city = 'CiudadTest'

    user = UserInfo(names="Juan", department="TI")
    info = user.get_info()

    assert info['names'] == "Juan"
    assert info['department'] == "TI"
    assert info['user'] == "testuser"
    assert info['location'] == "CiudadTest"
    assert "date" in info