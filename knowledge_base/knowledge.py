"""
Módulo: knowledge.py

Este módulo administra la Base de Conocimiento del Sistema Experto.

Su responsabilidad es proporcionar acceso a las reglas almacenadas
en rules.py sin que otros módulos conozcan cómo están implementadas.

"""

from knowledge_base.rules import RULES

class KnowledgeBase:
    """
    Representa la Base de Conocimiento del Sistema Experto.

    Contiene todas las reglas obtenidas 
    y proporciona métodos para acceder a ellas.
    """

    def __init__(self):
        """
        Inicializa la Base de Conocimiento cargando todas las reglas.
        """

        self._rules = RULES

    def get_rules(self):
        """
        Devuelve todas las reglas de la Base de Conocimiento.

        Returns:
            list:
                Lista con todas las reglas del sistema experto.
        """

        return self._rules

    def get_rule_by_id(self, rule_id):
        """
        Busca una regla utilizando su identificador.

        Args:
            rule_id (int):
                Identificador único de la regla.

        Returns:
            dict | None:
                La regla encontrada o None si no existe.
        """

        for rule in self._rules:
            if rule["id"] == rule_id:
                return rule

        return None

    def total_rules(self):
        """
        Devuelve la cantidad de reglas almacenadas.

        Returns:
            int:
                Número total de reglas.
        """

        return len(self._rules)