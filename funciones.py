import json
import os
from typing import Dict
from compuesto_quimico import CompuestoQuimico
import datos_quimicos

# --- Variables Globales de Estado ---
LISTA_COMPUESTOS: Dict[str, CompuestoQuimico] = {}

# Archivo de persistencia con extensión .txt (contenido JSON)
NOMBRE_ARCHIVO_PERSISTENCIA = "compuestos.txt" 


## LÓGICA DE PERSISTENCIA ##

def _serializar_compuestos() -> Dict:
    """Convierte la lista de objetos CompuestoQuimico a un diccionario indexado (1, 2, 3...) para JSON."""
    datos_serializados = {}
    index = 1  # Iniciar el contador de índice
    for formula, compuesto in LISTA_COMPUESTOS.items():
        if compuesto.es_valido:
            # Claves formales para persistencia
            datos_serializados[str(index)] = {
                "Formula": compuesto.formula,
                "Peso Molecular": compuesto.peso_molecular,
                "Elementos": compuesto.elementos_conteo
            }
            index += 1
    return datos_serializados

def guardar_compuestos():
    """Guarda cada compuesto válido en una línea separada en el archivo de persistencia."""
    print("Guardando datos...")
    datos_a_guardar = _serializar_compuestos()
    
    try:
        with open(NOMBRE_ARCHIVO_PERSISTENCIA, 'w') as f:
            for formula, data in datos_a_guardar.items():
                # Escribimos el par CLAVE-VALOR (ej: "1": {data}) en una línea JSON.
                linea_json = json.dumps({formula: data}, separators=(",", ":"))
                f.write(linea_json + "\n")
        print("Guardado exitoso en {}".format(NOMBRE_ARCHIVO_PERSISTENCIA))
    except IOError as e:
        print("Error al guardar el archivo: {}".format(e))

def _cargar_compuestos_desde_archivo():
    """Carga los datos guardados, leyendo cada línea y extrayendo la fórmula del diccionario interno."""
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
                
                # Obtener el índice numérico (ej: "1") y el diccionario de datos internos
                indice_clave = list(datos_compuesto.keys())[0]
                datos_internos = datos_compuesto[indice_clave] 
                
                # Obtenemos la fórmula del diccionario interno
                formula_str = datos_internos["Formula"] 

                # Recrear objetos CompuestoQuimico (la asignación del constructor dispara la validación)
                compuesto = CompuestoQuimico(formula_str) 
                
                if compuesto.es_valido:
                    # Usamos la fórmula como clave para la lista en memoria
                    LISTA_COMPUESTOS[compuesto.formula] = compuesto 
                    compuestos_cargados += 1
                else:
                    print("Advertencia: '{}' fue inválida al cargar y omitida.".format(compuesto.formula))
        
        print("Persistencia: Carga completa. {} compuestos cargados.".format(compuestos_cargados))
        
    except (IOError, json.JSONDecodeError) as e:
        print("Error al cargar o decodificar el archivo de persistencia: {}".format(e))
        LISTA_COMPUESTOS = {}


## FUNCIONES DE INICIO Y ESTADO ##

def cargar_datos_iniciales():
    """
    Función que el main.py llama para inicializar el programa.
    """
    _cargar_compuestos_desde_archivo()

def obtener_compuestos_cargados() -> Dict[str, CompuestoQuimico]:
    """ Devuelve el diccionario de compuestos cargados. """
    return LISTA_COMPUESTOS


## FUNCIONES DEL MENÚ (LÓGICA DEL FLUJO) ##

def _pedir_formula_y_crear_compuesto():
    """
    Solicita la fórmula, crea el objeto CompuestoQuimico, y notifica si ya existía.
    """
    
    print("\nADVERTENCIA: La **nomenclatura del compuesto químico** debe ser ESTRICTA (IUPAC).")
    print("   Ingrese el compuesto respetando mayúsculas y minúsculas (Ej: CO2 y no Co2/co2/cO2).")
    formula_input = input("Ingresa la fórmula: ").strip() 
    
    if not formula_input:
        print("Error: La fórmula no puede estar vacía.")
        return

    # La creación llama al setter, validando la entrada.
    compuesto = CompuestoQuimico(formula_input)
    
    # Uso de .es_valido (propiedad)
    if compuesto.es_valido:
        formula_clave = compuesto.formula # Uso de .formula (propiedad)
        
        mensaje_impreso = False 
        
        # --- VERIFICACIÓN DE EXISTENCIA ---
        if formula_clave in LISTA_COMPUESTOS:
            existente = LISTA_COMPUESTOS[formula_clave]
            print("\nEl compuesto '{}' ya estaba guardado.".format(formula_clave))
            # Uso de .peso_molecular (propiedad)
            print("   PM: {:.3f} g/mol".format(existente.peso_molecular)) 
            mensaje_impreso = True
        # ------------------------------------

        LISTA_COMPUESTOS[formula_clave] = compuesto 
        
        if not mensaje_impreso:
            print("\nCálculo exitoso para '{}'.".format(formula_clave))
            # Uso de .peso_molecular (propiedad)
            print("   Peso Molecular Actual: {:.3f} g/mol".format(compuesto.peso_molecular))
    else:
        # Uso de .formula y .mensaje_error (propiedades)
        print("Error en fórmula '{}': {}".format(compuesto.formula, compuesto.mensaje_error))
        
    
def _opcion_mostrar_compuestos():
    """Muestra un resumen de los compuestos que están actualmente guardados en memoria."""
    if not LISTA_COMPUESTOS:
        print("\nNo hay compuestos válidos cargados actualmente.")
        return

    print("\n--- Compuestos Válidos Guardados ---")
    for formula, compuesto in LISTA_COMPUESTOS.items():
        # Llama a la representación __str__ del objeto
        print(" > {}".format(str(compuesto)))
    print("-" * 35)

def _opcion_eliminar_compuesto():
    """
    Solicita la fórmula de un compuesto guardado y lo elimina de LISTA_COMPUESTOS.
    """
    if not LISTA_COMPUESTOS:
        print("\nNo hay compuestos guardados para eliminar.")
        return

    print("\n--- Eliminar Compuesto Guardado ---")
    
    # Muestra una lista de fórmulas existentes para ayudar al usuario
    formulas_existentes = ", ".join(LISTA_COMPUESTOS.keys())
    print(f"Fórmulas guardadas: {formulas_existentes}")

    formula_a_eliminar = input("Ingrese la fórmula IUPAC del compuesto a eliminar: ").strip()

    if not formula_a_eliminar:
        print("Error: La fórmula no puede estar vacía.")
        return

    # La fórmula es la clave del diccionario en memoria
    if formula_a_eliminar in LISTA_COMPUESTOS:
        del LISTA_COMPUESTOS[formula_a_eliminar]
        print(f"\nCompuesto '{formula_a_eliminar}' eliminado exitosamente de la memoria.")
        print("Recuerde seleccionar la opción 'Guardar' o 'Guardar y Salir' para aplicar el cambio al archivo de persistencia.")
    else:
        print(f"\nError: El compuesto '{formula_a_eliminar}' no se encontró en los datos guardados. Intente con la capitalización correcta.")