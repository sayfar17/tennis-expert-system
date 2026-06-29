"""
Módulo: inference.py

Implementa el Motor de Inferencia del Sistema Experto.

Su función es comparar los hechos ingresados por el usuario con
las reglas almacenadas en la Base de Conocimiento y determinar
cuál de ellas se cumple.

"""
from knowledge_base.knowledge import KnowledgeBase

class InferenceEngine:
    """
    Motor de Inferencia del Sistema Experto.
    """

    def __init__(self):
        """
        Inicializa el motor de inferencia cargando la Base de
        Conocimiento.
        """

        self.knowledge_base = KnowledgeBase()

    def evaluate(self, facts):
        """
        Evalúa los hechos ingresados contra todas las reglas.

        Args:
            facts (Facts):
                Base de hechos del sistema.

        Returns:
            dict:
                Resultado de la inferencia.
        """

        rules = self.knowledge_base.get_rules()

        for rule in rules:

            rule_matches = True

            for attribute, expected_value in rule["conditions"].items():

                user_value = facts.get_fact(attribute)

                if user_value != expected_value:
                    rule_matches = False
                    break

            if rule_matches:

                return {
                    "success": True,
                    "rule": rule
                }

        return {
            "success": False,
            "rule": None
        }