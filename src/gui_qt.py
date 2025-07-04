import sys
import os
import time
import shutil
import traceback
from pathlib import Path

from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                              QLabel, QLineEdit, QPushButton, QProgressBar,
                              QFileDialog, QMessageBox, QHBoxLayout)
from PySide6.QtCore import Qt, Signal, QObject, QThread
from PySide6.QtGui import QPixmap, QFont

from .main import main as generar_informe

# Clase para manejar el hilo de generación del informe
class InformeWorker(QObject):
    finished = Signal()
    error = Signal(str)
    progress = Signal(int)
    
    def __init__(self, names, department):
        super().__init__()
        self.names = names
        self.department = department
    
    def run(self):
        try:
            # Simulación de progreso visual
            for pct in [10, 30, 60, 80]:
                self.progress.emit(pct)
                time.sleep(0.3)
                
            # Clase simulada para emular la barra de progreso
            class ProgressEmulator:
                def __init__(self, signal):
                    self.signal = signal
                
                def set(self, value):
                    self.signal.emit(int(value * 100))
                    
                def update_idletasks(self):
                    pass
                    
            # Generar el informe con barra de progreso
            generar_informe(self.names, self.department, ProgressEmulator(self.progress))
            self.progress.emit(100)
            self.finished.emit()
            
        except Exception as e:
            self.error.emit(str(e))


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generador de Informes Automático")
        self.setFixedSize(420, 400)
        self.thread = None
        self.worker = None
        
        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Layout principal
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        # Logo
        logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/assets/LOGOBA.png"))
        logo_pixmap = QPixmap(logo_path)
        max_width = 180
        if logo_pixmap.width() > max_width:
            logo_pixmap = logo_pixmap.scaledToWidth(max_width, Qt.SmoothTransformation)
            
        logo_label = QLabel()
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(logo_label)
        self.layout.addSpacing(10)
        
        # Campos de entrada - Nombres
        name_label = QLabel("Nombre y Apellido:")
        name_label.setFont(QFont("Arial", 10))
        self.layout.addWidget(name_label)
        
        self.names = QLineEdit()
        self.names.setMinimumHeight(30)
        self.names.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.names)
        self.layout.addSpacing(15)
        
        # Campos de entrada - Departamento
        dept_label = QLabel("Departamento:")
        dept_label.setFont(QFont("Arial", 10))
        self.layout.addWidget(dept_label)
        
        self.departament = QLineEdit()
        self.departament.setMinimumHeight(30)
        self.departament.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.departament)
        self.layout.addSpacing(20)
        
        # Container para botón y barra de progreso (para poder alternarlos)
        self.action_container = QWidget()
        self.action_container_layout = QVBoxLayout(self.action_container)
        self.action_container_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.action_container)
        
        # Botón principal
        self.btn = QPushButton("Generar Informe")
        self.btn.setMinimumHeight(40)  # Más alto
        self.btn.setMinimumWidth(200)  # Más ancho
        self.btn.setFont(QFont("Arial", 11, QFont.Bold))  # Fuente más grande y en negrita
        self.btn.setStyleSheet("""
            QPushButton {
                background-color: #1E88E5;
                color: white;
                border-radius: 6px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """)
        self.btn.clicked.connect(self.start_report)
        self.action_container_layout.addWidget(self.btn, alignment=Qt.AlignCenter)
        
        # Barra de progreso (oculta al inicio)
        self.progress_widget = QWidget()
        self.progress_layout = QVBoxLayout(self.progress_widget)
        self.progress_layout.setContentsMargins(0, 0, 0, 0)
        
        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setValue(0)
        self.progress.setFixedWidth(280)  # Más ancha
        self.progress.setMinimumHeight(20)  # Más alta
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #BDBDBD;
                border-radius: 5px;
                background-color: #F5F5F5;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
                border-radius: 5px;
            }
        """)
        self.progress_layout.addWidget(self.progress, alignment=Qt.AlignCenter)
        
        # Mensaje de progreso
        self.generating_label = QLabel("Generando informe...")
        self.generating_label.setStyleSheet("font-size: 14px; margin-top: 8px;")
        self.generating_label.setAlignment(Qt.AlignCenter)
        self.progress_layout.addWidget(self.generating_label)
        
        # Agregar pero inicialmente oculto
        self.action_container_layout.addWidget(self.progress_widget)
        self.progress_widget.setVisible(False)
        
        # Mensaje de éxito (oculto al inicio)
        self.success_label = QLabel()
        self.success_label.setStyleSheet("color: green; font-size: 16px; font-weight: bold; margin: 10px 0;")
        self.success_label.setAlignment(Qt.AlignCenter)
        self.success_label.setVisible(False)
        self.layout.addWidget(self.success_label)
        
        # Frame para los botones de acción
        self.action_frame = QWidget()
        self.action_layout = QVBoxLayout(self.action_frame)
        self.action_layout.setSpacing(12)  # Más espacio entre botones
        
        # Botones horizontales
        self.buttons_container = QWidget()
        self.buttons_layout = QHBoxLayout(self.buttons_container)
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons_layout.setSpacing(20)  # Espacio entre botones
        
        # Botón Generar de nuevo - PRIMERO para que aparezca a la izquierda
        self.again_btn = QPushButton("Generar de nuevo")
        self.again_btn.setMinimumWidth(160)
        self.again_btn.setMinimumHeight(38)  # Más alto
        self.again_btn.setFont(QFont("Arial", 10, QFont.Bold))
        self.again_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        self.again_btn.clicked.connect(self.reset_form)
        self.buttons_layout.addWidget(self.again_btn)
        
        # Botón Salir - SEGUNDO para que aparezca a la derecha
        self.ok_btn = QPushButton("Salir")
        self.ok_btn.setMinimumWidth(140)
        self.ok_btn.setMinimumHeight(38)  # Más alto
        self.ok_btn.setFont(QFont("Arial", 10, QFont.Bold))
        self.ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """)
        self.ok_btn.clicked.connect(self.close_app)
        self.buttons_layout.addWidget(self.ok_btn)
        
        self.action_layout.addWidget(self.buttons_container)
        self.layout.addWidget(self.action_frame)
        self.action_frame.setVisible(False)
        
        # Centrar ventana
        self.center_window()
        
        # Aplicar estilo global
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
            QLabel {
                color: #333333;
            }
            QLineEdit {
                border: 1px solid #BDBDBD;
                border-radius: 4px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #2196F3;
            }
        """)
    
    def center_window(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
    
    def start_report(self):
        if not self.names.text() or not self.departament.text():
            QMessageBox.critical(self, "Error", "Por favor, complete todos los campos.")
            return
            
        # Aplicar Title Case a los campos
        names = " ".join(word.capitalize() for word in self.names.text().split())
        department = " ".join(word.capitalize() for word in self.departament.text().split())
        
        # Actualizar los campos con el texto formateado
        self.names.setText(names)
        self.departament.setText(department)
        
        # Configurar interfaz para estado de generación
        self.btn.setVisible(False)  # Ocultar el botón
        self.progress_widget.setVisible(True)  # Mostrar el widget de progreso
        self.progress.setValue(0)
        self.success_label.setVisible(False)
        self.action_frame.setVisible(False)
        
        # Crear worker y thread
        self.thread = QThread()
        self.worker = InformeWorker(names, department)
        self.worker.moveToThread(self.thread)
        
        # Conectar señales
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_report_finished)
        self.worker.error.connect(self.on_report_error)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        
        # Iniciar proceso
        self.thread.start()
    
    def update_progress(self, value):
        self.progress.setValue(value)
    
    def on_report_finished(self):
        try:
            # Ruta del informe generado
            reports_dir = Path(__file__).resolve().parent.parent / "reports"
            safe_names = "".join(c for c in self.names.text() if c.isalnum() or c in (" ", "_", "-")).strip()
            informe_final = reports_dir / f"Informe Técnico {safe_names}.pdf"
            
            # Diálogo para guardar como...
            destino, _ = QFileDialog.getSaveFileName(
                self,
                "Guardar informe como...",
                f"Informe Técnico {safe_names}.pdf",
                "PDF files (*.pdf)"
            )
            
            if destino:
                shutil.copy(str(informe_final), destino)
            
            # Actualizar UI para mostrar éxito
            self.success_label.setText("¡Informe generado correctamente!")
            self.success_label.setVisible(True)
            self.action_frame.setVisible(True)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al guardar el informe:\n{e}")
            print(traceback.format_exc())
        finally:
            # Ocultar elementos de progreso
            self.progress_widget.setVisible(False)
            # No mostrar el botón principal hasta que se reinicie
    
    def on_report_error(self, error_msg):
        QMessageBox.critical(self, "Error", f"Ocurrió un error:\n{error_msg}")
        print(traceback.format_exc())
        
        # Reset UI
        self.progress_widget.setVisible(False)
        self.btn.setVisible(True)
    
    def close_app(self):
        self.close()
    
    def reset_form(self):
        self.names.clear()
        self.departament.clear()
        self.success_label.setVisible(False)
        self.action_frame.setVisible(False)
        self.btn.setVisible(True)  # Mostrar botón nuevamente


# Función de inicio
def run():
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run()