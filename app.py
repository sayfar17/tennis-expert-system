"""
Módulo: app.py
Punto de entrada del Sistema Experto 
"""
from controllers.expert_controller import ExpertController

def solicitar_dato(mensaje, opciones):
    """
    Solicita un dato al usuario y valida que pertenezca
    a las opciones permitidas.

    Args:
        mensaje (str):
            Mensaje mostrado al usuario.

        opciones (list):
            Lista de opciones válidas.

    Returns:
        str:
            Valor ingresado por el usuario.
    """

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