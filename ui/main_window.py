import tkinter as tk
from tkinter import filedialog, messagebox
from knowledge_acquisition.dataset_loader import DatasetLoader
from knowledge_acquisition.chaid import CHAID
from knowledge_acquisition.rule_generator import RuleGenerator
from controllers.expert_controller import ExpertController
from ui.form_frame import FormFrame


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema Experto - UNDAC")
        self.root.geometry("720x460")  # Dimensiones balanceadas
        self.root.resizable(False, False)

        # Paleta de colores elegante y minimalista (Sutil Modo Oscuro)
        self.bg_color = "#121118"  # Fondo oscuro premium
        self.card_color = "#1C1B22"  # Fondo de contenedores
        self.sidebar_color = "#16151C"  # Lateral sutil
        self.accent_color = "#9D85FF"  # Lila de acento principal
        self.text_light = "#F3E5F5"  # Texto principal claro
        self.text_muted = "#A5A1B8"  # Texto secundario elegante

        self.root.configure(bg=self.bg_color)
        self.controller = None

        # ─── 1. PANEL LATERAL (INFORMACIÓN INSTITUCIONAL) ───
        sidebar = tk.Frame(self.root, bg=self.sidebar_color, width=260, bd=0, highlightthickness=1,
                           highlightbackground="#2A2835")
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Encabezado limpio de la Universidad
        tk.Label(sidebar, text="UNDAC", font=("Segoe UI", 26, "bold"), bg=self.sidebar_color,
                 fg=self.accent_color).pack(pady=(45, 5))
        tk.Label(sidebar, text="Ingeniería de Sistemas y Computación", font=("Segoe UI", 10), bg=self.sidebar_color,
                 fg=self.text_light).pack(pady=(0, 25))

        # Línea divisoria muy fina y sutil
        tk.Frame(sidebar, bg="#2A2835", height=1, width=200).pack(pady=10)

        # Detalles del proyecto presentados de forma limpia
        details_frame = tk.Frame(sidebar, bg=self.sidebar_color)
        details_frame.pack(fill="x", padx=25, pady=15)

        detalles = [
            ("Proyecto:", "Sistema Experto de Tenis"),
            ("Algoritmo:", "CHAID"),
            ("Curso:", "Sistemas Expertos"),
            ("Semestre:", "IX - 2026-A")
        ]

        for titulo, valor in detalles:
            row = tk.Frame(details_frame, bg=self.sidebar_color)
            row.pack(fill="x", pady=6)
            tk.Label(row, text=titulo, font=("Segoe UI", 9, "bold"), bg=self.sidebar_color, fg=self.text_muted,
                     width=10, anchor="w").pack(side="left")
            tk.Label(row, text=valor, font=("Segoe UI", 10), bg=self.sidebar_color, fg=self.text_light,
                     anchor="w").pack(side="left")

        # ─── 2. PANEL PRINCIPAL (INTEGRANTES Y ACCIÓN) ───
        main_panel = tk.Frame(self.root, bg=self.bg_color)
        main_panel.pack(side="right", fill="both", expand=True, padx=25, pady=25)

        # Tarjeta contenedora para los integrantes
        card_integrantes = tk.Frame(main_panel, bg=self.card_color, bd=0, highlightthickness=1,
                                    highlightbackground="#2A2835")
        card_integrantes.pack(fill="both", expand=True, pady=(0, 20))

        tk.Label(card_integrantes, text="Integrantes del Grupo", font=("Segoe UI", 12, "bold"), bg=self.card_color,
                 fg=self.text_light).pack(pady=(20, 15), anchor="w", padx=25)

        # Lista de nombres bien alineada y limpia (Fuera fuentes raras de consola)
        frame_lista = tk.Frame(card_integrantes, bg=self.card_color)
        frame_lista.pack(fill="both", expand=True, padx=25, pady=(0, 20))

        integrantes = [
            "•  Chamorro Martel, Juan Carlos",
            "•  Lopez Sanchez, Farid Sebastian",
            "•  Olivares Melendez, Johan Alexander",
            "•  Palpan Rimac, Sergio Alfredo",
            "•  Pastor Fuero, Abraham",
            "•  Veli Moya, Luis Fernando"
        ]

        for nombre in integrantes:
            tk.Label(
                frame_lista,
                text=nombre,
                font=("Segoe UI", 11),
                bg=self.card_color,
                fg=self.text_light,
                anchor="w"
            ).pack(fill="x", pady=4)

        # Botón de Inicio Comercial / Moderno
        self.btn_cargar = tk.Button(
            main_panel,
            text="Cargar Dataset e Iniciar Componente",
            command=self.cargar_dataset,
            font=("Segoe UI", 11, "bold"),
            bg=self.accent_color,
            fg="#121118",
            activebackground="#B39DDB",
            activeforeground="#121118",
            bd=0,
            cursor="hand2",
            height=2
        )
        self.btn_cargar.pack(fill="x")
        self.aplicar_hover(self.btn_cargar, self.accent_color, "#B39DDB")

    def aplicar_hover(self, boton, color_normal, color_hover):
        boton.bind("<Enter>", lambda e: boton.config(bg=color_hover))
        boton.bind("<Leave>", lambda e: boton.config(bg=color_normal))

    def cargar_dataset(self):
        ruta_dataset = filedialog.askopenfilename(
            title="Seleccione el archivo del conjunto de datos",
            filetypes=[
                ("Archivos de texto", "*.txt"),
                ("Archivos CSV", "*.csv"),
                ("Todos los archivos", "*.*")
            ]
        )

        if not ruta_dataset:
            return

        try:
            dataset_loader = DatasetLoader()
            dataset = dataset_loader.load_dataset(ruta_dataset)

            chaid = CHAID()
            chaid.fit(dataset)
            knowledge_information = chaid.get_knowledge_information()

            rule_generator = RuleGenerator()
            rule_generator.load_knowledge_information(knowledge_information)
            reglas = rule_generator.generate_rules()

            messagebox.showinfo("Éxito", "Dataset cargado y reglas generadas correctamente.")

            self.controller = ExpertController()
            self.abrir_sistema_experto(dataset, reglas)

        except Exception as error:
            messagebox.showerror("Error", f"Ocurrió un error:\n{str(error)}")

    def abrir_sistema_experto(self, dataset, reglas):
        if self.controller:
            FormFrame(self.root, self.controller, dataset, reglas)

    def run(self):
        self.root.mainloop()