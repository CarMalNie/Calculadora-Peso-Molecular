-----

# Calculadora de Peso Molecular (Fase 1: Fórmulas Simples)

Este **trabajo personal** es el primer avance de una Calculadora de Peso Molecular más completa. En su estado actual, es capaz de determinar el peso molecular de compuestos químicos cuyas fórmulas **no contienen paréntesis** (ej., `H2O`, `NaCl`, `C6H12O6`). Su diseño modular sienta las bases para futuras expansiones, como el manejo de paréntesis anidados y otras funcionalidades químicas.

-----

## Características Clave (Fase 1)

  - **Cálculo de Peso Molecular:** Calcula el peso molecular de cualquier compuesto con una fórmula simple.
  - **Validación de Elementos:** Utiliza una base de datos externa (`mendeleev`) para validar si los símbolos químicos ingresados son reales.
  - **Manejo de Entrada Robusto:** Es tolerante a variaciones en el uso de mayúsculas/minúsculas en los símbolos de los elementos (ej., `h2o` o `NACL` son aceptados y corregidos internamente a `H2O` y `NaCl`), y elimina caracteres no deseados.
  - **Interfaz Simple:** Ofrece una interfaz de línea de comandos sencilla y directa.

-----

## Fundamentos de Python en Este Trabajo

Este trabajo personal no es solo una calculadora de peso molecular; es también una demostración práctica de varios **conceptos fundamentales de la programación en Python**. Hemos implementado intencionalmente estos pilares para crear una aplicación robusta y bien estructurada.

### Variables, Operadores y Tipos de Datos

  - **Variables**: Las usamos ampliamente para almacenar información. Por ejemplo, `formula_input` guarda la fórmula química del usuario, `peso_mol` el peso molecular calculado, `simbolo_del_elemento` el símbolo de un elemento, y `cantidad` la cuenta de átomos de un elemento.
  - **Operadores**: Los operadores **aritméticos** (`+` para suma, `*` para multiplicación) son cruciales para calcular el `peso_molecular_total`. Los operadores de **comparación** (`==`, `!=`) y **lógicos** (`and`, `or`, `not`) se utilizan en validaciones y para controlar el flujo del programa.
  - **Tipos de Datos**:
      - **Cadenas de caracteres (`str`)**: Fundamentales para las fórmulas químicas (ej., "H2O", "NaCl"), los símbolos de elementos (ej., "H", "Cu"), y toda la entrada y salida de texto del usuario.
      - **Enteros (`int`)**: Se usan para las cantidades de átomos (subíndices como '2' en H2O) y los contadores en los bucles.
      - **Flotantes (`float`)**: Esenciales para almacenar y calcular los pesos moleculares y atómicos (ej., 1.008 g/mol, 74.092 g/mol), que suelen tener decimales.
      - **Booleanos (`bool`)**: Utilizados en las condiciones (`if not formula_str`, `if char.isalpha()`) para tomar decisiones y controlar el flujo del programa basándose en si una condición es verdadera o falsa.

### Estructuras de Control de Flujo

  - **Condicionales (`if`, `elif`, `else`)**: Estas estructuras son la base para la toma de decisiones en el programa.
      - Utilizamos `if not formula_str:` para verificar si una entrada está vacía.
      - `if simbolo in data.validador_simbolos_elementos:` valida los símbolos de los elementos contra nuestra base de datos.
      - La lógica `if/else` dentro de `normalizar_formula_quimica` ajusta inteligentemente el tipo de carácter y el uso de mayúsculas/minúsculas de los símbolos de elementos.
  - **Bucles (`for`, `while`)**: Empleados para repetir acciones de manera eficiente.
      - Un bucle **`while True`** en `calculadora_peso_molecular.py` mantiene el programa en ejecución continua, solicitando nuevas fórmulas hasta que el usuario decida salir.
      - Los bucles **`for`** se utilizan para iterar sobre colecciones, como `for objeto_elemento_individual in lista_de_objetos_elementos:` en `data.py` para construir el conjunto de símbolos válidos, y `for simbolo, subindice_str in partes_formula:` en `calcular_peso_molecular` para procesar cada par de elemento-cantidad.
      - También se emplean bucles **`while`** (`while i < len(limpia):`) en `normalizar_formula_quimica` y `while i < len(sub_formula_str):` en `_obtener_conteo_de_elementos_en_formula` para procesar las cadenas de fórmulas carácter por carácter.

### Estructuras de Datos para Organización

  - **Conjuntos (`set`)**: El `validador_simbolos_elementos` en `data.py` es un **`set`**. Elegimos esta estructura específicamente por su **alta eficiencia al verificar la existencia de elementos** (`if simbolo in validador_simbolos_elementos:`), lo que garantiza una validación rápida de los símbolos de elementos. Los conjuntos también aseguran automáticamente la unicidad de sus elementos, ideal para una lista de símbolos químicos distintos.
  - **Diccionarios (`dict`)**: El diccionario `elementos_conteo` en `calcular_peso_molecular` es crucial para **organizar y acumular el conteo** de cada elemento encontrado en la fórmula química (ej., `{'H': 2, 'O': 1}`). Los diccionarios almacenan datos como pares clave-valor, permitiendo búsquedas y actualizaciones rápidas de las cantidades de elementos.
  - **Listas (`list`)**: La `lista_de_objetos_elementos` (obtenida de `mendeleev`) es una lista de objetos que representan elementos. Las listas también se utilizan para almacenar secuencias de partes de fórmulas analizadas (ej., `partes_formula` de `re.findall()`) y `normalized_tokens` en `normalizar_formula_quimica` para construir la fórmula normalizada.

### Modularización del Código

Hemos **modularizado el código** en tres archivos (`data.py`, `funciones.py`, `calculadora_peso_molecular.py`) para **reutilizar la lógica** y mejorar la organización general.

  - `data.py` se encarga de la gestión de los **datos globales**.
  - `funciones.py` contiene todas las **funciones lógicas** (`calcular_peso_molecular`, `normalizar_formula_quimica`, `_obtener_conteo_de_elementos_en_formula`).
  - `calculadora_peso_molecular.py` actúa como el **punto de entrada principal** del programa, orquestando la interacción con el usuario y llamando a las funciones necesarias.

Esta separación de responsabilidades hace que el código sea más legible, fácil de mantener y de escalar para futuras funcionalidades.

-----

## Estructura del Trabajo

```
.
├── data.py
├── funciones.py
└── calculadora_peso_molecular.py
```

### `data.py`

Este archivo actúa como el **cerebro de datos** del trabajo. Su principal responsabilidad es:

  - **Cargar la base de datos de elementos:** Al iniciar, se conecta con la librería `mendeleev` para obtener un listado completo y actualizado de todos los elementos de la tabla periódica.
  - **Crear el validador de símbolos:** Genera un `set` (conjunto) llamado `validador_simbolos_elementos`. Este `set` contiene todos los símbolos químicos válidos (ej., "H", "O", "Na"). Un `set` es extremadamente eficiente para verificar rápidamente si un símbolo ingresado por el usuario es un elemento químico real.

**Conexión:** `funciones.py` importa `data` para acceder a `validador_simbolos_elementos`.

### `funciones.py`

Aquí reside toda la **lógica central** de la calculadora. Contiene las funciones que realizan los cálculos y el pre-procesamiento de las fórmulas:

  - **`normalizar_formula_quimica(formula_str)`:** Esta es una función crucial. Toma la fórmula ingresada por el usuario (ej., "h2o", "NACL", "-Fe") y la limpia y formatea.
      - Elimina caracteres no alfanuméricos (excepto paréntesis, para futuras fases).
      - Asegura que los símbolos de los elementos tengan el uso correcto de mayúsculas y minúsculas (ej. "na" se convierte a "Na", "cl" a "Cl"), resolviendo posibles ambigüedades como "NH" vs "Nh" de forma inteligente.
  - **`_obtener_conteo_de_elementos_en_formula(sub_formula_str)`:** Esta es una función auxiliar (marcada con `_` al inicio para indicar uso interno). Su tarea es recorrer una parte de la fórmula (o la fórmula completa) e identificar cada elemento y la cantidad de veces que aparece.
      - Utiliza **expresiones regulares (`re.match`)** para identificar patrones de símbolos (ej. "H", "O", "Na") y sus subíndices (ej. "2", "3").
      - Acumula el conteo de cada elemento en un diccionario (ej. `{'H': 2, 'O': 1}`).
      - En esta fase, solo maneja fórmulas sin paréntesis.
  - **`calcular_peso_molecular(formula)`:** Esta es la función principal de cálculo.
      - Recibe la fórmula cruda del usuario.
      - Primero, llama a `normalizar_formula_quimica` para limpiar y formatear la entrada.
      - Luego, utiliza `_obtener_conteo_de_elementos_en_formula` para obtener el conteo de cada elemento.
      - Finalmente, usa la librería `mendeleev` para obtener los pesos atómicos de cada elemento y suma el total para calcular el peso molecular.

**Conexión:** `calculadora_peso_molecular.py` importa funciones específicas de `funciones.py` para realizar las operaciones.

### `calculadora_peso_molecular.py`

Este es el **archivo principal** del trabajo, el que el usuario ejecuta. Su responsabilidad es gestionar la interfaz de usuario:

  - Muestra el mensaje de bienvenida y las instrucciones.
  - Contiene un bucle principal que continuamente solicita al usuario una fórmula química.
  - Valida la entrada básica (no vacía, opción de salir).
  - Llama a `calcular_peso_molecular` (desde `funciones.py`) con la fórmula ingresada.
  - Muestra el peso molecular calculado o un mensaje de error si la fórmula es inválida o no se pudo procesar.

**Conexión:** Este archivo orquesta la interacción y llama a la lógica definida en `funciones.py`.

-----

## Cómo Ejecutar el Código

1.  **Instala Python:** Asegúrate de tener Python 3.8 o superior instalado en tu sistema.
2.  **Instala la librería `mendeleev`:**
    Abre tu terminal o línea de comandos y ejecuta:
    ```bash
    pip install mendeleev
    ```
3.  **Descarga los archivos:** Clona este repositorio o descarga los archivos `data.py`, `funciones.py`, y `calculadora_peso_molecular.py` en la misma carpeta.
4.  **Ejecuta el programa:**
    Abre tu terminal, navega hasta la carpeta donde guardaste los archivos y ejecuta:
    ```bash
    python calculadora_peso_molecular.py
    ```

El programa te pedirá que ingreses una fórmula química (ej., `H2O`, `NaCl`, `C6H12O6`). Puedes escribir `salir` para terminar.

-----

## Próximos Pasos (Fases Futuras)

Esta calculadora es una base sólida para tu trabajo personal. Los próximos pasos en su desarrollo incluyen:

  - **Manejo de Paréntesis:** Extender la lógica de `_obtener_conteo_de_elementos_en_formula` para procesar grupos con paréntesis (ej., `Ca(OH)2`).
  - **Manejo de Paréntesis Anidados:** Ampliar el soporte para fórmulas con múltiples niveles de paréntesis (ej., `K4[Fe(CN)6]`).
  - **Cálculo de Moles:** Reintroducir la funcionalidad para convertir masa a moles (g, kg, t).
  - **Interfaz Gráfica (Opcional):** Desarrollar una interfaz de usuario más amigable que la línea de comandos.

-----
