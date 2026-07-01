"""
Módulo: rule_generator.py

Genera la base de conocimiento a partir de la
información obtenida por el algoritmo CHAID.
"""
class RuleGenerator:

    def __init__(self):
        """
        Inicializa el generador de reglas.
        """

        # Información obtenida desde CHAID
        self.knowledge_information = {}

        # Reglas generadas automáticamente
        self.generated_rules = []

        # Reglas esperadas (para validación)
        self.expected_rules = []
        
    # ==========================================================
    # CARGA DE INFORMACIÓN
    # ==========================================================

    def load_knowledge_information(self, knowledge_information):
        """
        Carga la información generada por el algoritmo CHAID.

        Args:
            knowledge_information (dict): Información obtenida
            mediante el método get_knowledge_information().
        """

        self.knowledge_information = knowledge_information
        
    def get_knowledge_information(self):
        """
        Devuelve la información cargada desde CHAID.

        Returns:
            dict
        """

        return self.knowledge_information
    
    def show_knowledge_information(self):
        """
        Muestra la información recibida desde el
        algoritmo CHAID.
        """

        print("\n========== INFORMACIÓN DEL CHAID ==========")

        if not self.knowledge_information:

            print("No existe información cargada.")

            print("===========================================")

            return

        print(
            f"Mejor predictor : "
            f"{self.knowledge_information['best_predictor']}"
        )

        print(
            f"Variable objetivo : "
            f"{self.knowledge_information['target_attribute']}"
        )

        print("\nSubconjuntos encontrados:")

        partitions = self.knowledge_information["dataset_partitions"]

        for value, records in partitions.items():

            print(f"  - {value}: {len(records)} registros")

        print("===========================================")
        
    # ==========================================================
    # CONSTRUCCIÓN DE REGLAS
    # ==========================================================
    
    def _build_rule(self, rule_id, conditions, decision):
        """
        Construye una regla del Sistema Experto.

        Args:
            rule_id (int): Identificador único.
            conditions (dict): Condiciones de la regla.
            decision (str): Conclusión de la regla.

        Returns:
            dict
        """

        return {

            "id": rule_id,

            "conditions": conditions,

            "decision": decision

        }
    
    def generate_rules(self):
        """
        Genera las reglas del Sistema Experto a partir de la
        información obtenida por el algoritmo CHAID.

        Returns:
            list: Lista de reglas generadas.
        """

        # Limpiar reglas generadas anteriormente
        self.generated_rules = []

        # Verificar que exista información cargada
        if not self.knowledge_information:
            raise ValueError(
                "No existe información cargada desde el algoritmo CHAID."
            )

        partitions = self.knowledge_information["dataset_partitions"]

        rule_id = 1

        # --------------------------------------------------
        # Cielo = Cubierto
        # --------------------------------------------------
        if "Cubierto" in partitions:

            self.generated_rules.append(
                self._build_rule(
                    rule_id=rule_id,
                    conditions={
                        "Cielo": "Cubierto"
                    },
                    decision="Si"
                )
            )

            rule_id += 1

        # --------------------------------------------------
        # Cielo = Soleado
        # --------------------------------------------------
        if "Soleado" in partitions:

            soleado = partitions["Soleado"]

            for registro in soleado:

                humedad = registro["Humedad"]
                decision = registro["Jugar"]

                # Evitar reglas duplicadas
                existe = any(
                    regla["conditions"] == {
                        "Cielo": "Soleado",
                        "Humedad": humedad
                    }
                    for regla in self.generated_rules
                )

                if not existe:

                    self.generated_rules.append(
                        self._build_rule(
                            rule_id=rule_id,
                            conditions={
                                "Cielo": "Soleado",
                                "Humedad": humedad
                            },
                            decision=decision
                        )
                    )

                    rule_id += 1

        # --------------------------------------------------
        # Cielo = Lluvioso
        # --------------------------------------------------
        if "Lluvioso" in partitions:

            lluvioso = partitions["Lluvioso"]

            for registro in lluvioso:

                viento = registro["Viento"]
                decision = registro["Jugar"]

                existe = any(
                    regla["conditions"] == {
                        "Cielo": "Lluvioso",
                        "Viento": viento
                    }
                    for regla in self.generated_rules
                )

                if not existe:

                    self.generated_rules.append(
                        self._build_rule(
                            rule_id=rule_id,
                            conditions={
                                "Cielo": "Lluvioso",
                                "Viento": viento
                            },
                            decision=decision
                        )
                    )

                    rule_id += 1

        return self.generated_rules
    
    # ==========================================================
    # CONSULTA DE REGLAS
    # ==========================================================

    def get_generated_rules(self):
        """
        Devuelve la lista de reglas generadas por el sistema.

        Returns:
            list: Lista de reglas generadas.
        """

        return self.generated_rules
    
    def show_generated_rules(self):
        """
        Muestra todas las reglas generadas en un formato
        legible para el usuario.
        """

        print("\n========== REGLAS GENERADAS ==========")

        if not self.generated_rules:

            print("No existen reglas generadas.")
            print("======================================")

            return

        for rule in self.generated_rules:

            print(f"\nRegla {rule['id']}")

            print("\nSI")

            conditions = rule["conditions"]

            total_conditions = len(conditions)

            for index, (attribute, value) in enumerate(conditions.items()):

                print(f"   {attribute} = {value}")

                if index < total_conditions - 1:
                    print("   Y")

            print("\nENTONCES")

            print(f"   Jugar = {rule['decision']}")

            print("--------------------------------------")

        print("======================================")
        
    # ==========================================================
    # VALIDACIÓN DE REGLAS
    # ==========================================================
    
    def compare_rules(self):
        """
        Compara las reglas generadas con las reglas
        esperadas del Sistema Experto.

        La comparación ignora el orden de las reglas.

        Returns:
            bool
        """

        if not self.expected_rules:

            raise ValueError(
                "No existen reglas esperadas para realizar la comparación."
            )

        if len(self.generated_rules) != len(self.expected_rules):

            return False

        for expected_rule in self.expected_rules:

            found = False

            for generated_rule in self.generated_rules:

                same_conditions = (
                    expected_rule["conditions"] ==
                    generated_rule["conditions"]
                )

                same_decision = (
                    expected_rule["decision"] ==
                    generated_rule["decision"]
                )

                if same_conditions and same_decision:

                    found = True

                    break

            if not found:

                return False

        return True
    
    # ==========================================================
    # VALIDACIÓN DE REGLAS
    # ==========================================================
    
    def load_expected_rules(self):
        """
        Carga las reglas esperadas del Sistema Experto.

        Estas reglas representan la base de conocimiento
        obtenida previamente mediante el algoritmo CHAID y
        serán utilizadas para validar las reglas generadas.
        """

        self.expected_rules = [

            self._build_rule(
                rule_id=1,
                conditions={
                    "Cielo": "Cubierto"
                },
                decision="Si"
            ),

            self._build_rule(
                rule_id=2,
                conditions={
                    "Cielo": "Soleado",
                    "Humedad": "Alta"
                },
                decision="No"
            ),

            self._build_rule(
                rule_id=3,
                conditions={
                    "Cielo": "Soleado",
                    "Humedad": "Normal"
                },
                decision="Si"
            ),

            self._build_rule(
                rule_id=4,
                conditions={
                    "Cielo": "Lluvioso",
                    "Viento": "flojo"
                },
                decision="Si"
            ),

            self._build_rule(
                rule_id=5,
                conditions={
                    "Cielo": "Lluvioso",
                    "Viento": "fuerte"
                },
                decision="No"
            )

        ]
    
    def get_expected_rules(self):
        """
        Devuelve las reglas esperadas.

        Returns:
            list
        """

        return self.expected_rules

    def show_expected_rules(self):
        """
        Muestra las reglas esperadas del Sistema Experto.
        """

        print("\n========== REGLAS ESPERADAS ==========")

        if not self.expected_rules:

            print("No existen reglas esperadas.")
            print("======================================")

            return

        for rule in self.expected_rules:

            print(f"\nRegla {rule['id']}")

            print("\nSI")

            total_conditions = len(rule["conditions"])

            for index, (attribute, value) in enumerate(rule["conditions"].items()):

                print(f"   {attribute} = {value}")

                if index < total_conditions - 1:
                    print("   Y")

            print("\nENTONCES")

            print(f"   Jugar = {rule['decision']}")

            print("--------------------------------------")

        print("======================================")
    
# ==========================================================
# RESUMEN DEL PROCESO
# ==========================================================

    def summary(self):
        """
        Muestra un resumen del proceso de generación
        de reglas.
        """

        print("\n========== RESUMEN DEL GENERADOR ==========")

        print(f"Total de reglas generadas : {len(self.generated_rules)}")

        if self.generated_rules:

            print("\nListado de reglas:")

            for rule in self.generated_rules:

                print(f"  • {rule['id']}")

        else:

            print("\nNo existen reglas generadas.")

        print("===========================================")