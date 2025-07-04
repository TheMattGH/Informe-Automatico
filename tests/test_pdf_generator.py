import pytest
from utils.pdf_generator import PDFGenerator

def test_pdf_generator_normal(tmp_path):
    pdf_path = tmp_path / "test.pdf"
    pdf = PDFGenerator(str(pdf_path))
    pdf.add_tittle("Título de Prueba")
    pdf.add_paragraph("Contenido de prueba", "Sección")
    pdf.save_document()
    assert pdf_path.exists()

def test_pdf_generator_save_document_error(monkeypatch, tmp_path):
    pdf_path = tmp_path / "test.pdf"
    pdf = PDFGenerator(str(pdf_path))
    pdf.add_tittle("Título de Prueba")
    pdf.add_paragraph("Contenido de prueba", "Sección")

    # Fuerza un error en build
    def fake_build(*args, **kwargs):
        raise IOError("No se puede escribir el PDF")
    monkeypatch.setattr(pdf.pdf, "build", fake_build)

    with pytest.raises(IOError, match="No se puede escribir el PDF"):
        pdf.save_document()