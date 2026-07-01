import tkinter as tk
from tkinter import messagebox
from ui.result_modal import ResultModal
from ui.sky_form import SkyForm
from ui.temp_form import TempForm
from ui.humidity_form import HumidityForm
from ui.wind_form import WindForm

class FormFrame:
    def __init__(self, parent, controller, dataset, reglas):
        self.top = tk.Toplevel(parent)
        self.top.title("Evaluación de Caso")
        # Extend geometry to fit tables better
        self.top.geometry("600x400")
        self.top.resizable(False, False)
        self.controller = controller
        self.respuestas = {}
        self.dataset = dataset
        self.reglas = reglas
        
        self.frame_contenido = tk.Frame(self.top)
        self.frame_contenido.pack(expand=True, fill="both", padx=20, pady=20)
        
        self.mostrar_dataset()

    def limpiar_frame(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

    def mostrar_dataset(self):
        self.limpiar_frame()
        from ui.dataset_form import DatasetForm
        form = DatasetForm(self.frame_contenido, self.dataset, self.mostrar_reglas)
        form.pack(expand=True, fill="both")

    def mostrar_reglas(self):
        self.limpiar_frame()
        from ui.rules_form import RulesForm
        form = RulesForm(self.frame_contenido, self.reglas, self.mostrar_sky)
        form.pack(expand=True, fill="both")

    def mostrar_sky(self):
        self.limpiar_frame()
        form = SkyForm(self.frame_contenido, self.respuestas, self.mostrar_temp)
        form.pack(expand=True, fill="both")

    def mostrar_temp(self):
        self.limpiar_frame()
        form = TempForm(self.frame_contenido, self.respuestas, self.mostrar_humidity)
        form.pack(expand=True, fill="both")

    def mostrar_humidity(self):
        self.limpiar_frame()
        form = HumidityForm(self.frame_contenido, self.respuestas, self.mostrar_wind)
        form.pack(expand=True, fill="both")

    def mostrar_wind(self):
        self.limpiar_frame()
        form = WindForm(self.frame_contenido, self.respuestas, self.evaluar)
        form.pack(expand=True, fill="both")

    def evaluar(self):
        # Guardar referencia al master antes de destruir
        master = self.top.master
        
        # Destruir la ventana del formulario
        self.top.destroy()
        
        cielo = self.respuestas.get("Cielo", "Soleado")
        temp = self.respuestas.get("Temperatura", "Caluroso")
        humedad = self.respuestas.get("Humedad", "Alta")
        viento = self.respuestas.get("Viento", "Flojo")
        
        try:
            resultado = self.controller.evaluate_case(cielo, temp, humedad, viento)
            # Pasamos master al ResultModal
            ResultModal(master, resultado["explanation"])
        except Exception as e:
            messagebox.showerror("Error", f"Error al evaluar el caso:\n{str(e)}")

