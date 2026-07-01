import tkinter as tk

class ResultModal:
    def __init__(self, parent, resultado_texto):
        self.top = tk.Toplevel(parent)
        self.top.title("Resultado de Evaluación")
        self.top.geometry("400x300")
        
        lbl_titulo = tk.Label(self.top, text="Resultado del Sistema Experto", font=("Arial", 12, "bold"))
        lbl_titulo.pack(pady=10)

        # Utilizamos un Text widget en lugar de Label por si el texto es muy largo
        txt_resultado = tk.Text(self.top, wrap="word", width=45, height=10, font=("Arial", 10))
        txt_resultado.insert("1.0", resultado_texto)
        txt_resultado.config(state="disabled") # Solo lectura
        txt_resultado.pack(padx=20, pady=10)

        btn_cerrar = tk.Button(self.top, text="Cerrar", command=self.top.destroy,
                               font=("Arial", 10), bg="#f44336", fg="white", width=15)
        btn_cerrar.pack(pady=10)

        # Para que el modal bloquee la ventana de atrás (opcional)
        self.top.grab_set()
