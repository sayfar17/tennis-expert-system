"""
Módulo: app.py
Punto de entrada del Sistema Experto 
"""
from knowledge_acquisition.dataset_loader import DatasetLoader

from controllers.expert_controller import ExpertController
from knowledge_acquisition.chaid import CHAID
from knowledge_acquisition.rule_generator import RuleGenerator
from tkinter import Tk
from tkinter.filedialog import askopenfilename

dataset_loader = DatasetLoader()
chaid = CHAID()
rule_generator = RuleGenerator()

def solicitar_dato(mensaje, opciones):
    while True:

        print(f"\nOpciones disponibles: {', '.join(opciones)}")

        valor = input(mensaje).strip().capitalize()

        if valor in opciones:
            return valor

        print("\n❌ Valor inválido. Intente nuevamente.")


def main():
    """
    Función principal del programa.
    """
    print("=" * 60)
    print("      SISTEMA EXPERTO PARA ENCUENTROS DE TENIS")
    print("=" * 60)

    print("\nCARGA DEL CONJUNTO DE DATOS")
    print("-" * 60)

    # Ocultar la ventana principal de Tkinter
    root = Tk()
    root.withdraw()

    ruta_dataset = askopenfilename(
        title="Seleccione el archivo del conjunto de datos",
        filetypes=[
            ("Archivos de texto", "*.txt"),
            ("Archivos CSV", "*.csv"),
            ("Todos los archivos", "*.*")
        ]
    )

    # Si el usuario cancela la selección
    if not ruta_dataset:
        print("\nNo se seleccionó ningún archivo.")
        return

    try:

        dataset = dataset_loader.load_dataset(ruta_dataset)

        print("\n✓ Dataset cargado correctamente.")
        print("\nProcesando conjunto de datos...")

        try:

            chaid.fit(dataset)
            knowledge_information = chaid.get_knowledge_information()

            rule_generator.load_knowledge_information(
                knowledge_information
            )

            print("✓ Algoritmo ejecutado correctamente.")

        except Exception as error:

            print("\n✗ Error durante la ejecución del algoritmo.")

            print(error)

            return
        
        print("\nGenerando reglas mediante CHAID...")

        try:

            rule_generator.generate_rules()

            print("✓ Reglas generadas correctamente.\n")

            rule_generator.show_generated_rules()
            
            input("\nPresione ENTER para iniciar el Sistema Experto...")

        except Exception as error:

            print("\n✗ Error al generar las reglas.")

            print(error)

            return
            
    except Exception as error:

        print("\n✗ Error al cargar el dataset.")
        print(error)

        return

    controller = ExpertController()

    print("=" * 60)
    print("      SISTEMA EXPERTO PARA ENCUENTROS DE TENIS")
    print("=" * 60)

    while True:

        print("\nIngrese las condiciones climáticas:\n")

        cielo = solicitar_dato(
            "Cielo: ",
            ["Soleado", "Cubierto", "Lluvioso"]
        )

        temperatura = solicitar_dato(
            "Temperatura: ",
            ["Caluroso", "Suave", "Fresco"]
        )

        humedad = solicitar_dato(
            "Humedad: ",
            ["Alta", "Normal"]
        )

        viento = solicitar_dato(
            "Viento: ",
            ["Flojo", "Fuerte"]
        )

        # Ejecutar el sistema experto
        resultado = controller.evaluate_case(
            cielo,
            temperatura,
            humedad,
            viento
        )

        # Mostrar la explicación generada
        print(resultado["explanation"])

        # Consultar si desea realizar otra evaluación
        continuar = input(
            "\n¿Desea realizar otra consulta? (S/N): "
        ).strip().upper()

        if continuar != "S":
            print("\nGracias por utilizar el Sistema Experto.")
            break


if __name__ == "__main__":
    main()