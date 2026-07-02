import tkinter as tk
from tkinter import messagebox


class WindForm(tk.Frame):
    def __init__(self, parent, respuestas, on_next, on_back):
        super().__init__(parent, bg="#0F172A")
        self.respuestas = respuestas
        self.on_next = on_next
        self.on_back = on_back
        self.opciones = ["Fuerte", "Flojo"]
        self.opcion_seleccionada = None
        self.botones_dict = {}

        lbl_titulo = tk.Label(self, text="Fuerza del Viento", font=("Segoe UI", 16, "bold"), bg="#0F172A", fg="#F3E5F5")
        lbl_titulo.pack(pady=(35, 5))

        lbl_pregunta = tk.Label(self, text="Selecciona la intensidad del viento registrada:", font=("Segoe UI", 11),
                                bg="#0F172A", fg="#94A3B8")
        lbl_pregunta.pack(pady=(0, 25))

        frame_opciones = tk.Frame(self, bg="#0F172A")
        frame_opciones.pack(pady=10)

        for opcion in self.opciones:
            icono = "💨" if opcion == "Fuerte" else "🍃"

            btn = tk.Button(
                frame_opciones,
                text=f"{icono}\n\n{opcion}",
                font=("Segoe UI", 11, "bold"),
                bg="#1E293B", fg="#F3E5F5",
                activebackground="#F59E0B", activeforeground="#0F172A",
                bd=0, width=14, height=4, cursor="hand2",
                command=lambda o=opcion: self.seleccionar(o)
            )
            btn.pack(side="left", padx=12)
            self.botones_dict[opcion] = btn
            self.aplicar_hover(btn, "#1E293B", "#334155")

        frame_navegacion = tk.Frame(self, bg="#0F172A")
        frame_navegacion.pack(pady=(45, 20))

        btn_atras = tk.Button(
            frame_navegacion, text="⬅ Atrás", command=self.on_back,
            font=("Segoe UI", 11, "bold"), bg="#1E293B", fg="#94A3B8",
            activebackground="#0F172A", activeforeground="#F3E5F5",
            bd=0, width=12, height=2, cursor="hand2"
        )
        btn_atras.pack(side="left", padx=10)
        self.aplicar_hover(btn_atras, "#1E293B", "#334155")

        # Botón final para procesar la inferencia
        self.btn_siguiente = tk.Button(
            frame_navegacion, text="Evaluar Caso 🎾", command=self.siguiente,
            font=("Segoe UI", 11, "bold"), bg="#F59E0B", fg="#0F172A",
            activebackground="#D97706", activeforeground="#F3E5F5",
            bd=0, width=16, height=2, cursor="hand2"
        )
        self.btn_siguiente.pack(side="left", padx=10)
        self.aplicar_hover(self.btn_siguiente, "#F59E0B", "#FBBF24")

        self.lbl_error = tk.Label(self, text="", font=("Segoe UI", 10), bg="#0F172A", fg="#F87171")
        self.lbl_error.pack(pady=10)

    def aplicar_hover(self, boton, color_normal, color_hover):
        boton.bind("<Enter>", lambda e: self.on_enter(boton, color_hover))
        boton.bind("<Leave>", lambda e: self.on_leave(boton, color_normal))

    def on_enter(self, boton, color_hover):
        if b := [op for op, btn in self.botones_dict.items() if btn == boton]:
            if b[0] == self.opcion_seleccionada:
                return
        boton.config(bg=color_hover)

    def on_leave(self, boton, color_normal):
        if b := [op for op, btn in self.botones_dict.items() if btn == boton]:
            if b[0] == self.opcion_seleccionada:
                return
        boton.config(bg=color_normal)

    def seleccionar(self, opcion):
        for op, btn in self.botones_dict.items():
            btn.config(bg="#1E293B", fg="#F3E5F5")
        self.opcion_seleccionada = opcion
        self.botones_dict[opcion].config(bg="#F59E0B", fg="#0F172A")
        self.lbl_error.config(text="")

    def siguiente(self):
        if not self.opcion_seleccionada:
            self.lbl_error.config(text="⚠️ Por favor, seleccione una opción de viento antes de continuar.")
            return
        self.respuestas["Viento"] = self.opcion_seleccionada
        self.on_next()