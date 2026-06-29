"""
Módulo: facts.py

Este módulo representa la Base de Hechos (Working Memory) del
Sistema Experto.

Su responsabilidad es almacenar los hechos proporcionados por
el usuario durante una consulta.

Estos hechos serán utilizados posteriormente por el Motor de
Inferencia para determinar qué regla de la Base de Conocimiento
se cumple.

"""

class Facts:
    """
    Representa la Base de Hechos del Sistema Experto.

    Los hechos corresponden a las condiciones climáticas
    ingresadas por el usuario.
    """

    def __init__(self, cielo, temperatura, humedad, viento):
        """
        Inicializa la Base de Hechos.

        Args:
            cielo (str):
                Estado del cielo.

            temperatura (str):
                Temperatura registrada.

            humedad (str):
                Nivel de humedad.

            viento (str):
                Intensidad del viento.
        """

        self.facts = {
            "cielo": cielo,
            "temperatura": temperatura,
            "humedad": humedad,
            "viento": viento
        }

    def get_fact(self, attribute):
        """
        Obtiene el valor de un hecho específico.

        Args:
            attribute (str):
                Nombre del atributo.

        Returns:
            str:
                Valor asociado al atributo solicitado.
        """

        return self.facts.get(attribute)

    def get_all_facts(self):
        """
        Devuelve todos los hechos almacenados.

        Returns:
            dict:
                Diccionario con todos los hechos.
        """

        return self.facts

    def __str__(self):
        """
        Devuelve una representación legible de los hechos.

        Returns:
            str
        """

        return (
            f"Cielo: {self.facts['cielo']}\n"
            f"Temperatura: {self.facts['temperatura']}\n"
            f"Humedad: {self.facts['humedad']}\n"
            f"Viento: {self.facts['viento']}"
        )