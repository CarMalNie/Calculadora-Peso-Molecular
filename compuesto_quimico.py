import re
from datos_quimicos import obtener_peso_atomico, es_simbolo_valido

class CompuestoQuimico:
    """
    Representa un compuesto químico. Usa @property para una gestión de atributos controlada.
    """

    def __init__(self, formula_str: str):
        # Inicializamos atributos privados.
        self._formula = "" 
        self._elementos_conteo = {} 
        self._peso_molecular = 0.0
        self._es_valido = False 
        self._mensaje_error = ""
        
        # Llama al setter, disparando la validación y el cálculo central.
        self.formula = formula_str 

    
    ## MÉTODO DE REPRESENTACIÓN __str__ ##
    
    def __str__(self):
        """
        Devuelve una representación legible para humanos del compuesto, con PM a 3 decimales.
        Formato: Compuesto: H2O | Peso Molecular: 18.015 g/mol | Elementos: Hx2, Ox1
        """
        if not self.es_valido:
            return f"Compuesto: {self.formula} | Error: {self.mensaje_error}"
            
        # Construye la parte de elementos: Hx2, Ox1, etc.
        elementos_list = [f"{simbolo}x{cantidad}" for simbolo, cantidad in self.elementos_conteo.items()]
        elementos_str = ", ".join(elementos_list)
        
        return "Compuesto: {} | Peso Molecular: {:.3f} g/mol | Elementos: {}".format(
            self.formula,
            self.peso_molecular,
            elementos_str
        )
    
    
    ## GETTER/SETTER @PROPERTY PARA LA FÓRMULA (VALIDACIÓN CENTRAL) ##
        
    @property
    def formula(self) -> str:
        """ Getter: Permite acceder a la fórmula (ej: mi_compuesto.formula)."""
        return self._formula

    @formula.setter
    def formula(self, nueva_formula_str: str):
        """ Setter: Asigna la fórmula, limpia el estado y dispara la validación/cálculo."""
        formula_limpia = nueva_formula_str.strip()
        
        self._establecer_error("") 
        
        if not formula_limpia:
            self._establecer_error("La fórmula no puede estar vacía.")
            return

        self._formula = formula_limpia
        
        self._analizar_y_calcular()
        
    
    ## PROPIEDADES (GETTERS) RESTANTES ##

    @property
    def peso_molecular(self) -> float:
        """ Getter: Obtiene el PM. Acceso vía mi_compuesto.peso_molecular """
        return self._peso_molecular

    @property
    def es_valido(self) -> bool:
        """ Getter: Verifica el estado de validez. Acceso vía mi_compuesto.es_valido """
        return self._es_valido

    @property
    def mensaje_error(self) -> str:
        """ Getter: Obtiene el mensaje de error. Acceso vía mi_compuesto.mensaje_error """
        return self._mensaje_error
        
    @property
    def elementos_conteo(self) -> dict:
        """ Getter: Obtiene el conteo de elementos. Acceso vía mi_compuesto.elementos_conteo """
        return self._elementos_conteo
        
    
    ## LÓGICA INTERNA DE CÁLCULO (STACK) ##

    def _establecer_error(self, mensaje: str):
        """ Método auxiliar para establecer el estado de error de forma consistente. """
        self._es_valido = False
        self._peso_molecular = 0.0
        self._elementos_conteo = {}
        self._mensaje_error = mensaje


    def _analizar_formula_compleja(self, formula_original: str):
        """
        Implementación ROBUSTA con STACK para contar elementos y manejar agrupadores ((), []). 
        """
        conteo = {}
        # Pila de factores de grupo (siempre empieza en 1)
        multiplicadores_stack = [1] 
        # Factor actual de multiplicación acumulado del grupo más interno
        factor_actual = 1           
        
        # Patrón simple: capturar el token que esperamos encontrar: Símbolo, Número, Agrupador.
        tokens = re.findall(r'([A-Z][a-z]?|\d+|[()\[\]\{\}])', formula_original)
        tokens.reverse() # Procesar de Derecha a Izquierda
        
        ultimo_subindice = 1 # Subíndice del elemento/grupo que precede inmediatamente

        for token in tokens:
            
            # Caso 1: Dígito (Subíndice de Grupo/Elemento)
            if token.isdigit():
                ultimo_subindice = int(token)
            
            # Caso 2: Paréntesis/Corchete de CIERRE (en la fórmula original: ), ])
            elif token in [')', ']']:
                factor_actual *= ultimo_subindice
                multiplicadores_stack.append(factor_actual)
                ultimo_subindice = 1 
            
            # Caso 3: Paréntesis/Corchete de APERTURA (en la fórmula original: (, [)
            elif token in ['(', '[']:
                if len(multiplicadores_stack) > 1:
                    multiplicadores_stack.pop()
                    factor_actual = multiplicadores_stack[-1]
                    ultimo_subindice = 1
                else:
                    raise ValueError(f"Agrupador de apertura ('{token}') encontrado sin su cierre correspondiente. Verifique que no falte un subíndice o un agrupador de cierre.")

            # Caso 4: Símbolo Químico (Elemento)
            elif token.isalpha():
                simbolo = token
                
                # --- VALIDACIÓN DE AMBIGÜEDAD/CAPITALIZACIÓN (Ej. CU vs Cu) ---
                if len(simbolo) == 2 and simbolo.isupper():
                    simbolo_capitalizado = simbolo.capitalize()
                    if es_simbolo_valido(simbolo_capitalizado):
                        raise ValueError(f"Símbolo ambiguo: '{simbolo}' (dos mayúsculas). La notación IUPAC correcta es '{simbolo_capitalizado}' (Ej: Cobre).")
                
                if not es_simbolo_valido(simbolo):
                    raise ValueError(f"Símbolo no reconocido: '{simbolo}'. Debe ser un elemento químico válido (IUPAC).")

                # Calcular la cantidad total: Subíndice propio * Factor del Grupo
                cantidad_total = ultimo_subindice * factor_actual

                conteo[simbolo] = conteo.get(simbolo, 0) + cantidad_total
                
                ultimo_subindice = 1 

            else:
                raise ValueError(f"Sintaxis inválida: Carácter o token no reconocido: '{token}'.")

        # Comprobación de errores finales
        if len(multiplicadores_stack) > 1:
            raise ValueError("Fórmula incompleta: Falta cerrar uno o más agrupadores (paréntesis/corchetes).")
            
        if not conteo:
            raise ValueError("Fórmula vacía o la sintaxis es completamente inválida.")

        return conteo
        
    def _calcular_peso(self):
        """ Calcula el peso molecular total a partir del conteo de elementos. """
        peso_total = 0.0
        for simbolo, cantidad in self._elementos_conteo.items():
            peso_atomico = obtener_peso_atomico(simbolo)
            
            if peso_atomico == 0.0:
                raise Exception(f"No se pudo obtener el peso atómico para '{simbolo}'.")

            peso_total += peso_atomico * cantidad
        
        self._peso_molecular = peso_total


    def _analizar_y_calcular(self):
        """
        Método central que orquesta el análisis y el cálculo.
        """
        try:
            formula_a_analizar = self._formula 
            
            self._elementos_conteo = self._analizar_formula_compleja(formula_a_analizar)
            
            self._calcular_peso()
            self._es_valido = True 
            
        except ValueError as e:
            self._establecer_error(f"Error de Formato: {e}")
        except Exception as e:
            self._establecer_error(f"Error Inesperado en el cálculo: {e}")