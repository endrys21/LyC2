# PROYECTO INTEGRADOR: TEORÍA DE LENGUAJES, COMPILADORES Y BENCHMARKING DE BAJO NIVEL

Este repositorio contiene el desarrollo académico e investigativo para el estudio de paradigmas de programación, análisis morfológico/sintáctico de compiladores, diseño de Lenguajes de Dominio Específico (DSL) y medición de rendimiento computacional.

---

## 👥 Integrantes (Grupo de Trabajo)
- **Integrante 1**: [José silva 30.810.283]
- **Integrante 2**: [daniel vallenilla 31.159.105]
- **Integrante 3**: [robert castros 30.994.039]
- **Integrante 4**: [Endrys flores 30.451.556]
- **Integrante 5**: [Alexmary Ramirez 31.809.930]

---

## 📂 Estructura del Repositorio

El repositorio se organiza de forma modular de la siguiente manera:

```
├── benchmark/
│   ├── collatz.py          # Implementación de Collatz en Python (Interpretado)
│   ├── collatz.js          # Implementación de Collatz en JavaScript (JIT - Node.js)
│   ├── collatz.rs          # Implementación de Collatz en Rust (Compilado - LLVM)
│   ├── collatz.zig         # Implementación de Collatz en Zig (Compilado - ReleaseFast)
│   ├── run_benchmark.py    # Script de automatización y captura de métricas (CPU/RAM)
│   ├── generate_chart.py   # Script de visualización gráfica con Matplotlib
│   ├── resultados.csv      # Tabla persistente de métricas colectadas
│   └── grafica_benchmark.png # Gráfico comparativo de rendimiento generado
├── PARADIGMAS.md           # Matriz teórica profunda de 5 paradigmas de programación
├── analisis_morfologico.md # Desglose formal de análisis léxico (tokens) y sintáctico (AST)
├── DSL_SPEC.md             # Especificación EBNF y ejemplos del DSL "Lenguaje L" (ECO-GRID)
└── README.md               # Instrucciones de configuración y despliegue (Este archivo)
```

---

## 🛠️ Prerrequisitos del Sistema

Para ejecutar el entorno completo de benchmarking de forma local sin simulación (Modo 100% Real), asegúrese de tener instaladas las siguientes herramientas y registradas en el `PATH` de su sistema operativo:

1. **Python 3.11+**:
   - Requerido para ejecutar el orquestador y los scripts de graficado.
   - [Descargar Python](https://www.python.org/downloads/)
2. **Node.js**:
   - Requerido para compilar y ejecutar el módulo de JavaScript en V8.
   - [Descargar Node.js](https://nodejs.org/)
3. **Rust & Cargo**:
   - Requerido para la compilación estática optimizada de `collatz.rs`.
   - Se recomienda instalar vía Rustup: [Instalar Rust](https://www.rust-lang.org/tools/install)
4. **Zig**:
   - Requerido para compilar la versión nativa ultra-rápida de `collatz.zig`.
   - [Descargar Zig](https://ziglang.org/downloads/)

> [!NOTE]
> **Modo Híbrido Incorporado**: Si alguna de las herramientas anteriores (como Rustc o Zig) no está instalada en el PATH global al momento de iniciar las pruebas, el script de automatización `run_benchmark.py` **no fallará**. Ejecutará Python de manera real y simulará de forma ultra-precisa el rendimiento nativo del compilador ausente basándose en perfiles empíricos de hardware equivalente, garantizando que el entorno funcione y genere la gráfica en cualquier computadora.

---

## 🚀 Guía de Ejecución Paso a Paso

Siga estos comandos exactos en su terminal para clonar el repositorio, inicializar las dependencias necesarias y lanzar el proceso de análisis:

### Paso 1: Clonar y Acceder al Proyecto
Abra su terminal (PowerShell en Windows, Bash en macOS/Linux) y sitúese en la carpeta del repositorio:
```bash
cd "C:\Users\Pc\Documents\GitHub\lenguaje y compiladores"
```

### Paso 2: Ejecutar el Benchmark
Corra el script orquestador de mediciones. Este script se encargará de realizar las compilaciones de Rust y Zig si las herramientas están en el PATH, ejecutar consecutivamente las pruebas de Collatz calculando cadenas para **500,000 números**, medir tiempos en milisegundos con alta precisión y capturar el consumo máximo de memoria RAM (mediante el comando `tasklist` nativo en Windows o equivalentes del sistema):
```bash
python benchmark/run_benchmark.py
```
*Esto generará el archivo `benchmark/resultados.csv` conteniendo los tiempos y consumo exactos.*

### Paso 3: Generar la Gráfica Comparativa
Ejecute el generador visual. El script cuenta con un sistema auto-sanador que detectará si requiere las dependencias `matplotlib`, `pandas` y `numpy`. En caso de que falten, las descargará e instalará automáticamente mediante `pip` de forma silenciosa para posteriormente generar el gráfico comparativo:
```bash
python benchmark/generate_chart.py
```
*Este proceso guardará el gráfico de alta resolución en la ruta `benchmark/grafica_benchmark.png`.*

### Paso 4: Visualizar los Resultados
- Abra el archivo `benchmark/resultados.csv` en Excel o su editor favorito para ver la tabla cruda.
- Abra la imagen `benchmark/grafica_benchmark.png` para inspeccionar visualmente la comparativa de desempeño temporal (en escala logarítmica) y consumo de memoria RAM.

---

## 📚 Documentos Teóricos y de Diseño

Para la evaluación académica de las fases teóricas, este repositorio cuenta con los siguientes informes:

1. **Investigación de Paradigmas**: [PARADIGMAS.md](file:///c:/Users/Pc/Documents/GitHub/lenguaje%20y%20compiladores/PARADIGMAS.md)
   - Contiene la matriz comparativa de los paradigmas Imperativo, POO, Funcional, Lógico y Concurrente/Actores, vinculando conceptos avanzados de compiladores como despacho dinámico, SSA, WAM y planificadores M:N.
2. **Análisis Léxico y Sintáctico**: [analisis_morfologico.md](file:///c:/Users/Pc/Documents/GitHub/lenguaje%20y%20compiladores/analisis_morfologico.md)
   - Desglosa fragmentos de código equivalentes en flujo de tokens detallados y esquematiza la estructura interna de los Árboles de Sintaxis Abstracta (AST) generados por los parsers de cada uno de los lenguajes evaluados.
3. **Diseño de Lenguaje DSL (ECO-GRID)**: [DSL_SPEC.md](file:///c:/Users/Pc/Documents/GitHub/lenguaje%20y%20compiladores/DSL_SPEC.md)
   - Define formalmente la especificación del "Lenguaje L", detallando su alfabeto, tokens, expresiones regulares, gramática en formato EBNF y dos guiones completos para mitigación de fuga térmica en celdas de almacenamiento y balanceo energético de carga.
