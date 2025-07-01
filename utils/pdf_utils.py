from pdfrw import PdfReader, PdfWriter, PageMerge
from pathlib import Path

def apply_template(names):
    """
    Aplica la plantilla visual institucional al informe generado.
    El nombre final del archivo incluye el nombre del usuario.
    """
    base_dir = Path(__file__).resolve().parent.parent
    reports_dir = base_dir / "reports"
    data_dir = base_dir / "data"
    reports_dir.mkdir(parents=True, exist_ok=True)

    template_path = data_dir / "plantilla.pdf"
    report_path = reports_dir / "informe_contenido.pdf"
    safe_names = "".join(c for c in names if c.isalnum() or c in (" ", "_", "-")).strip()
    final_report_path = reports_dir / f"Informe Técnico {safe_names}.pdf"

    template = PdfReader(str(template_path)).pages
    report = PdfReader(str(report_path)).pages

    for page in report:
        fondo = template[0]
        merger = PageMerge(page)
        merger.add(fondo, prepend=True).render()

    writer = PdfWriter()
    writer.addpages(report)
    writer.write(str(final_report_path))