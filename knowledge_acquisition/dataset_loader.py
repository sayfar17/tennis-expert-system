"""
Módulo: dataset_loader.py

Este módulo implementa el cargador de conjuntos de datos del
Sistema Experto.

Su responsabilidad es leer archivos de diferentes formatos
(TXT, CSV y JSON), validar su contenido y convertirlos a una
estructura uniforme que será utilizada posteriormente por el
algoritmo CHAID.

"""
import os
import csv
import json

class DatasetLoader:
    """
    Permite cargar conjuntos de datos desde diferentes formatos.

    Formatos soportados:
        - .txt
        - .csv
        - .json
    """

    # ---------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------

    def __init__(self):
        """
        Inicializa el cargador.
        """

        self.dataset = []

    # ---------------------------------------------------------
    # Método público principal
    # ---------------------------------------------------------

    def load_dataset(self, file_path):
        """
        Carga un conjunto de datos desde un archivo.

        Args:
            file_path (str):
                Ruta del archivo.

        Returns:
            list:
                Lista de registros del dataset.

        Raises:
            FileNotFoundError:
                Si el archivo no existe.

            ValueError:
                Si el formato no es soportado.
        """

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"No existe el archivo: {file_path}"
            )

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".csv":
            self.dataset = self._load_csv(file_path)

        elif extension == ".txt":
            self.dataset = self._load_txt(file_path)

        elif extension == ".json":
            self.dataset = self._load_json(file_path)

        else:
            raise ValueError(
                f"Formato '{extension}' no soportado."
            )

        if len(self.dataset) == 0:
            raise ValueError(
                "El conjunto de datos está vacío."
            )

        return self.dataset

    # ---------------------------------------------------------
    # Lectura de archivos CSV
    # ---------------------------------------------------------

    def _load_csv(self, file_path):
        """
        Lee un archivo CSV.

        Returns:
            list
        """

        dataset = []

        with open(file_path, mode="r", encoding="utf-8") as file:

            reader = csv.DictReader(file)

            for row in reader:
                dataset.append(dict(row))

        return dataset

    # ---------------------------------------------------------
    # Lectura de archivos TXT
    # ---------------------------------------------------------

    def _load_txt(self, file_path):
        """
        Lee un archivo TXT separado por tabulaciones.

        Returns:
            list
        """

        dataset = []

        with open(file_path, mode="r", encoding="utf-8") as file:

            reader = csv.DictReader(
                file,
                delimiter="\t"
            )

            for row in reader:
                dataset.append(dict(row))

        return dataset

    # ---------------------------------------------------------
    # Lectura de archivos JSON
    # ---------------------------------------------------------

    def _load_json(self, file_path):
        """
        Lee un archivo JSON.

        El archivo debe contener una lista de objetos.

        Returns:
            list
        """

        with open(file_path, mode="r", encoding="utf-8") as file:

            dataset = json.load(file)

        return dataset

    # ---------------------------------------------------------
    # Información del dataset
    # ---------------------------------------------------------

    def get_total_records(self):
        """
        Devuelve el número de registros.

        Returns:
            int
        """

        return len(self.dataset)

    def get_attributes(self):
        """
        Obtiene los nombres de las columnas.

        Returns:
            list
        """

        if len(self.dataset) == 0:
            return []

        return list(self.dataset[0].keys())

    def get_total_attributes(self):
        """
        Devuelve la cantidad de atributos.

        Returns:
            int
        """

        return len(self.get_attributes())

    def get_dataset(self):
        """
        Devuelve el dataset completo.

        Returns:
            list
        """

        return self.dataset

    # ---------------------------------------------------------
    # Mostrar resumen
    # ---------------------------------------------------------

    def summary(self):
        """
        Imprime un resumen del conjunto de datos.
        """

        print("\n=========== DATASET ===========")

        print(f"Registros : {self.get_total_records()}")

        print(f"Atributos : {self.get_total_attributes()}")

        print("Columnas  :")

        for attribute in self.get_attributes():
            print(f"   - {attribute}")

        print("===============================\n")
    
    def show_algorithm_results(self):
        """
        Muestra un resumen completo del algoritmo.
        """

        self.summary()

        self.show_chi_square_results()

        self.show_significance_results()

        self.show_best_predictor()

        self.show_dataset_partitions()