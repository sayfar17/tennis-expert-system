import tkinter as tk
from tkinter import ttk

class DatasetForm(tk.Frame):
    def __init__(self, parent, dataset, on_next):
        super().__init__(parent)
        self.dataset = dataset
        self.on_next = on_next

        lbl_titulo = tk.Label(self, text="Conjunto de Datos Cargado", font=("Arial", 14, "bold"))
        lbl_titulo.pack(pady=10)

        # Crear Frame para la tabla y el scrollbar
        frame_tabla = tk.Frame(self)
        frame_tabla.pack(expand=True, fill="both", padx=10, pady=5)

        if not self.dataset:
            tk.Label(frame_tabla, text="No hay datos disponibles.", font=("Arial", 10)).pack(pady=20)
        else:
            # Obtener columnas
            columnas = list(self.dataset[0].keys())

            tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=8)
            
            # Configurar columnas
            for col in columnas:
                tree.heading(col, text=col)
                # Ajustar ancho de las columnas
                tree.column(col, width=80, anchor="center")

            # Insertar datos
            for fila in self.dataset:
                valores = [fila.get(col, "") for col in columnas]
                tree.insert("", "end", values=valores)

            # Scrollbar vertical
            scrollbar_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar_y.set)
            
            # Posicionar elementos
            tree.pack(side="left", expand=True, fill="both")
            scrollbar_y.pack(side="right", fill="y")
        
        btn_siguiente = tk.Button(self, text="Siguiente", command=self.on_next,
                                  font=("Arial", 10, "bold"), bg="#2196F3", fg="white", width=15)
        btn_siguiente.pack(pady=20)
