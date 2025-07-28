
from funciones import calcular_peso_molecular, normalizar_formula_quimica

if __name__=="__main__":

    print("\n----------- MENÚ PRINCIPAL CALCULADORA de PESO MOLECULAR ------------")
    print("Escribe 'salir' en cualquier momento para terminar el programa.")
        
    while True:
        
        formula_input = input("\nIngrese la formula química del compuesto: ").strip()

        if formula_input.lower() == "salir":
            print("\n¡Gracias por usar la calculadora! Hasta luego.")
            break

        if not formula_input:
            print("Error: La fórmula no puede estar vacía.")
            continue
        
        peso_mol = calcular_peso_molecular(formula_input)
        
        if peso_mol is not None:
            print(f"El Peso Molecular de {normalizar_formula_quimica(formula_input)} es: {peso_mol:.3f} g/mol")
        