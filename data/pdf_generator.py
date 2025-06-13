from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from PIL import Image as PILImage
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics import renderPDF
from reportlab.lib.units import cm
class PDFGenerator:

    def __init__(self, nombre_arhivo = "informe.pdf"):
        self.pdf =  SimpleDocTemplate(
            nombre_arhivo,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2.5*cm,
            bottomMargin=2*cm        
            )
        self.estilos = getSampleStyleSheet()
        self.contenido = []

    def AddHeader(self, canvas, doc):
        try:
            canvas.saveState()

            # Ruta y tamaño ajustado de la imagen
            logo_path = "data/assets/LOGOBA.png" 
            logo_width = 110   # Aumentado de 80
            logo_height = 18   # Aumentado de 15

            y_position = A4[1] - 60  # Más abajo que antes (antes era -40)

            # Dibujar logo
            canvas.drawImage(
                logo_path,
                doc.leftMargin,
                y_position,
                width=logo_width,
                height=logo_height,
                mask='auto'
            )

            # Dibujar título centrado verticalmente con respecto al logo
            canvas.setFont("Helvetica-Bold", 12)
            canvas.drawRightString(
                A4[0] - doc.rightMargin,
                y_position + logo_height / 4 + 2,
                "INFORME TÉCNICO DEL SISTEMA"
            )

            canvas.restoreState()
        except Exception as e:
            print(f"[Error en encabezado]: {e}")


    def AddParagraph(self, texto, titulo = "Datos del Usuario"):
        self.contenido.append(Paragraph(f"<b>{titulo}</b>", self.estilos["Heading2"]))
        for line in texto.split("\n"):
            if line.strip():
                self.contenido.append(Paragraph(line.strip(), self.estilos["Normal"]))
        self.contenido.append(Spacer(1, 12))

    def AddTable(self, titulo, cabecera, datos):    
        self.contenido.append(Paragraph(titulo, self.estilos["Title"]))
        tabla = Table([cabecera] + datos, repeatRows=1)
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        self.contenido.append(tabla)

    def AddKeyValueTable(self, titulo, data_dict):
        self.contenido.append(Paragraph(titulo, self.estilos["Title"]))

        col_widths = [130, 200] 

        data = [[Paragraph(f"<b>{k}</b>", self.estilos["Normal"]), Paragraph(str(v), self.estilos["Normal"])] for k, v in data_dict.items()]
        tabla = Table(data, colWidths=col_widths)   

        tabla.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ]))

        self.contenido.append(tabla)
        self.contenido.append(Spacer(1, 16))    


    def AddSmartStatus(self, smart_info):
        self.contenido.append(Paragraph("Estado SMART de los Discos", self.estilos["Title"]))

        for disk, estado in smart_info.items():
            if isinstance(estado, dict):
                self.contenido.append(Paragraph(f"<b>🖴 {disk}</b>", self.estilos["Normal"]))
                for k, v in estado.items():
                    self.contenido.append(Paragraph(f"{k}: {v}", self.estilos["Normal"]))
                self.contenido.append(Spacer(1, 8))
            else:
                self.contenido.append(Paragraph(f"🖴 {disk}: No se pudo obtener información SMART.", self.estilos["Normal"]))
                self.contenido.append(Spacer(1, 8))


    def PageFooter(self, canvas, doc):
            canvas.saveState()
            canvas.setFont('Helvetica', 8)
            canvas.drawString(40, 30, "Informe generado automáticamente por el sistema.")
            canvas.drawRightString(A4[0] - 40, 30, f"Página {canvas.getPageNumber()}")
            canvas.restoreState()
    
    def _withHeaderAndFooter(self, canvas, doc):
        self.AddHeader(canvas, doc)
        self.PageFooter(canvas, doc)

    def SaveTable(self):
            self.pdf.build(
                self.contenido,
                onFirstPage = self._withHeaderAndFooter, 
                onLaterPages=self._withHeaderAndFooter)

    
        