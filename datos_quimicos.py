from mendeleev import get_all_elements, element
import sys

# --- Variables Globales del Módulo ---
# Contendrá un conjunto de todos los símbolos válidos para una validación rápida.
VALIDADOR_SIMBOLOS = set()

# Contendrá un diccionario mapeando símbolo a peso atómico para un acceso rápido.
PESOS_ATOMICOS = {}


def cargar_datos_mendeleev():
    """
    Carga todos los datos de elementos químicos (símbolos y pesos atómicos)
    desde la librería mendeleev al iniciar el programa.
    """
    global VALIDADOR_SIMBOLOS, PESOS_ATOMICOS
    
    # Si los datos ya están cargados, salimos para evitar recargas.
    if VALIDADOR_SIMBOLOS:
        return
        
    print("Datos Químicos: Cargando base de datos de elementos...")
    
    try:
        lista_elementos = get_all_elements()
        
        for el in lista_elementos:
            simbolo = el.symbol
            peso = el.atomic_weight
            
            # 1. Almacenar el símbolo para validación
            VALIDADOR_SIMBOLOS.add(simbolo)
            
            # 2. Almacenar el peso atómico para cálculos
            PESOS_ATOMICOS[simbolo] = peso
            
        print(f"Datos Químicos: Cargados {len(VALIDADOR_SIMBOLOS)} elementos y sus pesos.")
        
    except Exception as e:
        # Manejo de error si la librería falla o no puede obtener datos
        print(f"Error fatal al cargar mendeleev: {e}")
        print("Asegúrate de que la librería 'mendeleev' esté instalada correctamente.")
        # Salimos del programa si la base de datos no se puede cargar
        sys.exit(1)


def es_simbolo_valido(simbolo: str) -> bool:
    """ Verifica si un símbolo es un elemento químico real. """
    return simbolo in VALIDADOR_SIMBOLOS


def obtener_peso_atomico(simbolo: str) -> float:
    """ Obtiene el peso atómico de un elemento. Retorna 0.0 si no es válido. """
    return PESOS_ATOMICOS.get(simbolo, 0.0)

# Al importar este módulo, la función de carga se ejecutará automáticamente.
cargar_datos_mendeleev()