from funciones import (
    cargar_datos_iniciales, 
    obtener_compuestos_cargados,
    _pedir_formula_y_crear_compuesto,
    _opcion_mostrar_compuestos,
    guardar_compuestos
)
from typing import Dict
from compuesto_quimico import CompuestoQuimico

# --- FUNCIÓN DE INTERFAZ ---
def mostrar_menu_principal(compuestos: Dict[str, CompuestoQuimico]):
    """ Muestra el menú en la terminal. """
    print("\n" + "="*45)
    print("--- CALCULADORA QUÍMICA ---")
    
    if compuestos:
        ultima_formula = list(compuestos.keys())[-1]
        print("Compuestos Cargados: {} - Último: {}".format(len(compuestos), ultima_formula))
    else:
        print("Compuestos Cargados: 0 - Usa la Opción 1 para calcular y agregar un nuevo compuesto.")
        
    print("---------------------------------------------")
    print("1. Calcular PM del Compuesto") 
    print("2. Mostrar Compuestos Guardados")
    print("3. Guardar")            
    print("4. Guardar y Salir")    
    print("="*45)


def main():
    """
    Función principal que ejecuta el ciclo de vida de la calculadora.
    """
    cargar_datos_iniciales()
    
    while True:
        # Mostrar el estado actual y el menú
        compuestos_actuales = obtener_compuestos_cargados()
        mostrar_menu_principal(compuestos_actuales) 
        
        opcion = input("Selecciona una opción (1-4): ").strip()
        
        # Lógica 'match/case' directa en main
        match opcion:
            case '1':
                _pedir_formula_y_crear_compuesto()
            case '2':
                _opcion_mostrar_compuestos()
            case '3':
                guardar_compuestos()
            case '4':
                guardar_compuestos() 
                print("\n¡Gracias por usar la calculadora!")
                break # Salir del bucle
            case _:
                print("Opción inválida. Por favor, selecciona un número entre 1 y 4.")
        
        if opcion in ['1', '2', '3']:
            input("\nPresiona Enter para volver al Menú Principal...")

if __name__ == "__main__":
    main()