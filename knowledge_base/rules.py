"""
Módulo: rules.py

Este módulo almacena la Base de Conocimiento del sistema experto.

Las reglas fueron obtenidas previamente mediante el algoritmo CHAID
y representan el conocimiento utilizado para decidir si se debe
jugar un encuentro de tenis.

"""

# ==========================
# BASE DE CONOCIMIENTO
# ==========================

RULES = [

    {
        "id": 1,
        "description": "Si el cielo es Cubierto, entonces jugar = Sí.",
        "conditions": {
            "cielo": "Cubierto"
        },
        "decision": "Sí"
    },

    {
        "id": 2,
        "description": "Si el cielo es Soleado y la humedad es Alta, entonces jugar = No.",
        "conditions": {
            "cielo": "Soleado",
            "humedad": "Alta"
        },
        "decision": "No"
    },

    {
        "id": 3,
        "description": "Si el cielo es Soleado y la humedad es Normal, entonces jugar = Sí.",
        "conditions": {
            "cielo": "Soleado",
            "humedad": "Normal"
        },
        "decision": "Sí"
    },

    {
        "id": 4,
        "description": "Si el cielo es Lluvioso y el viento es Flojo, entonces jugar = Sí.",
        "conditions": {
            "cielo": "Lluvioso",
            "viento": "Flojo"
        },
        "decision": "Sí"
    },

    {
        "id": 5,
        "description": "Si el cielo es Lluvioso y el viento es Fuerte, entonces jugar = No.",
        "conditions": {
            "cielo": "Lluvioso",
            "viento": "Fuerte"
        },
        "decision": "No"
    }

]