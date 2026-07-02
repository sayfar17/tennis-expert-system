import tkinter as tk
from tkinter import ttk


class DatasetForm(tk.Frame):
    def __init__(self, parent, dataset, on_next):
        super().__init__(parent, bg="#221F2B")
        self.dataset = dataset
        self.on_next = on_next

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="#312B3D", foreground="#F3E5F5", font=("Segoe UI", 10, "bold"),
                        borderwidth=0)
        style.configure("Treeview", background="#221F2B", foreground="#F3E5F5", fieldbackground="#221F2B", rowheight=26,
                        font=("Segoe UI", 10), borderwidth=0, highlightthickness=0)
        style.map("Treeview", background=[("selected", "#9D85FF")], foreground=[("selected", "#16141A")])

        lbl_titulo = tk.Label(self, text="Conjunto de Datos Cargado 📊", font=("Segoe UI", 15, "bold"), bg="#221F2B",
                              fg="#F3E5F5")
        lbl_titulo.pack(pady=15)

        frame_tabla = tk.Frame(self, bg="#221F2B")
        frame_tabla.pack(expand=True, fill="both", padx=15, pady=5)

        if not self.dataset:
            tk.Label(frame_tabla, text="No hay datos disponibles.", font=("Segoe UI", 11), bg="#221F2B",
                     fg="#B39DDB").pack(pady=30)
        else:
            columnas = list(self.dataset[0].keys())
            tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=8)

            for col in columnas:
                tree.heading(col, text=col)
                tree.column(col, width=90, anchor="center")

            for fila in self.dataset:
                valores = [fila.get(col, "") for col in columnas]
                tree.insert("", "end", values=valores)

            scrollbar_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar_y.set)

            tree.pack(side="left", expand=True, fill="both")
            scrollbar_y.pack(side="right", fill="y")

        btn_siguiente = tk.Button(
            self, text="Siguiente", command=self.on_next,
            font=("Segoe UI", 11, "bold"), bg="#9D85FF", fg="#16141A",
            activebackground="#7E65DD", activeforeground="#16141A",
            bd=0, width=18, height=2, cursor="hand2"
        )
        btn_siguiente.pack(pady=20)