import json
import os
from typing import Dict
from compuesto_quimico import CompuestoQuimico # Importamos la clase modelo (POO)
import datos_quimicos # Importamos datos_quimicos para asegurar que mendeleev cargue al inicio

# --- Variables Globales de Estado ---
LISTA_COMPUESTOS: Dict[str, CompuestoQuimico] = {}

# Archivo de persistencia con extensión .txt (contenido JSON)
NOMBRE_ARCHIVO_PERSISTENCIA = "compuestos.txt" 


## LÓGICA DE PERSISTENCIA ##


def _serializar_compuestos() -> Dict:
    """Convierte la lista de objetos CompuestoQuimico a un diccionario simple para JSON."""
    datos_serializados = {}
    for formula, compuesto in LISTA_COMPUESTOS.items():
        if compuesto.es_valido():
            # Claves formales para persistencia
            datos_serializados[formula] = {
                "Formula": compuesto.get_formula(),
                "Peso Molecular": compuesto.get_peso_molecular(),
                "Elementos": compuesto.get_elementos_conteo()
            }
    return datos_serializados

def guardar_compuestos():
    """Guarda cada compuesto válido en una línea separada en el archivo de persistencia."""
    print("Guardando datos...")
    datos_a_guardar = _serializar_compuestos()
    
    try:
        with open(NOMBRE_ARCHIVO_PERSISTENCIA, 'w') as f:
            for formula, data in datos_a_guardar.items():
                linea_json = json.dumps({formula: data}, separators=(",", ":"))
                f.write(linea_json + "\n")
        print("Guardado exitoso en {}".format(NOMBRE_ARCHIVO_PERSISTENCIA))
    except IOError as e:
        print("Error al guardar el archivo: {}".format(e))

def _cargar_compuestos_desde_archivo():
    """Carga los datos guardados, leyendo cada línea como un compuesto separado."""
    global LISTA_COMPUESTOS
    if not os.path.exists(NOMBRE_ARCHIVO_PERSISTENCIA):
        print("Persistencia: Archivo de datos no encontrado. Iniciando limpio.")
        return

    try:
        LISTA_COMPUESTOS = {} 
        compuestos_cargados = 0
        
        with open(NOMBRE_ARCHIVO_PERSISTENCIA, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                datos_compuesto = json.loads(line)
                formula_str = list(datos_compuesto.keys())[0]

                # Recrear objetos CompuestoQuimico
                compuesto = CompuestoQuimico(formula_str) 
                if compuesto.es_valido():
                    LISTA_COMPUESTOS[compuesto.get_formula()] = compuesto 
                    compuestos_cargados += 1
                else:
                    print("Advertencia: '{}' fue inválida al cargar y omitida.".format(formula_str))
        
        print("Persistencia: Carga completa. {} compuestos cargados.".format(compuestos_cargados))
        
    except (IOError, json.JSONDecodeError) as e:
        print("Error al cargar o decodificar el archivo de persistencia: {}".format(e))
        LISTA_COMPUESTOS = {}


## FUNCIONES DE INICIO Y ESTADO ##


def cargar_datos_iniciales():
    """
    Función que el main.py llama para inicializar el programa.
    Asegura la carga de datos atómicos (mendeleev) y la persistencia.
    """
    _cargar_compuestos_desde_archivo()

def obtener_compuestos_cargados() -> Dict[str, CompuestoQuimico]:
    """ Devuelve el diccionario de compuestos cargados. """
    return LISTA_COMPUESTOS


## FUNCIONES DEL MENÚ (LÓGICA DEL FLUJO) ##


def _pedir_formula_y_crear_compuesto():
    """
    Solicita la fórmula, crea el objeto CompuestoQuimico, y notifica si ya existía.
    Llamada directamente por main.py (Opción 1).
    """
    
    print("\nADVERTENCIA: La capitalización debe ser ESTRICTA (IUPAC).")
    print("Ingrese el compuesto respetando mayúsculas y minúsculas (Ej: CO2 y no Co2/co2/cO2).")
    formula_input = input("Ingresa la fórmula química: ").strip()
    
    if not formula_input:
        print("Error: La fórmula no puede estar vacía.")
        return

    compuesto = CompuestoQuimico(formula_input)
    
    if compuesto.es_valido():
        formula_clave = compuesto.get_formula() 
        
        mensaje_impreso = False 
        
        # --- VERIFICACIÓN DE EXISTENCIA ---
        if formula_clave in LISTA_COMPUESTOS:
            existente = LISTA_COMPUESTOS[formula_clave]
            print("\nEl compuesto '{}' ya estaba guardado.".format(formula_clave))
            print("   PM: {:.3f} g/mol".format(existente.get_peso_molecular())) 
            mensaje_impreso = True
        # ------------------------------------

        LISTA_COMPUESTOS[formula_clave] = compuesto 
        
        if not mensaje_impreso:
            print("\nCálculo exitoso para '{}'.".format(formula_clave))
            print("   Peso Molecular Actual: {:.3f} g/mol".format(compuesto.get_peso_molecular()))
    else:
        print("\nError al procesar '{}': {}".format(compuesto.get_formula(), compuesto.get_mensaje_error()))
        
    
def _opcion_mostrar_compuestos():
    """Muestra un resumen de los compuestos que están actualmente guardados en memoria.
    Llamada directamente por main.py (Opción 2).
    """
    if not LISTA_COMPUESTOS:
        print("\nNo hay compuestos válidos cargados actualmente.")
        return

    print("\n--- Compuestos Válidos Guardados ---")
    for formula, compuesto in LISTA_COMPUESTOS.items():
        print(" > {} | PM: {:.3f} g/mol | Elementos: {}".format(
            formula.ljust(15), 
            compuesto.get_peso_molecular(), 
            list(compuesto.get_elementos_conteo().keys()))
        )
    print("-" * 35)