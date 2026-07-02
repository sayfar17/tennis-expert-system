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
        self.top.title("Evaluación de Caso - Flujo de Trabajo")
        self.top.geometry("700x520")
        self.top.resizable(False, False)

        self.bg_color = "#0F172A"
        self.card_color = "#1E293B"
        self.top.configure(bg=self.bg_color)

        self.controller = controller
        self.respuestas = {}
        self.dataset = dataset
        self.reglas = reglas

        self.frame_contenido = tk.Frame(
            self.top,
            bg=self.card_color,
            bd=0,
            highlightthickness=1,
            highlightbackground="#312B3D"
        )
        # Modifica esta línea en el __init__ de form_frame.py
        self.bg_color = self.frame_contenido.pack(expand=True, fill="both", padx=35, pady=35)

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
        # Le inyectamos la barra de progreso paso 1 (opcional si la agregaste)
        # self.dibujar_progreso(1)

        # Pasamos mostrar_sky como cuarto parámetro para la navegación hacia atrás
        form = TempForm(self.frame_contenido, self.respuestas, self.mostrar_humidity, self.mostrar_sky)
        form.pack(expand=True, fill="both")

    def mostrar_humidity(self):
        self.limpiar_frame()
        # Pasamos self.mostrar_wind como siguiente y self.mostrar_temp como el retorno hacia atrás
        form = HumidityForm(self.frame_contenido, self.respuestas, self.mostrar_wind, self.mostrar_temp)
        form.pack(expand=True, fill="both")

    def mostrar_wind(self):
        self.limpiar_frame()
        # Pasamos self.evaluar como proceso final y self.mostrar_humidity como retorno hacia atrás
        form = WindForm(self.frame_contenido, self.respuestas, self.evaluar, self.mostrar_humidity)
        form.pack(expand=True, fill="both")

    def evaluar(self):
        master = self.top.master
        self.top.destroy()

        cielo = self.respuestas.get("Cielo", "Soleado")
        temp = self.respuestas.get("Temperatura", "Caluroso")
        humedad = self.respuestas.get("Humedad", "Alta")
        viento = self.respuestas.get("Viento", "Flojo")

        try:
            resultado = self.controller.evaluate_case(cielo, temp, humedad, viento)
            ResultModal(master, resultado["explanation"])
        except Exception as e:
            messagebox.showerror("Error", f"Error al evaluar el caso:\n{str(e)}")

    def dibujar_progreso(self, paso_actual):
        """Dibuja una barra de progreso visual en la parte superior del contenedor"""
        frame_progreso = tk.Frame(self.frame_contenido, bg="#221F2B")
        frame_progreso.pack(fill="x", pady=(5, 15))

        pasos = ["Cielo", "Temperatura", "Humedad", "Viento"]

        for i, paso in enumerate(pasos):
            # Si ya pasamos este paso o es el actual, se ilumina en lila brillante
            color_bloque = "#9D85FF" if i <= paso_actual else "#312B3D"
            color_texto = "#16141A" if i <= paso_actual else "#B39DDB"

            lbl_paso = tk.Label(
                frame_progreso,
                text=f" {i + 1}. {paso} ",
                font=("Segoe UI", 9, "bold"),
                bg=color_bloque,
                fg=color_texto,
                bd=0
            )
            lbl_paso.pack(side="left", expand=True, fill="x", padx=4)