import tkinter as tk
from tkinter import messagebox

class WindForm(tk.Frame):
    def __init__(self, parent, respuestas, on_finish):
        super().__init__(parent)
        self.respuestas = respuestas
        self.on_finish = on_finish
        self.opciones = ["Flojo", "Fuerte"]
        self.checkbox_vars = {}

        lbl_titulo = tk.Label(self, text="Seleccione Viento:", font=("Arial", 14, "bold"))
        lbl_titulo.pack(pady=10)

        for opcion in self.opciones:
            var = tk.BooleanVar(value=False)
            self.checkbox_vars[opcion] = var
            chk = tk.Checkbutton(
                self, 
                text=opcion, 
                variable=var, 
                font=("Arial", 12),
                command=lambda o=opcion: self.uncheck_others(o)
            )
            chk.pack(anchor="w", padx=40, pady=5)
        
        btn_evaluar = tk.Button(self, text="Evaluar Caso", command=self.evaluar,
                                font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", width=15)
        btn_evaluar.pack(pady=20)

    def uncheck_others(self, selected_option):
        if self.checkbox_vars[selected_option].get():
            for op in self.opciones:
                if op != selected_option:
                    self.checkbox_vars[op].set(False)

    def evaluar(self):
        seleccion = [op for op, var in self.checkbox_vars.items() if var.get()]
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione una opción para Viento.")
            return
        
        self.respuestas["Viento"] = seleccion[0]
        self.on_finish()
