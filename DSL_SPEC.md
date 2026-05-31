# ESPECIFICACIÓN FORMAL DEL DSL: "LENGUAJE L"
## Para el Control de Microredes Inteligentes ECO-GRID

Este documento define la especificación técnica completa (léxica, sintáctica y ejemplos pragmáticos) de un **Lenguaje de Dominio Específico (DSL)** imperativo y declarativo llamado **"Lenguaje L"**. Su propósito es modelar, automatizar y controlar las operaciones de la microred de distribución eléctrica **ECO-GRID**, especializada en la conmutación de líneas de distribución de energía, monitoreo térmico en bancos de almacenamiento y balanceo de carga en acumuladores.

---

## 1. Componente Léxico

El análisis léxico (morfología) descompone el texto plano del código fuente en tokens válidos. Cualquier carácter que no pertenezca al alfabeto definido o no encaje en las expresiones regulares de tokens producirá un **Error Léxico** en la primera fase del compilador.

### 1.1 Alfabeto ($\Sigma$)
El alfabeto del "Lenguaje L" es el conjunto de símbolos permitidos para construir programas:

$$\Sigma = \{ a\text{-}z, A\text{-}Z \} \cup \{ 0\text{-}9 \} \cup \{ +, -, *, /, \% \} \cup \{ =, <, >, ! \} \cup \{ (, ), ,, ;, \_, \text{#} \} \cup \{ \text{Espacio}, \text{Tabulación}, \text{Salto de línea} \}$$

### 1.2 Comentarios y Espacios en Blanco
- **Espacios en blanco y saltos de línea**: Se utilizan exclusivamente como delimitadores léxicos para separar tokens y son ignorados en la generación del árbol sintáctico (AST).
- **Comentarios**: Inician con el carácter `#` y se extienden hasta el final de la línea. Son desechados en el análisis léxico.

### 1.3 Expresiones Regulares de Categorías Léxicas
Para la especificación formal del Lexer, definimos las siguientes expresiones regulares en formato extendido POSIX:

- **Identificadores (ID)**: Representan nombres de variables o instancias de microredes. Deben iniciar con una letra o guion bajo, seguidos de letras, dígitos o guiones bajos.
  $$\text{Regex: } [a\text{-}zA\text{-}Z\_][a\text{-}zA\text{-}Z0\text{-}9\_]*$$
- **Literales Numéricos (NUM)**: Soporta números enteros y reales de punto flotante de precisión doble.
  $$\text{Regex: } [0\text{-}9]+(\.[0\text{-}9]+)?$$

### 1.4 Tabla Detallada de Tokens del Sistema

El "Lenguaje L" cuenta con palabras clave de control y funciones de hardware integradas (*built-ins*) reservadas. La siguiente tabla presenta el catálogo léxico completo:

| Nombre del Token | Lexema / Expresión Regular | Descripción Teórica y Rol en la Microred |
| :--- | :--- | :--- |
| `TK_INIT_GRID` | `init_grid` | Palabra clave para inicializar el bus de control de una microred física. |
| `TK_LEER_TEMP` | `leer_temperatura` | Función incorporada para leer la sonda térmica de un banco de baterías. |
| `TK_ESTADO_CARGA` | `estado_carga` | Función incorporada que retorna el porcentaje de energía útil del acumulador. |
| `TK_CONMUTAR` | `conmutar_linea` | Comando que acciona los interruptores físicos de la línea de energía. |
| `TK_SI` | `si` | Inicio de la bifurcación condicional. |
| `TK_ENTONCES` | `entonces` | Delimitador que introduce el bloque de ejecución del condicional. |
| `TK_FIN_SI` | `fin_si` | Fin del bloque condicional. Evita la ambigüedad sintáctica. |
| `TK_MIENTRAS` | `mientras` | Inicio del bucle condicional iterativo de retroalimentación. |
| `TK_EJECUTAR` | `ejecutar` | Delimitador que introduce el bloque de sentencias del bucle. |
| `TK_FIN_MIENTRAS` | `fin_mientras` | Cierre del bucle condicional. |
| `TK_ID` | `[a-zA-Z_][a-zA-Z0-9_]*` | Identificador de variable o nombre de la red. |
| `TK_NUM` | `[0-9]+(\.[0-9]+)?` | Valores numéricos de estados físicos o constantes de umbral. |
| `TK_ASIG` | `=` | Operador de asignación de variables. |
| `TK_OP_COMP` | `==` \| `!=` \| `<` \| `>` \| `<=` \| `>=` | Operadores lógicos relacionales de comparación de estado. |
| `TK_OP_ARIT` | `+` \| `-` \| `*` \| `/` | Operadores aritméticos binarios. |
| `TK_LPAREN` | `(` | Paréntesis de apertura para parámetros de funciones. |
| `TK_RPAREN` | `)` | Paréntesis de cierre para parámetros de funciones. |
| `TK_COMMA` | `,` | Separador de argumentos funcionales. |
| `TK_SEMI` | `;` | Punto y coma delimitador de fin de instrucción obligatoria. |

---

## 2. Componente Sintáctico (Gramática Formal EBNF)

Para validar la correcta estructura gramatical de las condiciones y bucles, definimos la **Gramática Libre de Contexto (CFG)** del "Lenguaje L" utilizando la notación sintáctica **EBNF (Extended Backus-Naur Form)**.

Esta gramática resuelve de manera determinista la precedencia de operadores aritméticos y condicionales, facilitando la construcción de parsers del tipo recursivo descendente (LL).

```ebnf
(* Regla Raíz del Programa *)
Programa              ::= Sentencia* EOF

(* Estructura de las Sentencias *)
Sentencia             ::= SentenciaInit
                        | SentenciaAsig
                        | SentenciaConmutar
                        | SentenciaSi
                        | SentenciaMientras

(* Declaraciones Imperativas *)
SentenciaInit         ::= "init_grid" "(" Identificador ")" ";"
SentenciaAsig         ::= Identificador "=" Expresion ";"
SentenciaConmutar     ::= "conmutar_linea" "(" Expresion "," Expresion ")" ";"

(* Estructuras de Control con Tokens Delimitadores Explícitos *)
SentenciaSi           ::= "si" Condicion "entonces" Sentencia* "fin_si"
SentenciaMientras     ::= "mientras" Condicion "ejecutar" Sentencia* "fin_mientras"

(* Expresiones Condicionales *)
Condicion             ::= Expresion OperadorComp Expresion

(* Expresiones Aritméticas (Resolución de Precedencia y Asociatividad) *)
Expresion             ::= Termino ( ( "+" | "-" ) Termino )*
Termino               ::= Factor ( ( "*" | "/" ) Factor )*
Factor                ::= Identificador
                        | Numero
                        | LlamadaFuncion
                        | "(" Expresion ")"

(* Llamadas a Funciones de Monitoreo de Microred *)
LlamadaFuncion        ::= "leer_temperatura" "(" Expresion ")"
                        | "estado_carga" "(" Expresion ")"

(* Componentes Léxicos Terminales *)
OperadorComp          ::= "==" | "!=" | "<" | ">" | "<=" | ">="
Identificador         ::= [a-zA-Z_][a-zA-Z0-9_]*
Numero                ::= [0-9]+(\.[0-9]+)?
```

---

## 3. Programas de Ejemplo en "Lenguaje L"

### 3.1 Escenario A: Prevención de Fuga Térmica en Baterías

**Objetivo**: Monitorear continuamente el sensor térmico del banco de baterías 1. Si la temperatura del acumulador supera un umbral crítico de $45.0^\circ\text{C}$ (lo cual indica un riesgo inminente de fuga térmica), se debe desconectar la línea de carga 3 para detener el influjo de corriente y activar simultáneamente la línea 4 conectada a los sopladores de refrigeración líquida. Una vez que la temperatura descienda por debajo de los $38.0^\circ\text{C}$, se restaura el sistema a su estado normal.

```lenguaje_l
# =====================================================================
# ESCENARIO A: CONTROL DE EMERGENCIA POR FUGA TÉRMICA (BANCO BATERÍAS 1)
# =====================================================================

init_grid(ECO_GRID_CENTRAL);

# Monitorear e iterar mientras dure la condición de calentamiento crítico
mientras leer_temperatura(bateria_01) > 45.0 ejecutar
    conmutar_linea(linea_carga_03, 0);  # Desconectar línea 3 (Entrada de Carga de Baterías)
    conmutar_linea(linea_refrigeracion_04, 1);  # Conectar línea 4 (Bomba de Refrigeración Líquida)
fin_mientras;

# Fase de histéresis: restaurar la microred si se estabiliza la temperatura
si leer_temperatura(bateria_01) <= 38.0 entonces
    conmutar_linea(linea_refrigeracion_04, 0);  # Apagar la bomba de refrigeración
    conmutar_linea(linea_carga_03, 1);  # Reconectar la línea 3 para reanudar la carga estándar
fin_si;
```

---

### 3.2 Escenario B: Balance de Carga Energética de Acumuladores

**Objetivo**: Leer el estado de carga (SoC) del grupo de acumuladores de respaldo 2. 
- Si el SoC es superior al $80\%$, significa que hay un superávit de energía almacenada. Por ende, se conmutan las líneas de distribución auxiliar 5 y 6 para derivar la energía excedente hacia la red vecinal o un sistema de riego comunitario.
- Si el SoC cae por debajo del $20\%$, la microred entra en estado de preservación de reserva. Se debe desconectar inmediatamente la línea 7 que alimenta a los consumidores comerciales no esenciales para prevenir descargas profundas destructivas en las celdas químicas del acumulador.

```lenguaje_l
# =====================================================================
# ESCENARIO B: BALANCEO AUTOMÁTICO DE CARGA Y PRESERVACIÓN DE RESERVA
# =====================================================================

init_grid(ECO_GRID_CENTRAL);

# Guardar el estado de carga actual del acumulador 2 en una variable
soc_baterias2 = estado_carga(bateria_02);

# Caso de Superávit de Energía (Baterías llenas)
si soc_baterias2 > 80.0 entonces
    conmutar_linea(linea_vecinal_05, 1);  # Activar línea 5 (Distribución auxiliar a red vecinal)
    conmutar_linea(linea_riego_06, 1);  # Activar línea 6 (Derivación a riego comunitario)
fin_si;

# Caso de Déficit Crítico (Preservación de celdas)
si soc_baterias2 < 20.0 entonces
    conmutar_linea(linea_industrial_07, 0);  # Desconectar línea 7 (Consumidores industriales no esenciales)
    conmutar_linea(linea_generador_08, 1);  # Conectar línea 8 (Generador diesel de respaldo auxiliar)
fin_si;
```

---

## 4. Análisis de Diseño del Compilador para "Lenguaje L"

1. **Evitando Ambigüedad de Bifurcaciones**: El uso de delimitadores explícitos de cierre (`fin_si` y `fin_mientras`) resuelve sintácticamente el problema clásico de la **Asociación Colgante** (*dangling else*). El parser del compilador siempre sabrá exactamente a qué estructura de control pertenece un bloque interno de sentencias sin recurrir a reglas heurísticas complejas.
2. **Chequeo de Tipos Estático**: A nivel del análisis semántico del compilador, se requiere que la variable que recibe el resultado de `estado_carga()` y `leer_temperatura()` sea un tipo flotante (`f64`). Del mismo modo, el segundo parámetro de `conmutar_linea()` debe limitarse estrictamente al conjunto de booleanos o números binarios $\{0, 1\}$, lo cual será validado en la fase de análisis de tipos.
3. **Mapeo de Funciones Integradas**: Funciones como `leer_temperatura(1)` se traducen en el árbol sintáctico (AST) a llamadas del sistema o lectura de puertos de hardware I/O mediante interrupciones directas del hardware del microcontrolador de la red ECO-GRID.
