import tkinter as tk
from tkinter import ttk


class RulesForm(tk.Frame):
    def __init__(self, parent, reglas, on_next):
        super().__init__(parent, bg="#221F2B")
        self.reglas = reglas
        self.on_next = on_next

        lbl_titulo = tk.Label(self, text="Reglas Generadas (CHAID) 🧠", font=("Segoe UI", 15, "bold"), bg="#221F2B",
                              fg="#F3E5F5")
        lbl_titulo.pack(pady=15)

        frame_texto = tk.Frame(self, bg="#221F2B")
        frame_texto.pack(expand=True, fill="both", padx=15, pady=5)

        txt_reglas = tk.Text(
            frame_texto, wrap="word", font=("Consolas", 10), bg="#16141A", fg="#B39DDB",
            insertbackground="#F3E5F5", bd=0, highlightthickness=1, highlightbackground="#312B3D", height=15
        )

        scrollbar_y = ttk.Scrollbar(frame_texto, orient="vertical", command=txt_reglas.yview)
        txt_reglas.configure(yscrollcommand=scrollbar_y.set)
        txt_reglas.pack(side="left", expand=True, fill="both")
        scrollbar_y.pack(side="right", fill="y")

        if not self.reglas:
            txt_reglas.insert("1.0", "No existen reglas generadas.")
        else:
            contenido = ""
            for rule in self.reglas:
                contenido += f" ──  Regla {rule['id']}  ──\n"
                contenido += " SI\n"
                conditions = rule["conditions"]
                total_conditions = len(conditions)

                for index, (attribute, value) in enumerate(conditions.items()):
                    contenido += f"    {attribute} = {value}\n"
                    if index < total_conditions - 1:
                        contenido += "    Y\n"

                contenido += " ENTONCES\n"
                contenido += f"    Jugar = {rule['decision']}\n"
                contenido += "─" * 45 + "\n\n"

            txt_reglas.insert("1.0", contenido)

        txt_reglas.config(state="disabled")

        btn_siguiente = tk.Button(
            self, text="Siguiente", command=self.on_next,
            font=("Segoe UI", 11, "bold"), bg="#9D85FF", fg="#16141A",
            activebackground="#7E65DD", activeforeground="#16141A",
            bd=0, width=18, height=2, cursor="hand2"
        )
        btn_siguiente.pack(pady=20)