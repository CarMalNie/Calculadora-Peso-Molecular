Calculadora de Peso Molecular (Fase 1: Fórmulas Simples)

Este trabajo personal es el primer avance de una Calculadora de Peso Molecular más completa. En su estado actual, es capaz de determinar el peso molecular de compuestos químicos cuyas fórmulas no contienen paréntesis (ej., H2O, NaCl, C6H12O6). Su diseño modular sienta las bases para futuras expansiones, como el manejo de paréntesis anidados y otras funcionalidades químicas.

Características Clave (Fase 1)

    Cálculo de Peso Molecular: Calcula el peso molecular de cualquier compuesto con una fórmula simple.

    Validación de Elementos: Utiliza una base de datos externa (mendeleev) para validar si los símbolos químicos ingresados son reales.

    Manejo de Entrada: Es robusto ante variaciones en el uso de mayúsculas/minúsculas en los símbolos de los elementos (ej., h2o o NACL son aceptados y corregidos internamente a H2O y NaCl).

    Interfaz Simple: Ofrece una interfaz de línea de comandos sencilla y directa.

Estructura del Trabajo

El código está organizado en tres archivos principales para promover la modularidad y la claridad:

.
├── data.py
├── funciones.py
└── calculadora_peso_molecular.py

data.py

Este archivo actúa como el cerebro de datos del trabajo. Su principal responsabilidad es:

    Cargar la base de datos de elementos: Al iniciar, se conecta con la librería mendeleev para obtener un listado completo y actualizado de todos los elementos de la tabla periódica.

    Crear el validador de símbolos: Genera un set (conjunto) llamado validador_simbolos_elementos. Este set contiene todos los símbolos químicos válidos (ej., "H", "O", "Na"). Un set es extremadamente eficiente para verificar rápidamente si un símbolo ingresado por el usuario es un elemento químico real.

Conexión: funciones.py importa data para acceder a validador_simbolos_elementos.

funciones.py

Aquí reside toda la lógica central de la calculadora. Contiene las funciones que realizan los cálculos y el pre-procesamiento de las fórmulas:

    normalizar_formula_quimica(formula_str): Esta es una función crucial. Toma la fórmula ingresada por el usuario (ej., "h2o", "NACL", "-Fe") y la limpia y formatea.

        Elimina caracteres no alfanuméricos (excepto paréntesis, para futuras fases).

        Asegura que los símbolos de los elementos tengan el uso correcto de mayúsculas y minúsculas (ej. "na" se convierte a "Na", "cl" a "Cl"), resolviendo posibles ambigüedades como "NH" vs "Nh" de forma inteligente.

    _obtener_conteo_de_elementos_en_formula(sub_formula_str): Esta es una función auxiliar (marcada con _ al inicio para indicar uso interno). Su tarea es recorrer una parte de la fórmula (o la fórmula completa) e identificar cada elemento y la cantidad de veces que aparece.

        Utiliza expresiones regulares (re.match) para identificar patrones de símbolos (ej. "H", "O", "Na") y sus subíndices (ej. "2", "3").

        Acumula el conteo de cada elemento en un diccionario (ej. {'H': 2, 'O': 1}).

        En esta fase, solo maneja fórmulas sin paréntesis.

    calcular_peso_molecular(formula): Esta es la función principal de cálculo.

        Recibe la fórmula cruda del usuario.

        Primero, llama a normalizar_formula_quimica para limpiar y formatear la entrada.

        Luego, utiliza _obtener_conteo_de_elementos_en_formula para obtener el conteo de cada elemento.

        Finalmente, usa la librería mendeleev para obtener los pesos atómicos de cada elemento y suma el total para calcular el peso molecular.

Conexión: calculadora_peso_molecular.py importa funciones específicas de funciones.py para realizar las operaciones.

calculadora_peso_molecular.py

Este es el archivo principal del trabajo, el que el usuario ejecuta. Su responsabilidad es gestionar la interfaz de usuario:

    Muestra el mensaje de bienvenida y las instrucciones.

    Contiene un bucle principal que continuamente solicita al usuario una fórmula química.

    Valida la entrada básica (no vacía, opción de salir).

    Llama a calcular_peso_molecular (desde funciones.py) con la fórmula ingresada.

    Muestra el peso molecular calculado o un mensaje de error si la fórmula es inválida o no se pudo procesar.

Conexión: Este archivo orquesta la interacción y llama a la lógica definida en funciones.py.

Cómo Ejecutar el Código

    Instala Python: Asegúrate de tener Python 3.8 o superior instalado en tu sistema.

    Instala la librería mendeleev:
    Abre tu terminal o línea de comandos y ejecuta:
    Bash

pip install mendeleev

Descarga los archivos: Clona este repositorio o descarga los archivos data.py, funciones.py, y calculadora_peso_molecular.py en la misma carpeta.

Ejecuta el programa:
Abre tu terminal, navega hasta la carpeta donde guardaste los archivos y ejecuta:
Bash

    python calculadora_peso_molecular.py

El programa te pedirá que ingreses una fórmula química (ej., H2O, NaCl, C6H12O6). Puedes escribir salir para terminar.

Próximos Pasos (Fases Futuras)

Esta calculadora es una base sólida para tu trabajo personal. Los próximos pasos en su desarrollo incluyen:

    Manejo de Paréntesis: Extender la lógica de _obtener_conteo_de_elementos_en_formula para procesar grupos con paréntesis (ej., Ca(OH)2).

    Manejo de Paréntesis Anidados: Ampliar el soporte para fórmulas con múltiples niveles de paréntesis (ej., K4[Fe(CN)6]).

    Cálculo de Moles: Reintroducir la funcionalidad para convertir masa a moles (g, kg, t).

    Interfaz Gráfica (Opcional): Desarrollar una interfaz de usuario más amigable que la línea de comandos.