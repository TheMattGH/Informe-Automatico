from reportlab.platypus import Spacer, XPreformatted, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
import textwrap
import re

class PDFBlocks:
    def generate_blocks(content, sections: dict):
        """
        Genera bloques de información técnica a partir de un diccionario de secciones.
        """
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

        for tittle, fields in sections.items():
            block_text = format_section(tittle, fields)
            block = XPreformatted(block_text, paragraph_style)
            content.append(KeepTogether([block, Spacer(1, 6)]))

    def add_processes_block(content, header, rows):
        """
        Agrega una tabla de procesos del sistema al informe.
        """
        from reportlab.platypus import XPreformatted, KeepTogether, Spacer
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.enums import TA_LEFT

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
        lines = []
        tittle = "<b>PROCESOS CON MAYOR CONSUMO DE RECURSOS</b>"
        lines.append("-" * total_width)
        lines.append(tittle.center(total_width + len(tittle) - len("PROCESOS CON MAYOR CONSUMO DE RECURSOS")))
        lines.append("-" * total_width)
        lines.append(
            f"<b>{header[0]:<25} {header[1]:<12} {header[2]:<10} {header[3]:<10} {header[4]}</b>"
        )
        lines.append("-" * total_width)
        for row in rows:
            lines.append(f"{row[0]:<25} {row[1]:<12} {row[2]:<10} {row[3]:<10} {row[4]}")
        lines.append("-" * total_width)

        block = XPreformatted("\n".join(lines), table_style)
        content.append(KeepTogether([block, Spacer(1, 6)]))

    def add_peripherals_block(content, peripherals: dict):
        """
        Agrega una tabla de periféricos conectados al informe.
        """
        from reportlab.platypus import XPreformatted, KeepTogether, Spacer
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.enums import TA_LEFT

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
        lines = []
        tittle = "<b>PERIFÉRICOS CONECTADOS</b>"
        lines.append("-" * total_width)
        lines.append(tittle.center(total_width + len(tittle) - len("PERIFÉRICOS CONECTADOS")))
        lines.append("-" * total_width)
        lines.append(f"<b>{'Categoría':<20} | Dispositivos</b>")
        lines.append("-" * total_width)

        import textwrap, re
        for category, devices in peripherals.items():
            if isinstance(peripherals, list):
                devices_str = ", ".join(peripherals)
            else:
                devices_str = str(devices)
            devices_str = re.sub(r'(\b[\wáéíóúÁÉÍÓÚñÑ]+:)', r'<b>\1</b>', devices_str)
            wrapped_lines = textwrap.wrap(devices_str, width=total_width - 23)
            if wrapped_lines:
                lines.append(f"<b>{category:<20}</b> | {wrapped_lines[0]}")
                for extra_line in wrapped_lines[1:]:
                    lines.append(f"{'':<20} | {extra_line}")
            else:
                lines.append(f"<b>{category:<20}</b> | ")

        lines.append("-" * total_width)

        block = XPreformatted("\n".join(lines), style)
        content.append(KeepTogether([block, Spacer(1, 6)]))
    
    def add_recommendations_block(content, recommendations):
        style = ParagraphStyle(
            name="RecomendacionesBlock",
            fontName="Courier",
            fontSize=9,
            leading=11,
            leftIndent=10,
            spaceBefore=5,
            spaceAfter=5,
        )
        import textwrap
        total_width = 80
        lines = []
        tittle = "<b>RECOMENDACIONES DEL SISTEMA</b>"
        lines.append("-" * total_width)
        lines.append(tittle.center(total_width + len(tittle) - len("RECOMENDACIONES DEL SISTEMA")))
        lines.append("-" * total_width)
        
        if not recommendations:
            lines.append("No se detectaron problemas significativos en el sistema.")
        else:
            for rec in recommendations:
                # Tratamiento especial para la línea divisoria de recomendaciones generales
                if rec.startswith("---RECOMENDACIONES GENERALES---"):
                    # Añade una línea separadora
                    lines.append("-" * total_width)
                    # Centra el texto de recomendaciones generales y lo pone en negrita
                    subtitle = "<b>RECOMENDACIONES GENERALES</b>"
                    left_space = (total_width - len("RECOMENDACIONES GENERALES")) // 2
                    centered_subtitle = " " * left_space + subtitle
                    lines.append(centered_subtitle)
                    lines.append("-" * total_width)
                else:
                    # Formato normal para el resto de recomendaciones
                    wrapped = textwrap.wrap(f"• {rec}", width=total_width)
                    lines.extend(wrapped)
        
        lines.append("-" * total_width)
        block = XPreformatted("\n".join(lines), style)
        content.append(KeepTogether([block, Spacer(1, 6)]))