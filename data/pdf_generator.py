from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from PIL import Image as PILImage
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics import renderPDF
from reportlab.lib.units import cm


from reportlab.platypus import Preformatted, XPreformatted, Spacer, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import textwrap
import re


class PDFGenerator:

    def __init__(self, nombre_arhivo = "informe.pdf"):
        self.pdf =  SimpleDocTemplate(
            nombre_arhivo,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=3*cm,
            bottomMargin=2*cm        
            )
        self.estilos = getSampleStyleSheet()
        self.contenido = []

    # def AddHeader(self, canvas, doc):
    #     try:
    #         canvas.saveState()

    #         # Ruta y tamaño ajustado de la imagen
    #         logo_path = "data/assets/LOGOBA.png" 
    #         logo_width = 110   # Aumentado de 80
    #         logo_height = 18   # Aumentado de 15

    #         y_position = A4[1] - 60  # Más abajo que antes (antes era -40)

    #         # Dibujar logo
    #         canvas.drawImage(
    #             logo_path,
    #             doc.leftMargin,
    #             y_position,
    #             width=logo_width,
    #             height=logo_height,
    #             mask='auto'
    #         )

    #         # Dibujar título centrado verticalmente con respecto al logo
    #         canvas.setFont("Helvetica-Bold", 12)
    #         canvas.drawRightString(
    #             A4[0] - doc.rightMargin,
    #             y_position + logo_height / 4 + 2,
    #             "INFORME TÉCNICO DEL SISTEMA"
    #         )

    #         canvas.restoreState()
    #     except Exception as e:
    #         print(f"[Error en encabezado]: {e}")

    
    def agregar_titulo_centrado(self, texto):
            estilo_titulo = ParagraphStyle(
                name="TituloCentrado",
                fontName="Courier-Bold",
                fontSize=13,
                alignment=TA_CENTER,
                spaceAfter=12
            )
            self.contenido.append(Paragraph(texto, estilo_titulo))

    def AddParagraph(self, texto, titulo="Datos del Informe"):
        estilo_titulo = ParagraphStyle(
            name="TituloUsuario",
            fontName="Courier-Bold",
            fontSize=11,
            leading=14,
            leftIndent=10,     
            spaceBefore=10,
            spaceAfter=2,
            alignment=TA_LEFT
        )

        estilo_html = ParagraphStyle(
            name="TextoHTML",
            fontSize=9,
            fontName="Courier",
            leading=11,
            leftIndent=10,       
            spaceBefore=0,
            spaceAfter=1,
            alignment=TA_LEFT
        )

        # Añade el título como un párrafo
        self.contenido.append(Paragraph(titulo, estilo_titulo))

        # Añade el contenido HTML con estilo personalizado
        self.contenido.append(Paragraph(texto, estilo_html))
        self.contenido.append(Spacer(1, 4))


    def generar_bloques_formato_fijo(self, secciones: dict):
        estilo_parrafo = ParagraphStyle(
            name="EstiloConsola",
            fontName="Courier",
            fontSize=9,
            leading=11,
            leftIndent=10,
            spaceBefore=5,
            spaceAfter=5,
            alignment=TA_LEFT
        )

        def formatear_seccion(titulo, campos):
            titulo_plano = titulo.upper()
            ancho_total = 80
            espacio_izq = (ancho_total - len(titulo_plano)) // 2
            titulo_centrado = " " * espacio_izq + titulo_plano

            bloque = f"{'-'*ancho_total}\n<b>{titulo_centrado}</b>\n{'-'*ancho_total}\n"
            for clave, valor in campos.items():
                clave_negrita = f"<b>{clave}:</b>"
                if isinstance(valor, list): 
                    bloque += f"{clave_negrita}\n"
                    for item in valor:
                        for linea in textwrap.wrap(f"  - {item}", width=76):
                            bloque += f"{linea}\n"
                else:
                    linea = f"{clave_negrita} {str(valor)}"
                    wrapped = textwrap.wrap(linea, width=76)
                    bloque += "\n".join(wrapped) + "\n"
            bloque += '-'*ancho_total + '\n'
            return bloque

        for titulo, campos in secciones.items():
            bloque_texto = formatear_seccion(titulo, campos)
            bloque = XPreformatted(bloque_texto, estilo_parrafo)
            self.contenido.append(KeepTogether([bloque, Spacer(1, 6)]))



    def agregar_tabla_procesos_texto(self, cabecera, filas):
        estilo_tabla = ParagraphStyle(
            name="TablaProcesosTextoPlano",
            fontName="Courier",
            fontSize=9,
            leading=11,
            leftIndent=10,
            spaceBefore=5,
            spaceAfter=5,
            alignment=TA_LEFT
        )

        ancho_total = 80
        contenido = []
        titulo = "<b>PROCESOS CON MAYOR CONSUMO DE RECURSOS</b>"
        contenido.append("-" * ancho_total)
        contenido.append(titulo.center(ancho_total + len(titulo) - len("PROCESOS CON MAYOR CONSUMO DE RECURSOS")))
        contenido.append("-" * ancho_total)
        # Cabecera en negrita
        contenido.append(
            f"<b>{cabecera[0]:<25} {cabecera[1]:<12} {cabecera[2]:<10} {cabecera[3]:<10} {cabecera[4]}</b>"
        )
        contenido.append("-" * ancho_total)
        # Filas
        for fila in filas:
            # Puedes poner en negrita solo los campos que sean subtítulo si lo deseas
            contenido.append(f"{fila[0]:<25} {fila[1]:<12} {fila[2]:<10} {fila[3]:<10} {fila[4]}")
        contenido.append("-" * ancho_total)

        bloque = XPreformatted("\n".join(contenido), estilo_tabla)
        self.contenido.append(KeepTogether([bloque, Spacer(1, 6)]))


    def agregar_perifericos_formato_tabla(self, perifericos: dict):
        estilo = ParagraphStyle(
            name="PerifericosTablaTexto",
            fontName="Courier",
            fontSize=9,
            leading=11,
            leftIndent=10,
            spaceBefore=5,
            spaceAfter=5,
            alignment=TA_LEFT
        )

        ancho_total = 80
        contenido = []
        titulo = "<b>PERIFÉRICOS CONECTADOS</b>"
        contenido.append("-" * ancho_total)
        contenido.append(titulo.center(ancho_total + len(titulo) - len("PERIFÉRICOS CONECTADOS")))
        contenido.append("-" * ancho_total)
        contenido.append(f"<b>{'Categoría':<20} | Dispositivos</b>")
        contenido.append("-" * ancho_total)

        for categoria, dispositivos in perifericos.items():
            if isinstance(dispositivos, list):
                dispositivos_str = ", ".join(dispositivos)
            else:
                dispositivos_str = str(dispositivos)
            # Negrita solo en títulos tipo "Fabricante:", "Driver:", etc.
            dispositivos_str = re.sub(r'(\b[\wáéíóúÁÉÍÓÚñÑ]+:)', r'<b>\1</b>', dispositivos_str)
            wrapped_lines = textwrap.wrap(dispositivos_str, width=ancho_total - 23)
            if wrapped_lines:
                # Primera línea con la categoría en negrita
                contenido.append(f"<b>{categoria:<20}</b> | {wrapped_lines[0]}")
                # Líneas siguientes solo con espacios en la columna de categoría
                for extra_line in wrapped_lines[1:]:
                    contenido.append(f"{'':<20} | {extra_line}")
            else:
                contenido.append(f"<b>{categoria:<20}</b> | ")

        contenido.append("-" * ancho_total)

        bloque = XPreformatted("\n".join(contenido), estilo)
        self.contenido.append(KeepTogether([bloque, Spacer(1, 6)]))


    # def AddTable(self, titulo, cabecera, datos):    
    #     self.contenido.append(Paragraph(titulo, self.estilos["Title"]))
    #     tabla = Table([cabecera] + datos, repeatRows=1)
    #     tabla.setStyle(TableStyle([
    #         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    #         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    #         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    #         ('GRID', (0, 0), (-1, -1), 1, colors.black)
    #     ]))
    #     self.contenido.append(tabla)

    # def AddKeyValueTable(self, titulo, data_dict):
    #     self.contenido.append(Paragraph(titulo, self.estilos["Title"]))

    #     col_widths = [130, 200] 

    #     data = [[Paragraph(f"<b>{k}</b>", self.estilos["Normal"]), Paragraph(str(v), self.estilos["Normal"])] for k, v in data_dict.items()]
    #     tabla = Table(data, colWidths=col_widths)   

    #     tabla.setStyle(TableStyle([
    #         ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    #         ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    #         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    #         ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
    #         ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    #     ]))

    #     self.contenido.append(tabla)
    #     self.contenido.append(Spacer(1, 16))    


    # def AddSmartStatus(self, smart_info):
    #     self.contenido.append(Paragraph("Estado SMART de los Discos", self.estilos["Title"]))

    #     for disk, estado in smart_info.items():
    #         if isinstance(estado, dict):
    #             self.contenido.append(Paragraph(f"<b>🖴 {disk}</b>", self.estilos["Normal"]))
    #             for k, v in estado.items():
    #                 self.contenido.append(Paragraph(f"{k}: {v}", self.estilos["Normal"]))
    #             self.contenido.append(Spacer(1, 8))
    #         else:
    #             self.contenido.append(Paragraph(f"🖴 {disk}: No se pudo obtener información SMART.", self.estilos["Normal"]))
    #             self.contenido.append(Spacer(1, 8))


    def PageFooter(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Courier-Bold', 8)

        # Usar márgenes definidos en el documento
        left_margin = doc.leftMargin
        right_margin = doc.rightMargin
        page_width = A4[0]

        # Alinear texto izquierdo con el inicio de los cuadros
        canvas.drawString(left_margin, 30, "Informe generado automáticamente por el sistema.")

        # Alinear número de página con el final de los cuadros
        canvas.drawRightString(page_width - right_margin, 30, f"Página {canvas.getPageNumber()}")

        canvas.restoreState()

    def SaveTable(self):
            self.pdf.build(
                self.contenido,
                onFirstPage = self.PageFooter, 
                onLaterPages=self.PageFooter)


