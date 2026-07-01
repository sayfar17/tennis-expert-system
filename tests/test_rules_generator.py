"""
Archivo de prueba del módulo RuleGenerator.

Este archivo permite verificar el funcionamiento de la
fase de adquisición del conocimiento antes de integrarla
con el Sistema Experto.
"""
import os
import sys

# Agregar la carpeta raíz del proyecto al PATH
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, PROJECT_ROOT)

from knowledge_acquisition.dataset_loader import DatasetLoader
from knowledge_acquisition.chaid import CHAID
from knowledge_acquisition.rule_generator import RuleGenerator


def main():
    """
    Ejecuta una prueba completa del algoritmo CHAID y
    del generador de reglas.
    """

    print("\n==============================================")
    print("      PRUEBA DEL GENERADOR DE REGLAS")
    print("==============================================")

    # --------------------------------------------------
    # Cargar dataset
    # --------------------------------------------------

    dataset_loader = DatasetLoader()
    
    # Construir la ruta completa del dataset
    dataset_path = os.path.join(
        "..",
        "data",
        "Tenis.txt"
    )

    dataset = dataset_loader.load_dataset(dataset_path)

    print("\nDataset cargado correctamente.")

    # --------------------------------------------------
    # Ejecutar CHAID
    # --------------------------------------------------

    chaid = CHAID()

    chaid.fit(dataset)

    print("\nAlgoritmo CHAID ejecutado correctamente.")

    # --------------------------------------------------
    # Crear RuleGenerator
    # --------------------------------------------------

    rule_generator = RuleGenerator()

    # Cargar información desde CHAID

    rule_generator.load_knowledge_information(

        chaid.get_knowledge_information()

    )

    # Mostrar información recibida

    rule_generator.show_knowledge_information()

    # --------------------------------------------------
    # Generar reglas
    # --------------------------------------------------

    rule_generator.generate_rules()

    # Mostrar reglas generadas

    rule_generator.show_generated_rules()

    # --------------------------------------------------
    # Cargar reglas esperadas
    # --------------------------------------------------

    rule_generator.load_expected_rules()

    # Mostrar reglas esperadas

    rule_generator.show_expected_rules()

    # --------------------------------------------------
    # Comparar reglas
    # --------------------------------------------------

    print("\n==============================================")
    print("VALIDACIÓN")

    if rule_generator.compare_rules():

        print("Resultado : CORRECTO")

        print("Las reglas generadas coinciden con")
        print("las reglas esperadas.")

    else:

        print("Resultado : INCORRECTO")

        print("Existen diferencias entre las reglas.")

    print("==============================================")

    # --------------------------------------------------
    # Resumen
    # --------------------------------------------------

    rule_generator.summary()


if __name__ == "__main__":

    main()