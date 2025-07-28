
from mendeleev import get_all_elements
# get_all_elements(), es una función de mendeleev, que nos entrega una lista de objetos, 
# la cual contiene todas las propiedades asociadas a cada elemento químico de la tabla periódica.

"""
Creación del conjunto o set de símbolos de los elementos desde mendeleev.
Esto se hace una sola vez al iniciar el programa y es necesario para
optimzar el rendimiento, lo que permite validar rápidamente los
símboles de elementos ingresados por el usuario.
"""
# VARIABLES GLOBALES DATOS ELEMENTOS QUÍMICOS

print("\ndata.py: Cargando base de datos de símbolos de elementos químicos para validación inicial, espere un momento...")

validador_simbolos_elementos = set() # Creación conjunto o set vacío para almacenar los símbolos de los elementos químicos.

lista_de_objetos_elementos = get_all_elements() # Se crea esta lista de objetos que contiene todas las propiedades de cada elemento químico.

for objeto_elemento_individual in lista_de_objetos_elementos: # Obtención y adición de los símbolos de los elementos en el set.
    simbolo_del_elemento = objeto_elemento_individual.symbol
    validador_simbolos_elementos.add(simbolo_del_elemento)

print(f"\ndata.py: Cargados {len(validador_simbolos_elementos)} símbolos de elementos químicos válidos.")

