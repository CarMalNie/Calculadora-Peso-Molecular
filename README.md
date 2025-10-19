
-----

# Calculadora de Peso Molecular (Evolución: Fase 1 a Fase 2)

Este **trabajo personal** documenta el desarrollo evolutivo de una calculadora de peso molecular. El proyecto migró de un diseño funcional simple (Fase 1) a una **arquitectura avanzada de POO** y **análisis algorítmico (Stack)** para manejar fórmulas complejas (Fase 2).

La versión actual representa la **Fase 2**, que es la versión estable y finalizada de la calculadora.

-----

## ⚙️ Fase 2: Análisis Avanzado (Commit: "Calculadora de Moles Etapa 2")

La Fase 2 es una reescritura completa del proyecto para resolver la limitación de los paréntesis e implementar principios de diseño avanzado.

### 🚀 Innovaciones y Valor Agregado

| Característica | Mejora sobre Fase 1 | Valor para el Portafolio |
| :--- | :--- | :--- |
| **Análisis de Fórmulas** | Limitado a estructuras simples. | **Resuelto con Algoritmo Stack (Pila):** Descompone fórmulas con agrupadores y anidamiento (Ej., $\text{Al}_2(\text{SO}_4)_3$, $\text{[Co}(\text{NH}_3)_6]\text{Cl}_3$). |
| **Arquitectura** | Funciones modulares. | **POO Completo:** `class CompuestoQuimico` para encapsular estado y lógica. |
| **Manejo de Datos** | Variables globales volátiles. | **Persistencia Robustez:** Guarda y carga objetos POO de forma segura en `compuestos.txt`. |
| **Encapsulación** | Sin control de acceso. | **Getters:** Acceso controlado y validado a atributos privados (`_peso_molecular`, `_es_valido`). |

### ⚠️ Restricción Crucial: Entrada Estricta IUPAC

Para garantizar resultados correctos y evitar la ambigüedad que un *parser* simple no puede resolver (Ej., si `CO2` es Cobalto y Oxígeno, o Carbono y dos Oxígenos), el programa requiere la **capitalización estricta** de la IUPAC.

  * **Si ingresa $\text{CO}_2$ (correcto),** el cálculo es preciso.
  * **Si ingresa $\text{Co}_2$ o $\text{co}_2$,** el cálculo será **incorrecto** o fallará, ya que se interpreta literalmente como el elemento $\text{Co}$ (Cobalto).

-----

## 💻 Fundamentos del Lenguaje Python (Demostrados en Fase 2)

El proyecto excede los requisitos, utilizando la modularidad POO y el algoritmo Stack para demostrar dominio sobre:

  * **Estructuras de Control Avanzadas:** Uso de `match/case` en `main.py` y el algoritmo de **Stack (Pila)** (`multiplicadores_stack`) en `compuesto_quimico.py`.
  * **Estructuras de Datos:** **Diccionarios** para conteo de elementos y **Listas** como estructuras de pila en la lógica de análisis.
  * **Modularidad:** Código dividido en capas lógicas: **Modelo** (`compuesto_quimico.py`), **Servicio** (`funciones.py`), e **Interfaz** (`main.py`).

-----

## 📚 Historial del Proyecto (Fase 1: La Base Funcional)

La Fase 1 fue la versión inicial del proyecto, sentando las bases de la modularidad y la lógica de cálculo simple.

### Características Clave (Fase 1)

  * **Cálculo de PM:** Limitado a fórmulas sin paréntesis.
  * **Validación:** Uso de `mendeleev` en `datos_quimicos.py` para validar símbolos.
  * **Normalización:** Lógica rudimentaria que intentaba corregir mayúsculas/minúsculas (ej., `h2o` $\rightarrow$ $\text{H}_2\text{O}$), la cual fue descartada en la Fase 2 por introducir ambigüedad ($\text{Co}_2$ vs $\text{CO}_2$).

-----

## Estructura del Trabajo (Fase 2)

```
.
├── compuesto_quimico.py (Modelo POO y Algoritmo STACK)
├── datos_quimicos.py    (Carga de mendeleev)
├── funciones.py         (Servicio, Gestión y Persistencia)
└── main.py              (Interfaz y Flujo)
```

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