"""
Módulo: chaid.py

Implementa el algoritmo CHAID (Chi-square Automatic Interaction Detection)
para la generación automática de reglas de un Sistema Experto.

"""

class CHAID:

    def __init__(self):
        """
        Inicializa los atributos principales.
        """

        # Dataset completo
        self.dataset = []

        # Variable objetivo
        self.target_attribute = None

        # Variables predictoras
        self.predictor_attributes = []

        # Total de registros
        self.total_records = 0

        # Categorías de la variable objetivo
        self.target_categories = []

        # Tablas de contingencia
        self.contingency_tables = {}
        
        # Frecuencias esperadas
        self.expected_tables = {}
        
        # Estadísticos Chi-Cuadrado
        self.chi_square_results = {}
        
        # Grados de libertad
        self.degrees_of_freedom = {}

        # Valores críticos de Chi-Cuadrado
        self.critical_values = {}

        # Resultado de la prueba de significancia
        self.significance_results = {}
        
        # Mejor atributo seleccionado por CHAID
        self.best_predictor = None
        
        # Subconjuntos generados a partir del mejor atributo
        self.dataset_partitions = {}
        
        # Estructura lógica del árbol CHAID
        self.tree_structure = {}
        
    # ==========================================================
    # MÉTODO PRINCIPAL
    # ==========================================================

    def fit(self, dataset):
        
        # Validar que el dataset no esté vacío      
        if not dataset:
            raise ValueError("El dataset se encuentra vacío.")

        self.dataset = dataset

        self.total_records = len(dataset)

        self._identify_attributes()

        self._identify_target_categories()

        self._build_all_contingency_tables()
        
        self._build_all_expected_tables()
        
        self._calculate_all_chi_square()
        
        self._evaluate_all_significance()
        
        self._select_best_predictor()
        
        self._split_dataset()
        
        self._build_tree_structure()
        
        # VALIDACIÓN CRÍTICA
        if not self.contingency_tables:
            raise ValueError("No se generaron tablas de contingencia.")

        return True
            

    # ==========================================================
    # IDENTIFICACIÓN DE ATRIBUTOS
    # ==========================================================

    def _identify_attributes(self):
        """
        Identifica automáticamente la variable objetivo
        y las variables predictoras.
        """

        if not self.dataset:
            return

        attributes = list(self.dataset[0].keys())

        self.target_attribute = attributes[-1]

        self.predictor_attributes = attributes[:-1]

    # ==========================================================
    # CATEGORÍAS DE LA VARIABLE OBJETIVO
    # ==========================================================

    def _identify_target_categories(self):

        categories = set()

        for record in self.dataset:
            categories.add(record[self.target_attribute])

        self.target_categories = sorted(list(categories))

    # ==========================================================
    # TABLAS DE CONTINGENCIA
    # ==========================================================

    def _build_contingency_table(self, predictor):

        table = {}

        predictor_values = set()

        for record in self.dataset:
            predictor_values.add(record[predictor])

        for value in predictor_values:
            table[value] = {}

            for category in self.target_categories:
                table[value][category] = 0

        for record in self.dataset:
            predictor_value = record[predictor]
            target_value = record[self.target_attribute]

            table[predictor_value][target_value] += 1

        return table

    def _build_all_contingency_tables(self):
        """
        Construye las tablas de contingencia
        para todos los atributos predictoras.
        """

        self.contingency_tables = {}

        for predictor in self.predictor_attributes:

            self.contingency_tables[predictor] = (
                self._build_contingency_table(predictor)
            )

    # ==========================================================
    # MÉTODOS GET
    # ==========================================================

    def get_dataset(self):
        return self.dataset

    def get_target_attribute(self):
        return self.target_attribute

    def get_predictor_attributes(self):
        return self.predictor_attributes

    def get_total_records(self):
        return self.total_records

    def get_target_categories(self):
        return self.target_categories

    def get_contingency_tables(self):
        return self.contingency_tables

    # ==========================================================
    # MÉTODOS DE VISUALIZACIÓN
    # ==========================================================

    def summary(self):
        """
        Muestra información general del dataset.
        """

        print("\n=========== CHAID ===========")

        print(f"Total de registros : {self.total_records}")

        print(f"Variable objetivo  : {self.target_attribute}")

        print("\nCategorías objetivo:")

        for category in self.target_categories:
            print(f"  - {category}")

        print("\nVariables predictoras:")

        for predictor in self.predictor_attributes:
            print(f"  - {predictor}")

        print("=============================\n")

    def show_contingency_tables(self):
        """
        Muestra todas las tablas de contingencia.
        """

        print("\n========== TABLAS DE CONTINGENCIA ==========")

        for predictor, table in self.contingency_tables.items():

            print(f"\nAtributo predictor: {predictor}")

            print("-" * 45)

            for predictor_value, target_values in table.items():

                print(f"\n{predictor_value}")

                for target, frequency in target_values.items():

                    print(f"   {target}: {frequency}")

        print("\n============================================")
    
        
    def _calculate_row_totals(self, table):
        """
        Calcula el total de cada fila de una tabla de contingencia.

        Args:
            table (dict)

        Returns:
            dict
        """

        row_totals = {}

        for predictor_value, target_values in table.items():
            row_totals[predictor_value] = sum(target_values.values())

        return row_totals
    
    def _calculate_column_totals(self, table):
        """
        Calcula el total de cada columna.

        Args:
            table (dict)

        Returns:
            dict
        """

        column_totals = {}

        for category in self.target_categories:
            column_totals[category] = 0

        for target_values in table.values():

            for category, frequency in target_values.items():
                column_totals[category] += frequency

        return column_totals
    
    def _calculate_expected_table(self, table):
        """
        Calcula las frecuencias esperadas de una tabla.

        Args:
            table (dict)

        Returns:
            dict
        """

        expected = {}

        row_totals = self._calculate_row_totals(table)

        column_totals = self._calculate_column_totals(table)

        grand_total = self.total_records

        for predictor_value in table:

            expected[predictor_value] = {}

            for category in self.target_categories:

                expected_frequency = (
                    row_totals[predictor_value]
                    * column_totals[category]
                ) / grand_total

                expected[predictor_value][category] = round(
                    expected_frequency,
                    4
                )

        return expected
    
    def _build_all_expected_tables(self):
        """
        Calcula las frecuencias esperadas para
        todos los atributos predictoras.
        """

        self.expected_tables = {}

        for predictor in self.predictor_attributes:

            observed = self.contingency_tables[predictor]

            self.expected_tables[predictor] = (
                self._calculate_expected_table(observed)
            )
    
    
    def get_expected_tables(self):
        """
        Devuelve todas las tablas de frecuencias esperadas.

        Returns:
            dict
        """

        return self.expected_tables
    
    def show_expected_tables(self):
        """
        Muestra las frecuencias esperadas.
        """

        print("\n========== FRECUENCIAS ESPERADAS ==========")

        for predictor, table in self.expected_tables.items():

            print(f"\nAtributo predictor: {predictor}")

            print("-" * 45)

            for predictor_value, target_values in table.items():

                print(f"\n{predictor_value}")

                for category, value in target_values.items():

                    print(f"   {category}: {value:.4f}")

        print("\n===========================================")
        
    def _calculate_chi_square(self, predictor):
        """
        Calcula el estadístico Chi-Cuadrado para
        un atributo predictor.
            Args:                predictor (str)

            Returns:
            float
            """

        observed = self.contingency_tables[predictor]

        expected = self.expected_tables[predictor]

        chi_square = 0.0

        for predictor_value in observed:

            for category in self.target_categories:

                observed_frequency = observed[predictor_value][category]

                expected_frequency = expected[predictor_value][category]

                    # Evitar división por cero
                if expected_frequency == 0:
                    continue

                chi_square += (
                    (observed_frequency - expected_frequency) ** 2
                ) / expected_frequency

        return round(chi_square, 6)
        
    def _calculate_all_chi_square(self):
        """
        Calcula el estadístico Chi-Cuadrado
        para todos los atributos predictoras.
        """

        self.chi_square_results = {}

        for predictor in self.predictor_attributes:

            self.chi_square_results[predictor] = (
                self._calculate_chi_square(predictor)
            )
                
    def get_chi_square_results(self):
        """
        Devuelve todos los valores Chi-Cuadrado.

        Returns:
            dict
        """

        return self.chi_square_results
        
    def show_chi_square_results(self):
        """
        Muestra los valores Chi-Cuadrado
        obtenidos para cada atributo.
        """

        print("\n=========== CHI-CUADRADO ===========")

        for predictor, chi in self.chi_square_results.items():

            print(f"{predictor:<20}: {chi:.6f}")

        print("====================================")
            
    def _calculate_degrees_of_freedom(self, predictor):
        """
        Calcula los grados de libertad para
        una tabla de contingencia.

        Fórmula:
            (filas - 1) * (columnas - 1)
        """

        table = self.contingency_tables[predictor]

        rows = len(table)

        columns = len(self.target_categories)

        return (rows - 1) * (columns - 1)
    
    def _get_critical_value(self, degrees_of_freedom):
        """
        Devuelve el valor crítico de Chi-Cuadrado
        para α = 0.05.

        Fuente:
        Tabla de Chi-Cuadrado.
        """

        critical_table = {

            1: 3.841,
            2: 5.991,
            3: 7.815,
            4: 9.488,
            5: 11.070,
            6: 12.592,
            7: 14.067,
            8: 15.507,
            9: 16.919,
            10: 18.307

        }

        return critical_table.get(degrees_of_freedom, None)
    
    def _evaluate_all_significance(self):
        """
        Evalúa la significancia estadística
        para todos los atributos.
        """

        self.degrees_of_freedom = {}

        self.critical_values = {}

        self.significance_results = {}

        for predictor in self.predictor_attributes:

            df = self._calculate_degrees_of_freedom(predictor)

            critical = self._get_critical_value(df)

            chi = self.chi_square_results[predictor]

            significant = False

            if critical is not None:

                significant = chi > critical

            self.degrees_of_freedom[predictor] = df

            self.critical_values[predictor] = critical

            self.significance_results[predictor] = significant
            
    def get_significance_results(self):
        """
        Devuelve el resultado de la prueba
        de significancia.
        """

        return self.significance_results
    
    def show_significance_results(self):
        """
        Muestra la evaluación estadística
        de cada predictor.
        """

        print("\n========== SIGNIFICANCIA ==========")

        print(
            f"{'Atributo':<18}"
            f"{'χ²':<12}"
            f"{'GL':<8}"
            f"{'Crítico':<12}"
            f"{'Resultado'}"
        )

        print("-" * 60)

        for predictor in self.predictor_attributes:

            chi = self.chi_square_results[predictor]

            df = self.degrees_of_freedom[predictor]

            critical = self.critical_values[predictor]

            significant = self.significance_results[predictor]

            result = "Significativo" if significant else "No significativo"

            print(
                f"{predictor:<18}"
                f"{chi:<12.4f}"
                f"{df:<8}"
                f"{critical:<12.3f}"
                f"{result}"
            )

        print("=" * 60)
        
    def _select_best_predictor(self):
        """
        Selecciona el mejor atributo predictor.

        En esta implementación del Sistema Experto,
        el mejor predictor será aquel que posea el
        mayor valor de Chi-Cuadrado.

        La significancia estadística se conserva
        únicamente con fines informativos.
        """

        self.best_predictor = None

        best_chi = -1

        for predictor in self.predictor_attributes:

            chi = self.chi_square_results[predictor]

            if chi > best_chi:

                best_chi = chi

                self.best_predictor = predictor
    
    def get_best_predictor(self):
        """
        Devuelve el mejor atributo predictor.

        Returns:
            str
        """

        return self.best_predictor
    
    def show_best_predictor(self):
        """
        Muestra el atributo seleccionado por CHAID.
        """

        print("\n========== MEJOR ATRIBUTO ==========")

        if self.best_predictor is None:

            print("No existe un atributo significativo.")

        else:

            print(f"Atributo seleccionado: {self.best_predictor}")

            print(
                f"Chi-Cuadrado: "
                f"{self.chi_square_results[self.best_predictor]:.6f}"
            )

        print("====================================")
        
    def _split_dataset(self):
        """
        Divide el dataset utilizando el mejor atributo
        seleccionado por el algoritmo CHAID.

        Cada valor del atributo genera un subconjunto
        independiente.
        """

        self.dataset_partitions = {}

        # Si no existe un atributo significativo
        if self.best_predictor is None:
            return

        # Recorrer todos los registros
        for record in self.dataset:

            predictor_value = record[self.best_predictor]

            # Crear el subconjunto si aún no existe
            if predictor_value not in self.dataset_partitions:
                self.dataset_partitions[predictor_value] = []

            # Agregar el registro al subconjunto
            self.dataset_partitions[predictor_value].append(record)
    
    def get_dataset_partitions(self):
        """
        Devuelve los subconjuntos generados
        por la división del dataset.

        Returns:
            dict
        """

        return self.dataset_partitions
    
    def show_dataset_partitions(self):
        """
        Muestra un resumen de los subconjuntos
        generados por el algoritmo.
        """

        print("\n========== DIVISIÓN DEL DATASET ==========")

        if not self.dataset_partitions:

            print("No existen subconjuntos.")

            print("==========================================")

            return

        for value, records in self.dataset_partitions.items():

            print(f"\n{self.best_predictor} = {value}")

            print(f"Registros: {len(records)}")

        print("\n==========================================")
        
    def show_partition_details(self):
        """
        Muestra todos los registros contenidos
        en cada subconjunto.
        """

        print("\n========== DETALLE DE SUBCONJUNTOS ==========")

        for value, records in self.dataset_partitions.items():

            print(f"\n{self.best_predictor} = {value}")

            print("-" * 50)

            for record in records:
                print(record)

        print("\n=============================================")
        
    def _build_tree_structure(self):
        """
        Construye una representación lógica del árbol CHAID.

        Cada valor del mejor atributo se convierte en una
        rama del árbol.

        En esta primera implementación únicamente se genera
        el primer nivel del árbol.
        """

        self.tree_structure = {}

        if self.best_predictor is None:
            return

        self.tree_structure["attribute"] = self.best_predictor

        self.tree_structure["branches"] = {}

        for value, records in self.dataset_partitions.items():

            self.tree_structure["branches"][value] = records
            
    def get_tree_structure(self):
        """
        Devuelve la estructura lógica del árbol.

        Returns:
            dict
        """

        return self.tree_structure

    def show_tree_structure(self):
        """
        Muestra la estructura del árbol generado.
        """

        print("\n========== ÁRBOL CHAID ==========")

        if not self.tree_structure:

            print("No existe árbol.")

            return

        print(f"\nNodo raíz: {self.tree_structure['attribute']}")

        print("\nRamas:")

        for value, records in self.tree_structure["branches"].items():

            print(
                f"  ├── {value} ({len(records)} registros)"
            )

        print("\n=================================")
    
    def get_knowledge_information(self):
        """
        Devuelve toda la información necesaria para que
        RuleGenerator construya la base de conocimiento.

        Returns:
            dict
        """

        return {

            "best_predictor": self.best_predictor,

            "predictor_attributes": self.predictor_attributes,

            "dataset_partitions": self.dataset_partitions if isinstance(self.dataset_partitions, dict) else {},

            "tree_structure": self.tree_structure if isinstance(self.tree_structure, dict) else {},

            "target_attribute": self.target_attribute

        }