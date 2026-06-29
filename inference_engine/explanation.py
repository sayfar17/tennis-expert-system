"""
Módulo: explanation.py

Este módulo implementa el Sistema de Explicación del Sistema Experto.

Su responsabilidad es generar una explicación clara y comprensible
para el usuario sobre la decisión obtenida por el Motor de Inferencia.

"""

class ExplanationEngine:
    """
    Genera una explicación del razonamiento realizado
    por el Sistema Experto.
    """

    def generate(self, facts, inference_result):
        """
        Genera una explicación detallada de la inferencia.

        Args:
            facts (Facts):
                Base de hechos.

            inference_result (dict):
                Resultado producido por el Motor de Inferencia.

        Returns:
            str:
                Explicación completa.
        """

        if not inference_result["success"]:

            return (
                "\n================ SISTEMA EXPERTO ================\n\n"
                "No fue posible emitir una recomendación.\n\n"
                "Motivo:\n"
                "Ninguna regla de la Base de Conocimiento coincide "
                "con los hechos ingresados.\n\n"
                "================================================="
            )

        rule = inference_result["rule"]

        # Determinar la recomendación final
        if rule["decision"] == "Sí":
            recommendation = "Se recomienda JUGAR el encuentro de tenis."
        else:
            recommendation = "Se recomienda NO JUGAR el encuentro de tenis."

        # Construir los hechos ingresados
        facts_text = ""

        for attribute, value in facts.get_all_facts().items():
            facts_text += f"- {attribute.capitalize()}: {value}\n"

        explanation = (
            "\n================ SISTEMA EXPERTO ================\n\n"
            "RESULTADO\n"
            "---------\n"
            f"{recommendation}\n\n"
            "HECHOS INGRESADOS\n"
            "-----------------\n"
            f"{facts_text}\n"
            "REGLA APLICADA\n"
            "--------------\n"
            f"Regla {rule['id']}\n"
            f"{rule['description']}\n\n"
            "CONCLUSIÓN\n"
            "----------\n"
            "Los hechos ingresados cumplen completamente las "
            "condiciones de la regla indicada, por lo que el "
            "Sistema Experto emite la recomendación mostrada.\n\n"
            "================================================="
        )

        return explanation