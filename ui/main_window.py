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
        self.root.title("Menú Principal - Sistema Experto")
        self.root.geometry("400x350")
        self.root.resizable(False, False)

        # Título del curso
        tk.Label(self.root, text="Curso: Sistemas Expertos 2026-A",
                 font=("Arial", 14, "bold")).pack(pady=5)
        tk.Label(self.root, text="Integrantes:", font=("Arial", 12)).pack(pady=5)
        tk.Label(self.root, text="- Chamorro Martel, Juan\n- Lopez Sanchez, Farid\n- Olivares Melendez, Johan\n- Palpan Rimac, Sergio\n- Pastor Fuero, Abraham\n- Veli Moya, Luis",
                 font=("Arial", 10)).pack(pady=5)

        self.btn_cargar = tk.Button(self.root, text="Cargar Dataset e Iniciar",
                                command=self.cargar_dataset,
                                font=("Arial", 10), bg="#2196F3", fg="white", width=25)
        self.btn_cargar.pack(pady=10)
        
        self.controller = None

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
        # Abre la ventana del formulario (sistema experto)
        if self.controller:
            FormFrame(self.root, self.controller, dataset, reglas)

    def run(self):
        self.root.mainloop()