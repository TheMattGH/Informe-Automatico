import pytest
from unittest.mock import patch, MagicMock
from pdfrw import PdfName
import os
from pathlib import Path
from utils.pdf_utils import apply_template

# Import the function to test using absolute import

@pytest.fixture
def setup_test_environment():
    """Create a test environment with mocked directories and files"""
    base_dir = Path(__file__).resolve().parent.parent
    reports_dir = base_dir / "reports"
    data_dir = base_dir / "data"
    
    # Create necessary directories for testing
    reports_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Create dummy files
    (data_dir / "plantilla.pdf").touch()
    (reports_dir / "informe_contenido.pdf").touch()
    
    yield {
        "base_dir": base_dir,
        "reports_dir": reports_dir,
        "data_dir": data_dir
    }
    
    # Clean up after test
    for file in reports_dir.glob("Informe Técnico*.pdf"):
        try:
            file.unlink()
        except:
            pass

@patch('utils.pdf_utils.PdfReader')
@patch('utils.pdf_utils.PdfWriter')
@patch('utils.pdf_utils.PageMerge')
def test_apply_template_basic(mock_page_merge, mock_pdf_writer, mock_pdf_reader, setup_test_environment):
    """Test apply_template with basic user name"""
    # Arrange
    mock_pdf_reader.return_value.pages = [MagicMock()]
    mock_writer_instance = MagicMock()
    mock_pdf_writer.return_value = mock_writer_instance
    mock_merger = MagicMock()
    mock_page_merge.return_value = mock_merger
    
    test_name = "John Doe"
    expected_output_file = setup_test_environment["reports_dir"] / f"Informe Técnico {test_name}.pdf"
    
    # Act
    apply_template(test_name)
    
    # Assert
    mock_pdf_reader.assert_called()
    mock_page_merge.assert_called()
    mock_writer_instance.addpages.assert_called()
    mock_writer_instance.write.assert_called_with(str(expected_output_file))

@patch('utils.pdf_utils.PdfReader')
@patch('utils.pdf_utils.PdfWriter')
@patch('utils.pdf_utils.PageMerge')
def test_apply_template_special_chars(mock_page_merge, mock_pdf_writer, mock_pdf_reader, setup_test_environment):
    """Test apply_template with special characters in name"""
    # Arrange
    mock_pdf_reader.return_value.pages = [MagicMock()]
    mock_writer_instance = MagicMock()
    mock_pdf_writer.return_value = mock_writer_instance
    mock_merger = MagicMock()
    mock_page_merge.return_value = mock_merger
    
    test_name = "John Doe @#$%^&*()!?"
    expected_safe_name = "John Doe"
    expected_output_file = setup_test_environment["reports_dir"] / f"Informe Técnico {expected_safe_name}.pdf"
    
    # Act
    apply_template(test_name)
    
    # Assert
    mock_writer_instance.write.assert_called_with(str(expected_output_file))

@patch('utils.pdf_utils.PdfReader')
@patch('utils.pdf_utils.PdfWriter')
@patch('utils.pdf_utils.PageMerge')
def test_apply_template_multiple_pages(mock_page_merge, mock_pdf_writer, mock_pdf_reader, setup_test_environment):
    """Test apply_template with multiple report pages"""
    # Arrange
    template_page = MagicMock()
    template_page.Type = PdfName.Page
    report_pages = [MagicMock() for _ in range(3)]
    for page in report_pages:
        page.Type = PdfName.Page

    mock_pdf_reader.side_effect = [
        MagicMock(pages=[template_page]),
        MagicMock(pages=report_pages)
    ]

    mock_writer_instance = MagicMock()
    mock_pdf_writer.return_value = mock_writer_instance

    mock_merger = MagicMock()
    mock_page_merge.return_value = mock_merger

    test_name = "John Doe"

    # Act
    apply_template(test_name)

    # Assert
    assert mock_pdf_reader.call_count == 2
    mock_writer_instance.addpages.assert_called_with(report_pages)

@patch('utils.pdf_utils.PdfReader')
def test_apply_template_template_file_error(mock_pdf_reader):
    """Test apply_template maneja error al leer plantilla"""
    mock_pdf_reader.side_effect = Exception("Archivo corrupto")
    with pytest.raises(Exception) as excinfo:
        apply_template("Usuario Error")
    assert "Archivo corrupto" in str(excinfo.value)

@patch('utils.pdf_utils.PdfReader')
@patch('utils.pdf_utils.PdfWriter')
@patch('utils.pdf_utils.PageMerge')
def test_apply_template_write_error(mock_page_merge, mock_pdf_writer, mock_pdf_reader):
    """Test apply_template maneja error al escribir el PDF final"""
    mock_pdf_reader.return_value.pages = [MagicMock()]
    mock_writer_instance = MagicMock()
    mock_writer_instance.write.side_effect = IOError("No se puede escribir archivo")
    mock_pdf_writer.return_value = mock_writer_instance
    mock_page_merge.return_value = MagicMock()
    with pytest.raises(IOError) as excinfo:
        apply_template("Usuario Error")
    assert "No se puede escribir archivo" in str(excinfo.value)