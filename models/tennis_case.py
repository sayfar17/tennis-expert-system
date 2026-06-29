"""
Módulo: tennis_case.py

Este módulo define la clase TennisCase, la cual representa un caso
de consulta para el sistema experto.

Cada objeto almacena las condiciones climáticas ingresadas por el usuario.

"""

class TennisCase:
    """
    Representa un caso de consulta del sistema experto.

    Atributos:
        cielo (str): Estado del cielo.
        temperatura (str): Temperatura ambiente.
        humedad (str): Nivel de humedad.
        viento (str): Intensidad del viento.
    """

    def __init__(self, cielo, temperatura, humedad, viento):
        """
        Constructor de la clase.

        Args:
            cielo (str): Soleado, Cubierto o Lluvioso.
            temperatura (str): Caluroso, Suave o Fresco.
            humedad (str): Alta o Normal.
            viento (str): Flojo o Fuerte.
        """

        self.cielo = cielo
        self.temperatura = temperatura
        self.humedad = humedad
        self.viento = viento

    def __str__(self):
        """
        Devuelve una representación legible del caso.

        Returns:
            str: Información del caso.
        """

        return (
            f"Cielo: {self.cielo}\n"
            f"Temperatura: {self.temperatura}\n"
            f"Humedad: {self.humedad}\n"
            f"Viento: {self.viento}"
        )