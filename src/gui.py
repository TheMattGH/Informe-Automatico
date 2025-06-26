import tkinter as tk
from tkinter import ttk, messagebox
import threading
from .main import main as generar_informe

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Generador de Informes")
        self.geometry("400x300")
        self.resizable(False, False)

        tk.Label(self, text="Nombres:").pack(pady=(20,0))
        self.names = tk.Entry(self)
        self.names.pack()

        tk.Label(self, text="Departamento:").pack()
        self.departament = tk.Entry(self)
        self.departament.pack()

        self.progress = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=20)

        self.btn = tk.Button(self, text="Generar Informe", command=self.start_report)
        self.btn.pack()

    def start_report(self):
        if not self.names.get() or not self.departament.get():
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return
        self.btn.config(state="disabled")
        threading.Thread(target=self.run_report).start()

    def run_report(self):
        import pythoncom
        pythoncom.CoInitialize()
        # Aquí puedes actualizar la barra de progreso en pasos si divides main()
        self.progress["value"] = 10
        generar_informe(self.names.get(), self.departament.get(), self.progress)
        self.progress["value"] = 100
        messagebox.showinfo("Listo", "¡Informe generado!")
        self.btn.config(state="normal")

if __name__ == "__main__":
    app = App()
    app.mainloop()