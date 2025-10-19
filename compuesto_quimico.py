import re
from datos_quimicos import obtener_peso_atomico, es_simbolo_valido

class CompuestoQuimico:
    """
    Representa un compuesto químico. Encapsula su fórmula y PM.
    Utiliza el método Stack para analizar fórmulas con agrupadores (paréntesis/corchetes).
    """

    def __init__(self, formula_str: str):
        """
        Constructor. Inicializa el objeto y realiza el análisis y cálculo del PM.
        """
        # --- 1. Atributos Privados (Encapsulación) ---
        self._formula_original = formula_str.strip()
        self._elementos_conteo = {} 
        self._peso_molecular = 0.0
        self._es_valido = False 
        self._mensaje_error = ""
        
        # --- 2. Ejecutar Lógica Central ---
        self._analizar_y_calcular()

    
    ## GETTERS (Acceso Controlado) ##
    

    def get_formula(self) -> str:
        """ Getter para obtener la fórmula original ingresada. """
        return self._formula_original

    def get_peso_molecular(self) -> float:
        """ Getter para obtener el peso molecular calculado. """
        return self._peso_molecular

    def es_valido(self) -> bool:
        """ Getter para verificar si el análisis de la fórmula fue exitoso. """
        return self._es_valido

    def get_mensaje_error(self) -> str:
        """ Getter para obtener el mensaje de error si la fórmula es inválida. """
        return self._mensaje_error
        
    def get_elementos_conteo(self) -> dict:
        """ Getter para obtener el diccionario de conteo de elementos. """
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
        Requiere capitalización estricta (IUPAC).
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
                # El subíndice pertenece al grupo. Acumulamos el nuevo factor.
                factor_actual *= ultimo_subindice
                multiplicadores_stack.append(factor_actual)
                ultimo_subindice = 1 
            
            # Caso 3: Paréntesis/Corchete de APERTURA (en la fórmula original: (, [)
            elif token in ['(', '[']:
                # Salimos del grupo. Deshacemos la multiplicación del grupo.
                if len(multiplicadores_stack) > 1:
                    multiplicadores_stack.pop()
                    factor_actual = multiplicadores_stack[-1]
                    ultimo_subindice = 1
                else:

                    raise ValueError(f"Agrupador de apertura ('{token}') encontrado sin su cierre correspondiente o sin subíndice inicial.")

            # Caso 4: Símbolo Químico (Elemento)
            elif token.isalpha():
                simbolo = token
                
                # --- VALIDACIÓN DE AMBIGÜEDAD/CAPITALIZACIÓN (Ej. CU vs Cu) ---
                if len(simbolo) == 2 and simbolo.isupper():
                    simbolo_capitalizado = simbolo.capitalize()
                    if es_simbolo_valido(simbolo_capitalizado):
                        # Mensaje modificado
                        raise ValueError(f"Símbolo ambiguo: '{simbolo}' (dos mayúsculas). La notación IUPAC correcta es '{simbolo_capitalizado}'.")
                
                if not es_simbolo_valido(simbolo):
                    
                    raise ValueError(f"Símbolo no reconocido: '{simbolo}'. Verifique que sea un elemento químico válido.")

                # Calcular la cantidad total: Subíndice propio * Factor del Grupo
                cantidad_total = ultimo_subindice * factor_actual

                conteo[simbolo] = conteo.get(simbolo, 0) + cantidad_total
                
                ultimo_subindice = 1 # Reiniciar para el siguiente elemento/grupo

            else:
                
                raise ValueError(f"Carácter o token inválido encontrado: '{token}'. Revise la sintaxis.")

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
            formula_original = self._formula_original
            
            self._elementos_conteo = self._analizar_formula_compleja(formula_original)
            
            self._calcular_peso()
            self._es_valido = True 
            
        except ValueError as e:
            self._establecer_error(f"Error de Formato: {e}")
        except Exception as e:
            self._establecer_error(f"Error Inesperado en el cálculo: {e}")