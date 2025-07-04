import pytest
from utils.pdf_generate_blocks import PDFBlocks

def test_generate_blocks_normal():
    content = []
    sections = {
        "Sistema": {"OS": "Windows", "Versión": "10"},
        "CPU": {"Modelo": "Intel", "Cores": 4}
    }
    PDFBlocks.generate_blocks(content, sections)
    assert content  # Debe haber contenido agregado

def test_generate_blocks_empty_sections():
    content = []
    sections = {}
    PDFBlocks.generate_blocks(content, sections)
    assert content == []

def test_generate_blocks_invalid_section(monkeypatch):
    content = []
    sections = {"Sistema": None}
    # No debe lanzar excepción aunque los datos sean incorrectos
    try:
        PDFBlocks.generate_blocks(content, sections)
    except Exception as e:
        pytest.fail(f"generate_blocks lanzó una excepción inesperada: {e}")

def test_add_processes_block_normal():
    content = []
    header = ["Nombre", "PID", "CPU %", "RAM %", "Usuario"]
    rows = [["explorer.exe", 1234, "10", "5", "user"]]
    PDFBlocks.add_processes_block(content, header, rows)
    assert content

def test_add_processes_block_empty():
    content = []
    header = ["Nombre", "PID", "CPU %", "RAM %", "Usuario"]
    rows = []
    PDFBlocks.add_processes_block(content, header, rows)
    assert content

def test_add_peripherals_block_normal():
    content = []
    peripherals = {"Monitores": ["Monitor1"], "Teclados": ["Teclado1"]}
    PDFBlocks.add_peripherals_block(content, peripherals)
    assert content

def test_add_peripherals_block_empty():
    content = []
    peripherals = {}
    PDFBlocks.add_peripherals_block(content, peripherals)
    assert content

def test_add_recommendations_block_normal():
    content = []
    recommendations = ["Revisar el uso de CPU."]
    PDFBlocks.add_recommendations_block(content, recommendations)
    assert content

def test_add_recommendations_block_none():
    content = []
    recommendations = None
    PDFBlocks.add_recommendations_block(content, recommendations)
    assert content