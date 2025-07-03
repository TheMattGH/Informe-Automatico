from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER
class PDFGenerator:
    """
    Clase para la generación estructurada de informes PDF técnicos.
    Utiliza ReportLab para crear documentos con formato profesional.
    """

    def __init__(self, document_name="informe.pdf"):
        """
        Inicializa el documento PDF con márgenes y estilos predeterminados.
        """
        self.pdf = SimpleDocTemplate(
            document_name,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=3*cm,
            bottomMargin=2*cm
        )
        self.styles = getSampleStyleSheet()
        self.content = []

    def add_tittle(self, texto):
        """
        Agrega un título centrado al informe.
        """
        tittle_style = ParagraphStyle(
            name="Titulo",
            fontName="Courier-Bold",
            fontSize=13,
            alignment=TA_CENTER,
            spaceAfter=12
        )
        self.content.append(Paragraph(texto, tittle_style))

    def add_paragraph(self, text, tittle):
        """
        Agrega una sección de párrafo con título y contenido HTML.
        """
        title_style = ParagraphStyle(
            name="TituloUsuario",
            fontName="Courier-Bold",
            fontSize=11,
            leading=14,
            leftIndent=10,
            spaceBefore=10,
            spaceAfter=2,
            alignment=TA_LEFT
        )
        html_style = ParagraphStyle(
            name="TextoHTML",
            fontSize=9,
            fontName="Courier",
            leading=11,
            leftIndent=10,
            spaceBefore=0,
            spaceAfter=1,
            alignment=TA_LEFT
        )
        self.content.append(Paragraph(tittle, title_style))
        self.content.append(Paragraph(text, html_style))
        self.content.append(Spacer(1, 4))
        
    def page_footer(self, canvas, doc):
        """
        Dibuja el pie de página en cada página del informe.
        """
        canvas.saveState()
        canvas.setFont('Courier-Bold', 8)
        left_margin = doc.leftMargin
        right_margin = doc.rightMargin
        page_width = A4[0]
        canvas.drawString(left_margin, 30, "Informe generado automáticamente por el sistema.")
        canvas.drawRightString(page_width - right_margin, 30, f"Página {canvas.getPageNumber()}")
        canvas.restoreState()

    def save_document(self):
        """
        Construye y guarda el documento PDF con todo el contenido agregado.
        Agrega el pie de página en todas las páginas.
        """
        self.pdf.build(
            self.content,
            onFirstPage=self.page_footer,
            onLaterPages=self.page_footer
        )

