"""
Módulo: expert_controller.py
Este módulo coordina el funcionamiento del Sistema Experto.

Actúa como intermediario entre la interfaz de usuario
(consola o interfaz gráfica) y los componentes internos
del sistema experto.

"""
from models.tennis_case import TennisCase
from knowledge_base.facts import Facts
from inference_engine.inference import InferenceEngine
from inference_engine.explanation import ExplanationEngine

class ExpertController:
    """
    Controlador principal del Sistema Experto.
    """

    def __init__(self):

        self.inference_engine = InferenceEngine()
        self.explanation_engine = ExplanationEngine()

    def evaluate_case(self, cielo, temperatura, humedad, viento):
        """
        Evalúa un caso utilizando el Sistema Experto.
        """

        # Crear el caso de consulta
        tennis_case = TennisCase(
            cielo,
            temperatura,
            humedad,
            viento
        )

        # Construir la Base de Hechos
        facts = Facts(
            cielo,
            temperatura,
            humedad,
            viento
        )

        # Ejecutar la inferencia
        inference_result = self.inference_engine.evaluate(facts)

        # Generar la explicación
        explanation = self.explanation_engine.generate(
            facts,
            inference_result
        )

        # Retornar toda la información
        return {
            "case": tennis_case,
            "facts": facts,
            "inference": inference_result,
            "explanation": explanation
        }