import tkinter as tk
from tkinter import ttk

class RulesForm(tk.Frame):
    def __init__(self, parent, reglas, on_next):
        super().__init__(parent)
        self.reglas = reglas
        self.on_next = on_next

        lbl_titulo = tk.Label(self, text="Reglas Generadas (CHAID)", font=("Arial", 14, "bold"))
        lbl_titulo.pack(pady=10)

        frame_texto = tk.Frame(self)
        frame_texto.pack(expand=True, fill="both", padx=10, pady=5)

        txt_reglas = tk.Text(frame_texto, wrap="word", font=("Courier", 10), bg="#f5f5f5", height=15)
        
        scrollbar_y = ttk.Scrollbar(frame_texto, orient="vertical", command=txt_reglas.yview)
        txt_reglas.configure(yscrollcommand=scrollbar_y.set)

        txt_reglas.pack(side="left", expand=True, fill="both")
        scrollbar_y.pack(side="right", fill="y")

        # Formatear e insertar las reglas
        if not self.reglas:
            txt_reglas.insert("1.0", "No existen reglas generadas.")
        else:
            contenido = ""
            for rule in self.reglas:
                contenido += f"Regla {rule['id']}\n"
                contenido += "SI\n"
                
                conditions = rule["conditions"]
                total_conditions = len(conditions)
                
                for index, (attribute, value) in enumerate(conditions.items()):
                    contenido += f"   {attribute} = {value}\n"
                    if index < total_conditions - 1:
                        contenido += "   Y\n"
                
                contenido += "ENTONCES\n"
                contenido += f"   Jugar = {rule['decision']}\n"
                contenido += "-" * 40 + "\n\n"

            txt_reglas.insert("1.0", contenido)
        
        txt_reglas.config(state="disabled") # Solo lectura

        btn_siguiente = tk.Button(self, text="Siguiente", command=self.on_next,
                                  font=("Arial", 10, "bold"), bg="#2196F3", fg="white", width=15)
        btn_siguiente.pack(pady=20)
