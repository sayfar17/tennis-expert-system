import tkinter as tk


class ResultModal:
    def __init__(self, parent, explanation):
        self.top = tk.Toplevel(parent)
        self.top.title("Reporte Meteorológico de Pista")
        self.top.geometry("540x410")
        self.top.resizable(False, False)
        self.top.grab_set()

        # Colores de la app meteorológica
        self.bg_color = "#0F172A"
        self.card_color = "#1E293B"
        self.top.configure(bg=self.bg_color)

        se_juega = "Jugar = Si" in explanation or "Jugar = Sí" in explanation
        color_reporte = "#F59E0B" if se_juega else "#38BDF8"  # Ámbar Cálido / Azul Tormenta
        estado_pista = "CONDICIONES ÓPTIMAS PARA EL PARTIDO 🎾" if se_juega else "CONDICIONES DESFAVORABLES EN PISTA ❌"

        # Tarjeta de Reporte Principal
        card = tk.Frame(self.top, bg=self.card_color, bd=0, highlightthickness=1, highlightbackground="#334155")
        card.pack(fill="both", expand=True, padx=25, pady=25)

        # Encabezado del Reporte
        lbl_status = tk.Label(
            card,
            text=estado_pista,
            font=("Segoe UI", 13, "bold"),
            bg=self.card_color,
            fg=color_reporte
        )
        lbl_status.pack(pady=(20, 10))

        # Divisor sutil de app móvil
        divisor = tk.Frame(card, bg="#334155", height=1)
        divisor.pack(fill="x", padx=20, pady=5)

        tk.Label(
            card,
            text="Análisis Predictivo Avanzado:",
            font=("Segoe UI", 10, "bold"),
            bg=self.card_color,
            fg="#94A3B8"
        ).pack(anchor="w", padx=20, pady=(10, 5))

        # Cuadro de texto limpio donde el motor de inferencia vacía la explicación
        txt_explicacion = tk.Text(
            card,
            wrap="word",
            font=("Segoe UI", 10),
            bg="#0F172A",
            fg="#F3E5F5",
            bd=0,
            highlightthickness=1,
            highlightbackground="#334155",
            padx=15,
            pady=15,
            height=7
        )
        txt_explicacion.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        # Damos un formato pulido al reporte interno
        clean_exp = explanation.replace("Jugar = Si", "Resultado -> Apto para Jugar").replace("Jugar = No",
                                                                                              "Resultado -> No Apto")
        txt_explicacion.insert("1.0", clean_exp)
        txt_explicacion.config(state="disabled")

        # Botón de Cierre
        btn_cerrar = tk.Button(
            card,
            text="Volver al Panel",
            command=self.top.destroy,
            font=("Segoe UI", 11, "bold"),
            bg=color_reporte,
            fg="#0F172A",
            activebackground="#F3E5F5",
            bd=0,
            height=2,
            cursor="hand2"
        )
        btn_cerrar.pack(fill="x", padx=20, pady=(0, 20))