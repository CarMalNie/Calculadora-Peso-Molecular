
import re
from mendeleev import element
import data


"""
Normaliza una cadena de fórmula química ingresada por el usuario.
    
    1. Elimina caracteres no alfanuméricos al inicio/final.
    2. Asegura el uso correcto de mayúsculas/minúsculas para los símbolos de elementos.
    
    Ej: "-hcl" -> "HCl", "+C6h12o6" -> "C6H12O6", ",hcl" -> "HCl".
"""
def normalizar_formula_quimica(formula_str):

    if not formula_str:
        return ""
    
    # Paso 1: Limpiar la cadena de caracteres no deseados al inicio y final,
    # y también cualquier espacio extra en medio. Esto es una limpieza básica.
    # Usaremos un regex para esto para ser robustos.
    # Solo permitimos letras, números y paréntesis (aunque aún no los procesamos).
    # Reemplazamos cualquier cosa que NO sea letra o número o paréntesis con un espacio (o nada)
    # y luego limpiamos esos espacios.
    
    # Nuevo: Permitir solo caracteres de fórmula válidos (letras, números).
    # Esto elimina -, +, ,, . etc.
    
    limpia = re.sub(r'[^A-Za-z0-9]', '', formula_str) # Elimina todo lo que NO sea letra o número
    
    if not limpia: # Si después de limpiar queda vacío
        return ""
    
    normalizada = ""
    i = 0
    while i < len(limpia): # Iteramos sobre la cadena limpia
        char = limpia[i]
        
        if char.isalpha(): # Si es una letra
            # Intentar formar un candidato de dos letras (ej. 'Na', 'Cl')
            candidate_two_char_capitalized = ""
            if i + 1 < len(limpia) and limpia[i+1].isalpha():
                candidate_two_char_capitalized = (limpia[i] + limpia[i+1]).capitalize()
            
            # 1. Priorizamos símbolos de DOS letras válidos
            if candidate_two_char_capitalized and candidate_two_char_capitalized in data.validador_simbolos_elementos:
                normalizada += candidate_two_char_capitalized # Añadir el símbolo de 2 letras normalizado
                i += 2 
                continue 
            
            # 2. Si no fue un símbolo de 2 letras válido, entonces es uno de UNA letra.
            normalizada += char.upper() 
            i += 1
        else: # Si no es una letra (es un número)
            normalizada += char
            i += 1
            
    return normalizada


"""
Calcula el peso molecular de un compuesto que tenga
una fórmula simple (sin paréntesis).
Por ejemplo: "H2O" o "C6H12O6"
"""
def calcular_peso_molecular(formula):
    
    formula_normalizada = normalizar_formula_quimica(formula)

    elementos_conteo = {} # Diccionario para guardar {'Símbolo': Cantidad_Total}

# Patrón de expresión regular para analizar la fórmula química.
# r'': Indica una "raw string" para tratar las barras invertidas literalmente.
# 
# Componentes del patrón:
# 1. ([A-Z][a-z]*)  Primer grupo de captura: Identifica el SÍMBOLO del elemento.
#       - [A-Z] : Coincide con una letra mayúscula (inicio del símbolo, ej. 'H', 'C').
#       - [a-z]*: Coincide con cero o más letras minúsculas (para símbolos de dos letras, ej. 'Cl', 'Na'; o nada si es de una letra).
# 
# 2. (\d*)  Segundo grupo de captura: Identifica el SUBÍNDICE (cantidad de átomos).
#       - \d: Coincide con cualquier dígito (0-9).
#       - *:  Coincide con cero o más dígitos (permite subíndices como '2' o vacío si es '1').
# 
# re.findall() devuelve una lista de tuplas, donde cada tupla es (símbolo, subíndice_str).
# Ejemplo para "H2O": [('H', '2'), ('O', '')]

    patron_elemento = r'([A-Z][a-z]*)(\d*)'
    partes_formula = re.findall(patron_elemento, formula_normalizada)

    if not partes_formula:
        print(f"Error no se pudieron identificar elementos en la fórmula '{formula_normalizada}'.")
        return None

    for simbolo, subindice_str in partes_formula:
        if subindice_str:
            cantidad = int(subindice_str)
        else:
            cantidad = 1

        if simbolo in data.validador_simbolos_elementos:
            elementos_conteo[simbolo] = elementos_conteo.get(simbolo, 0) + cantidad
        else:
            print(f"Error el símbolo '{simbolo}' no es un elemento químico válido.")
            return None

    peso_molecular_total = 0.0
    for simbolo, cantidad in elementos_conteo.items():
        peso_atomico = element(simbolo).atomic_weight
        peso_molecular_total += peso_atomico * cantidad
        
    return peso_molecular_total