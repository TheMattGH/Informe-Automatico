from core.software_info import SoftwareInfo
from core.cpu_info import CPUInfo
from core.memory_info import MemoryInfo
from core.storage_info import StorageInfo
from core.user_info import UserInfo
from core.peripherals_info import PeripheralsInfo
from core.system_info import SystemInfo
from core.process_info import ProcessInfo
from core.recommendations import generate_recommendations
from core.report_data_builder import ReportDataBuilder
from utils.pdf_utils import apply_template
from utils.pdf_generate_blocks import PDFBlocks
import time
import traceback
import logging
from pathlib import Path
from utils.pdf_generator import PDFGenerator

# Configurar logging
reports_dir = Path(__file__).resolve().parent.parent / "reports"
reports_dir.mkdir(parents=True, exist_ok=True)
log_file = reports_dir / "error_log.txt"

logging.basicConfig(
    filename=str(log_file),
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main(names=None, department=None, progress=None):
    """
    Función principal para la generación del informe técnico.
    Recopila información del sistema, la estructura y genera el PDF final.
    """
    start_time = time.time()
    pdf = None
    reports_dir = None
    
    try:
        # Actualizar progreso si está disponible
        if progress:
            progress.set(10)
            progress.update_idletasks()
            
        # Crear el directorio de reportes si no existe
        reports_dir = Path(__file__).resolve().parent.parent / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Generar PDF base
        pdf = PDFGenerator(str(reports_dir / "informe_contenido.pdf"))
        pdf.add_tittle("INFORME TECNICO DEL SISTEMA")
        
        if progress:
            progress.set(20)
            progress.update_idletasks()
            
        # Datos del informe
        user_info = UserInfo(names, department)
        pdf.add_paragraph(user_info.get_text(), "Datos del Informe")
        
        if progress:
            progress.set(30)
            progress.update_idletasks()
            
        # Recopilación de información técnica
        software_info = SoftwareInfo().get_info()
        cpu_info = CPUInfo().get_info()
        memory_info = MemoryInfo()
        ram_info = memory_info.get_info()
        slot_info = memory_info.get_slot_info()
        system_info = SystemInfo().get_info()
        process_info = ProcessInfo()
        header, rows = process_info.get_info()
        disks = StorageInfo().get_info()
        
        if progress:
            progress.set(60)
            progress.update_idletasks()
            
        # Estructura de secciones del informe
        sections = ReportDataBuilder.build_sections(
            software_info, cpu_info, ram_info, slot_info, system_info, disks
        )
        
        # Información de periféricos
        peripherals_info = PeripheralsInfo()
        peripherals_data = peripherals_info.get_info()
        peripherals_data_formatted = PeripheralsInfo.format_for_report(peripherals_data)
        
        if progress:
            progress.set(80)
            progress.update_idletasks()
            
        # Generar bloques y agregar información al PDF
        PDFBlocks.generate_blocks(pdf.content, sections)
        PDFBlocks.add_peripherals_block(pdf.content, peripherals_data_formatted)
        PDFBlocks.add_processes_block(pdf.content, header, rows)
        recommendations = generate_recommendations(cpu_info, ram_info, disks, rows)
        
        # Recomendaciones técnicas
        PDFBlocks.add_recommendations_block(pdf.content, recommendations)
        
        if progress:
            progress.set(90)
            progress.update_idletasks()
            
        # Guardar PDF base y aplicar plantilla visual
        pdf.save_document()
        apply_template(names)
        
        if progress:
            progress.set(100)
            progress.update_idletasks()
        
        return True
        
    except Exception as e:
        # Manejo de errores global
        error_msg = f"Error en la generación del informe: {str(e)}"
        logging.error(error_msg)
        logging.error(traceback.format_exc())
        
        # Generar un PDF de error si es posible
        if pdf is not None and reports_dir is not None:
            try:
                error_pdf_path = str(reports_dir / "informe_error.pdf")
                error_pdf = PDFGenerator(error_pdf_path)
                error_pdf.add_tittle("ERROR EN LA GENERACIÓN DEL INFORME")
                error_pdf.add_paragraph(
                    f"Se produjo un error durante la generación del informe:\n\n"
                    f"{error_msg}\n\n"
                    f"Se ha creado un archivo de registro 'error_log.txt' con más detalles.",
                    "Detalles del Error"
                )
                error_pdf.save_document()
            except:
                pass
        
        return False

if __name__ == "__main__":
    main()