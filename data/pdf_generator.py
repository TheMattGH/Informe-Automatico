from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

class PDFGenerator:

    def AddTitle(self, titulo="INFORME TÉCNICO DEL SISTEMA"):
        self.contenido.append(Paragraph(f"<para align='center'><b><font size=16>{titulo}</font></b></para>", self.estilos["Normal"]))
        self.contenido.append(Spacer(1, 24))

    def __init__(self, nombre_arhivo = "informe.pdf"):
        self.pdf =  SimpleDocTemplate(nombre_arhivo, pagesize = A4)
        self.estilos = getSampleStyleSheet()
        self.contenido = []

    def AddParagraph(self, texto, titulo = "Datos del Usuario"):
        self.contenido.append(Paragraph(f"<b>{titulo}</b>", self.estilos["Heading2"]))
        for line in texto.split("\n"):
            if line.strip():
                self.contenido.append(Paragraph(line.strip(), self.estilos["Normal"]))
        self.contenido.append(Spacer(1, 12))

    def AddTable(self, titulo, cabecera, datos):    
        self.contenido.append(Paragraph(titulo, self.estilos["Title"]))
        tabla = Table([cabecera] + [datos], repeatRows=1)
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        self.contenido.append(tabla)

    def AddKeyValueTable(self, titulo, data_dict):
        self.contenido.append(Paragraph(titulo, self.estilos["Title"]))

        data = [[Paragraph(f"<b>{k}</b>", self.estilos["Normal"]), Paragraph(str(v), self.estilos["Normal"])] for k, v in data_dict.items()]
        tabla = Table(data, colWidths=[130, 200])   

        tabla.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ]))

        self.contenido.append(tabla)
        self.contenido.append(Spacer(1, 16))    

    def PageFooter(self, canvas, doc):
            canvas.saveState()
            canvas.setFont('Helvetica', 8)
            canvas.drawString(40, 30, "Informe generado automáticamente por el sistema.")
            canvas.drawRightString(A4[0] - 40, 30, f"Página {canvas.getPageNumber()}")
            canvas.restoreState()
        
    def SaveTable(self):
            self.pdf.build(self.contenido, onFirstPage = self.PageFooter, onLaterPages=self.PageFooter)