
-----

# Calculadora de Peso Molecular (Evolución: Fase 1 a Fase 2)

Este **trabajo personal** documenta el desarrollo evolutivo de una calculadora de peso molecular. El proyecto migró de un diseño funcional simple (Fase 1) a una **arquitectura de Programación Orientada a Objetos (POO)** y **análisis algorítmico (Stack)** para manejar fórmulas complejas.

La versión actual representa la **Fase 2** (el commit "Calculadora de Moles Etapa 2"), que es la versión estable y finalizada de la calculadora.

-----

## Fase 2: Análisis Avanzado y POO (Versión Actual)

La Fase 2 es una reescritura completa del proyecto, enfocada en resolver la limitación de la Fase 1 (no manejar paréntesis) e implementar principios de diseño avanzado.

### Innovaciones y Valor Agregado

| Característica | Mejora sobre Fase 1 | Valor para el Portafolio |
| :--- | :--- | :--- |
| **Análisis de Fórmulas** | Limitado a estructuras simples. | **Algoritmo Stack (Pila):** Descompone fórmulas con agrupadores y anidamiento (Ej., $\text{Al}_2(\text{SO}_4)_3$, $\text{[Co}(\text{NH}_3)_6]\text{Cl}_3$). |
| **Arquitectura** | Funciones modulares. | **POO Completo:** `class CompuestoQuimico` para encapsular estado y lógica. |
| **Persistencia** | Variables globales volátiles. | **Persistencia Robusta:** Guarda y carga **objetos POO** de forma segura en `compuestos.txt`. |
| **Encapsulación** | Sin control de acceso. | **Getters:** Acceso controlado y validado a atributos privados, demostrando el uso de **getters**. |

### Restricción Crucial: Entrada Estricta IUPAC

Para garantizar resultados precisos y evitar la ambigüedad irresoluble de $\text{CO}_2$ vs. $\text{Co}_2$ (un problema que la Fase 1 no podía resolver), el programa requiere que el usuario ingrese la fórmula respetando estrictamente la **capitalización de la IUPAC**.

-----

## Fundamentos del Lenguaje Python (Demostrados en Fase 2)

El proyecto excede los requisitos mínimos, aplicando el diseño POO y el algoritmo Stack para demostrar dominio sobre:

* **Estructuras de Control Avanzadas:** Uso de **`match/case`** en `main.py` para el despacho limpio del menú, y el algoritmo de **Stack (Pila)** para el análisis sintáctico químico.
* **Estructuras de Datos:** **Diccionarios** para conteo de elementos y **Listas** como estructuras de pila en la lógica de análisis.
* **Modularidad:** El código está dividido en capas lógicas: **Modelo** (`compuesto_quimico.py`), **Servicio** (`funciones.py`), e **Interfaz** (`main.py`).

-----

## Historial del Proyecto (Fase 1: La Base Funcional)

La Fase 1 fue la versión inicial del proyecto, sentando las bases de la modularidad y la lógica de cálculo simple. Esta fase fue completamente reemplazada por la arquitectura POO de la Fase 2.

### Características Clave (Fase 1)

* **Cálculo de PM:** Limitado a fórmulas sin paréntesis.
* **Validación:** Uso de `mendeleev` en `datos_quimicos.py` para validar símbolos.
* **Manejo de Entrada:** Intentaba corregir minúsculas a mayúsculas (ej., `h2o` $\rightarrow$ $\text{H}_2\text{O}$), una lógica que fue descartada en la Fase 2 por ser ambigua.

-----

## Visión a Futuro: Fase 3 - Modelado Relacional

Una vez completada la lógica de cálculo en Python, la **Fase 3** se enfoca en la **Persistencia Avanzada y el Modelado de Datos** utilizando **MySQL Workbench**.

El objetivo es migrar el almacenamiento de los resultados (actualmente en `compuestos.txt`) a un diseño estructurado de **Base de Datos Relacional**. Este diseño de **6 tablas** (que incluye Elementos, Compuestos, Aplicaciones y sus tablas $\text{M:M}$ intermedias) demostrará el dominio del **Modelado Entidad-Relación (ERD)**, independientemente del código Python.

---

### Estructura del Trabajo (Fase 2)

```

.
├── compuesto\_quimico.py (Modelo POO y Algoritmo STACK)
├── datos\_quimicos.py    (Carga de mendeleev)
├── funciones.py         (Servicio, Gestión y Persistencia)
└── main.py              (Interfaz y Flujo)

````

### Cómo Ejecutar el Código

1.  **Instala la Dependencia:**
    ```bash
    pip install mendeleev
    ```
2.  **Ejecuta el Script Principal:**
    ```bash
    python main.py
    ```

El programa se inicia con un menú de 4 opciones. La **Opción 4 (Guardar y Salir)** asegura la persistencia de tus cálculos.
````