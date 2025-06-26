from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import XPreformatted, Spacer, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import textwrap
import re
class PDFGenerator:

    #Definicion de Formato del documento
    def __init__(self, document_name = "informe.pdf"):
        self.pdf =  SimpleDocTemplate(
            document_name,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=3*cm,
            bottomMargin=2*cm        
            )
        self.styles = getSampleStyleSheet()
        self.content = []

    #Generacion del Titulo
    def add_tittle(self, texto):
            tittle_style = ParagraphStyle(
                name="Titulo",
                fontName="Courier-Bold",
                fontSize=13,
                alignment=TA_CENTER,
                spaceAfter=12
            )
            self.content.append(Paragraph(texto, tittle_style))

    #Generacion de los datos del Informe en formato de parrafo
    def add_paragraph(self, text, tittle):
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

        # Añade el titulo como un párrafo
        self.content.append(Paragraph(tittle, title_style))

        # Añade el contenido HTML
        self.content.append(Paragraph(text, html_style))
        self.content.append(Spacer(1, 4))

    #Generar las tablas de Informacion
    def generate_blocks(self, sections: dict):
        paragraph_style = ParagraphStyle(
            name="EstiloConsola",
            fontName="Courier",
            fontSize=9,
            leading=11,
            leftIndent=10,
            spaceBefore=5,
            spaceAfter=5,
            alignment=TA_LEFT
        )

        def format_section(tittle, fields):
            flat_tittle = tittle.upper()
            total_width = 80
            left_space = (total_width - len(flat_tittle)) // 2
            center_tittle = " " * left_space + flat_tittle

            bloque = f"{'-'*total_width}\n<b>{center_tittle}</b>\n{'-'*total_width}\n"
            for key, value in fields.items():
                bold_keys = f"<b>{key}:</b>"
                if isinstance(value, list): 
                    bloque += f"{bold_keys}\n"
                    for item in value:
                        for line in textwrap.wrap(f"  - {item}", width=76):
                            bloque += f"{line}\n"
                else:
                    line = f"{bold_keys} {str(value)}"
                    wrapped = textwrap.wrap(line, width=76)
                    bloque += "\n".join(wrapped) + "\n"
            bloque += '-'*total_width + '\n'
            return bloque

        for tittle, fileds in sections.items():
            block_text = format_section(tittle, fileds)
            block = XPreformatted(block_text, paragraph_style)
            self.content.append(KeepTogether([block, Spacer(1, 6)]))
    
    #Generar tabla de procesos del sistema
    def add_processes_block(self, header, rows):
        table_style = ParagraphStyle(
            name="TablaProcesos",
            fontName="Courier",
            fontSize=9,
            leading=11,
            leftIndent=10,
            spaceBefore=5,
            spaceAfter=5,
            alignment=TA_LEFT
        )

        total_width = 80
        content = []
        tittle = "<b>PROCESOS CON MAYOR CONSUMO DE RECURSOS</b>"
        content.append("-" * total_width)
        content.append(tittle.center(total_width + len(tittle) - len("PROCESOS CON MAYOR CONSUMO DE RECURSOS")))
        content.append("-" * total_width)
        # Cabecera en negrita
        content.append(
            f"<b>{header[0]:<25} {header[1]:<12} {header[2]:<10} {header[3]:<10} {header[4]}</b>"
        )
        content.append("-" * total_width)
        # Filas
        for row in rows:
            # Puedes poner en negrita solo los campos que sean subtítulo si lo deseas
            content.append(f"{row[0]:<25} {row[1]:<12} {row[2]:<10} {row[3]:<10} {row[4]}")
        content.append("-" * total_width)

        block = XPreformatted("\n".join(content), table_style)
        self.content.append(KeepTogether([block, Spacer(1, 6)]))

    #Generar tabla de perifericos
    def add_peripherals_block(self, peripherals: dict):
        style = ParagraphStyle(
            name="PerifericosTabla",
            fontName="Courier",
            fontSize=9,
            leading=11,
            leftIndent=10,
            spaceBefore=5,
            spaceAfter=5,
            alignment=TA_LEFT
        )

        total_width = 80
        content = []
        tittle = "<b>PERIFÉRICOS CONECTADOS</b>"
        content.append("-" * total_width)
        content.append(tittle.center(total_width + len(tittle) - len("PERIFÉRICOS CONECTADOS")))
        content.append("-" * total_width)
        content.append(f"<b>{'Categoría':<20} | Dispositivos</b>")
        content.append("-" * total_width)

        for category, devices in peripherals.items():
            if isinstance(peripherals, list):
                devices_str = ", ".join(peripherals)
            else:
                devices_str = str(devices)
            devices_str = re.sub(r'(\b[\wáéíóúÁÉÍÓÚñÑ]+:)', r'<b>\1</b>', devices_str)
            wrapped_lines = textwrap.wrap(devices_str, width=total_width - 23)
            if wrapped_lines:
                content.append(f"<b>{category:<20}</b> | {wrapped_lines[0]}")
                for extra_line in wrapped_lines[1:]:
                    content.append(f"{'':<20} | {extra_line}")
            else:
                content.append(f"<b>{category:<20}</b> | ")

        content.append("-" * total_width)

        block = XPreformatted("\n".join(content), style)
        self.content.append(KeepTogether([block, Spacer(1, 6)]))


    def agregar_recomendaciones(self, recomendaciones):
        self.content.append(Spacer(1, 12))
        self.content.append(Paragraph("<b>Recomendaciones del Sistema</b>", self.styles["Heading2"]))
        if not recomendaciones:
            self.content.append(Paragraph("No se detectaron problemas significativos en el sistema.", self.styles["Normal"]))
        else:
            for rec in recomendaciones:
                self.content.append(Paragraph(rec, self.styles["Normal"]))


    def page_footer(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Courier-Bold', 8)

        left_margin = doc.leftMargin
        right_margin = doc.rightMargin
        page_width = A4[0]

        canvas.drawString(left_margin, 30, "Informe generado automáticamente por el sistema.")

        canvas.drawRightString(page_width - right_margin, 30, f"Página {canvas.getPageNumber()}")

        canvas.restoreState()

    #Guardar documento pdf
    def save_document(self):
            self.pdf.build(
                self.content,
                onFirstPage = self.page_footer, 
                onLaterPages=self.page_footer)


