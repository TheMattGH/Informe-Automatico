from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from PIL import Image as PILImage
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics import renderPDF
from reportlab.lib.units import cm


from reportlab.platypus import Preformatted, XPreformatted
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
import textwrap

class PDFGenerator:

    def __init__(self, nombre_arhivo = "informe.pdf"):
        self.pdf =  SimpleDocTemplate(
            nombre_arhivo,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
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


    def generar_bloques_formato_fijo(self, secciones: dict):
        estilo_parrafo = ParagraphStyle(
            name="EstiloConsola",
            fontName="Courier",
            fontSize=9,
            leading=11,
            leftIndent=10,
            spaceBefore=10,
            spaceAfter=10,
            alignment=TA_LEFT
        )

        def escapar(texto):
            return texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        def formatear_seccion(titulo, campos):
            titulo_plano = titulo.upper()
            ancho_total = 80
            espacio_izq = (ancho_total - len(titulo_plano)) // 2
            titulo_centrado = " " * espacio_izq + f"<b>{escapar(titulo_plano)}</b>"

            bloque = f"{'-'*80}\n{titulo_centrado}\n{'-'*80}\n"
            for clave, valor in campos.items():
                clave_negrita = f"<b>{escapar(clave)}:</b>"
                if isinstance(valor, list): 
                    bloque += f"{clave_negrita}\n"
                    for item in valor:
                        for linea in textwrap.wrap(f"  - {item}", width=76):
                            bloque += f"{escapar(linea)}\n"
                else:
                    linea = f"{clave_negrita} {escapar(str(valor))}"
                    wrapped = textwrap.wrap(linea, width=76)
                    bloque += "\n".join(wrapped) + "\n"
            bloque += '-'*80 + '\n'
            return bloque

        from reportlab.platypus import XPreformatted  # Importar XPreformatted que sí acepta HTML simple
        for titulo, campos in secciones.items():
            bloque_texto = formatear_seccion(titulo, campos)
            self.contenido.append(XPreformatted(bloque_texto, estilo_parrafo))



    def agregar_tabla_procesos_texto(self, cabecera, filas):
        estilo_tabla = ParagraphStyle(
            name="TablaProcesosTextoPlano",
            fontName="Courier",
            fontSize=9,
            leading=11,
            leftIndent=10,
            spaceBefore=10,
            spaceAfter=10,
            alignment=TA_LEFT
        )

        def escapar(texto):
            return texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        titulo = "PROCESOS CON MAYOR CONSUMO DE RECURSOS"
        ancho_total = 80
        espacio_izq = (ancho_total - len(titulo)) // 2
        titulo_centrado = " " * espacio_izq + f"<b>{escapar(titulo)}</b>"

        contenido = [
            "-" * 80,
            titulo_centrado,
            "-" * 80,
            f"<b>{escapar(cabecera[0]):<25} {cabecera[1]:<12} {cabecera[2]:<10} {cabecera[3]:<10} {cabecera[4]}</b>",
            "-" * 80,
        ]

        for fila in filas:
            contenido.append(f"{escapar(fila[0]):<25} {fila[1]:<12} {fila[2]:<10} {fila[3]:<10} {fila[4]}")

        contenido.append("-" * 80)

        self.contenido.append(XPreformatted("\n".join(contenido), estilo_tabla))


    def agregar_perifericos_formato_tabla(self, perifericos: dict):

        estilo = ParagraphStyle(
            name="PerifericosTablaTexto",
            fontName="Courier",
            fontSize=9,
            leading=11,
            leftIndent=10,
            spaceBefore=10,
            spaceAfter=10,
            alignment=TA_LEFT
        )

        def escapar(texto):
            return texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        ancho_total = 80
        titulo = "PERIFÉRICOS CONECTADOS"
        espacio_izq = (ancho_total - len(titulo)) // 2
        titulo_centrado = " " * espacio_izq + f"<b>{titulo}</b>"

        contenido = ["-" * 80, titulo_centrado, "-" * 80]
        encabezado = f"<b>{'Categoría':<20} | Dispositivos</b>"
        contenido.append(encabezado)
        contenido.append("-" * 80)

        for categoria, dispositivos in perifericos.items():
            if isinstance(dispositivos, list):
                dispositivos_str = ", ".join(dispositivos)
            else:
                dispositivos_str = str(dispositivos)

            linea = f"{categoria:<20} | {dispositivos_str}"
            contenido.append(escapar(linea))

        contenido.append("-" * 80)

        from reportlab.platypus import XPreformatted
        self.contenido.append(XPreformatted("\n".join(contenido), estilo))

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

    
        