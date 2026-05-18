# ArduinoEspañol — Analizador Léxico

Lenguaje natural simplificado en español para programar Arduino.
Reconoce instrucciones como configurar pines, encender/apagar LEDs,
mover servos y esperar tiempos.

## Información del Curso

| Campo        | Valor                               |
| ------------ | ----------------------------------- |
| Materia      | Programación de Sistemas de Base 1 |
| Institución | Universidad Autónoma de Tamaulipas |
| Semestre     | 2026-1                              |
| Profesor     | Muñoz Quintero Dante Adolfo        |

## Integrantes del Equipo

| Nombre                         | Matrícula  |
| ------------------------------ | ----------- |
| Gomez Rubio Iram Said          | a2223330159 |
| Reyes Avalos Joshua Emmanuel   | a2223330185 |
| Contreras Morales Ricardo Axel | a2223330147 |
| Serrano Vargas Aldo Antonio    | a2223330198 |

## Descripción del Lenguaje

**ArduinoEspañol** es un lenguaje imperativo de propósito educativo
diseñado para expresar instrucciones de control de hardware Arduino
usando palabras del español cotidiano. La extensión de los archivos
fuente es `.ard`.

Ejemplo de código:

```
configurar pin 13 como salida
encender led 13
esperar 500 ms
mover servo D9 a 90 grados
```

## Tokens Reconocidos

| Categoría    | Palabras / Símbolos                                                                           |
| ------------- | ---------------------------------------------------------------------------------------------- |
| ACCION        | `configurar` `encender` `apagar` `leer` `escribir` `esperar` `mover` `repetir` |
| COMPONENTE    | `led` `sensor` `servo` `buzzer` `motor` `boton` `pantalla`                       |
| PALABRA_CLAVE | `pin` `como` `en` `a` `durante` `veces`                                            |
| MODO          | `entrada` `salida` `entrada_pullup`                                                      |
| VALOR_DIGITAL | `alto` `bajo`                                                                              |
| CONTROL       | `si` `entonces` `sino` `fin_si` `fin_repetir`                                        |
| OPERADOR      | `>` `<` `>=` `<=` `==` `!=`                                                        |
| UNIDAD        | `ms` `segundos` `grados`                                                                 |
| PIN_ANALOGICO | `A0` … `A5`                                                                               |
| PIN_DIGITAL   | `D0` … `D13`                                                                              |
| NUMERO        | `100` `3.3` `500`                                                                        |
| CADENA        | `"Hola Arduino"`                                                                             |
| COMENTARIO    | `# …` `// …` `/* … */` (descartados)                                                  |

## Cómo Ejecutar

**Requisitos:** Python 3.10+

```powershell
# Programa válido
python src/main.py tests/valid/programa1.ard

# Programa con errores
python src/main.py tests/invalid/errores1.ard
```

## Estructura del Proyecto

```
analizador-lexico-arduinoespanol/
├── src/
│   ├── main.py      ← punto de entrada
│   ├── lexer.py     ← analizador léxico
│   ├── tokens.py    ← tipos de token + clase Token
│   └── errors.py    ← reporte de errores
├── grammar/
│   └── ArduinoEspanol.g4
├── tests/
│   ├── valid/       ← programas correctos
│   └── invalid/     ← programas con errores léxicos
├── docs/
└── capturas/
```

## Ejemplos de Uso

**Entrada válida (`programa1.ard`):**

```
configurar pin 13 como salida
encender led 13
esperar 500 ms
```

**Salida esperada:**

```
[  1] Token(Configurar       'configurar'  linea=2, col=1)
[  2] Token(Pin              'pin'         linea=2, col=12)
[  3] Token(Numero           13            linea=2, col=16)
[  4] Token(Como             'como'        linea=2, col=19)
[  5] Token(Salida           'salida'      linea=2, col=24)
```
