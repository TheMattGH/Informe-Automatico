import customtkinter as ctk
from customtkinter import CTkImage
from tkinter import messagebox
from PIL import Image
import os
import threading
import pythoncom
import traceback
from .main import main as generar_informe

class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Generador de Informes")
        self.geometry("420x400")
        self.resizable(False, False)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Logo proporcionado y centrado
        logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/assets/LOGOBA.png"))
        logo_img = Image.open(logo_path)
        max_width = 180
        if logo_img.width > max_width:
            ratio = max_width / logo_img.width
            new_size = (max_width, int(logo_img.height * ratio))
            logo_img = logo_img.resize(new_size, Image.LANCZOS)
        self.logo = CTkImage(light_image=logo_img, dark_image=logo_img, size=logo_img.size)
        ctk.CTkLabel(self, image=self.logo, text="").pack(pady=(18, 10))

        # Campos de entrada
        ctk.CTkLabel(self, text="Nombres:", font=ctk.CTkFont(size=15)).pack(pady=(5, 0))
        self.names = ctk.CTkEntry(self, width=240, font=ctk.CTkFont(size=14))
        self.names.pack(pady=(0, 15))

        ctk.CTkLabel(self, text="Departamento:", font=ctk.CTkFont(size=15)).pack()
        self.departament = ctk.CTkEntry(self, width=240, font=ctk.CTkFont(size=14))
        self.departament.pack(pady=(0, 20))

        # Barra de progreso (oculta al inicio)
        self.progress = ctk.CTkProgressBar(self, width=260)
        self.progress.set(0)
        self.progress.pack_forget()

        # Botón grande y moderno
        self.btn = ctk.CTkButton(self, text="Generar Informe", width=180, height=36, font=ctk.CTkFont(size=15), command=self.start_report)
        self.btn.pack(pady=10)

        # Mensaje de éxito (oculto al inicio)
        self.success_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=15), text_color="green")
        self.success_label.pack(pady=(18, 0))
        self.success_label.pack_forget()

        # Frame para los botones de acción (OK y Volver a generar)
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.ok_btn = ctk.CTkButton(self.action_frame, text="OK", width=120, command=self.close_app)
        self.again_btn = ctk.CTkButton(self.action_frame, text="Volver a generar", width=140, command=self.reset_form)
        self.ok_btn.pack(pady=(0, 8))
        self.again_btn.pack()
        self.action_frame.pack_forget()

        # Centrar ventana
        self.after(100, self.center_window)

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def start_report(self):
        if not self.names.get() or not self.departament.get():
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return
        names = self.names.get().title()
        departament = self.departament.get().title()

        self.btn.configure(state="disabled")
        self.progress.pack(pady=10)
        self.progress.set(0)
        self.success_label.pack_forget()
        self.action_frame.pack_forget()
        threading.Thread(target=self.run_report(names, departament)).start()

    def run_report(self, names, department):
        pythoncom.CoInitialize()
        try:
            self.progress.set(0.1)
            generar_informe(names, department, self.progress)
            self.progress.set(1)
            self.success_label.configure(text="¡Informe generado correctamente!")
            self.success_label.pack()
            self.action_frame.pack(pady=(10, 0))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error:\n{e}")
            print(traceback.format_exc())
        finally:
            self.btn.configure(state="normal")
            self.progress.pack_forget()

    def close_app(self):
        self.destroy()

    def reset_form(self):
        self.names.delete(0, "end")
        self.departament.delete(0, "end")
        self.success_label.pack_forget()
        self.action_frame.pack_forget()
        self.btn.configure(state="normal")

if __name__ == "__main__":
    app = App()
    app.mainloop()