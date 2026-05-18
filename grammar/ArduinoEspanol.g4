/**
 * ArduinoEspanol.g4
 * Gramática ANTLR 4 para el lenguaje ArduinoEspañol.
 *
 * ArduinoEspañol es un lenguaje natural simplificado en español
 * para controlar hardware Arduino: pines, LEDs, servos, sensores,
 * buzzers, motores y pantallas.
 *
 * Herramienta: ANTLR 4 con target Python 3
 * Autor: ArduinoEspañol Team — 2026
 */

grammar ArduinoEspanol;

// ══════════════════════════════════════════════════════════════════
//  REGLAS DE PARSER (instrucciones del lenguaje)
// ══════════════════════════════════════════════════════════════════

programa
    : instruccion* EOF
    ;

instruccion
    : instrConfigPin
    | instrEncender
    | instrApagar
    | instrEsperar
    | instrMoverServo
    | instrLeer
    | instrEscribir
    | instrRepetir
    | instrSi
    ;

instrConfigPin
    : CONFIGURAR PIN (NUMERO | PIN_DIGITAL | PIN_ANALOGICO) COMO modo
    ;

instrEncender
    : ENCENDER componente (NUMERO | PIN_DIGITAL | PIN_ANALOGICO)
    ;

instrApagar
    : APAGAR componente (NUMERO | PIN_DIGITAL | PIN_ANALOGICO)
    ;

instrEsperar
    : ESPERAR NUMERO unidad
    ;

instrMoverServo
    : MOVER SERVO (NUMERO | PIN_DIGITAL) A NUMERO GRADOS
    ;

instrLeer
    : LEER SENSOR EN (PIN_ANALOGICO | PIN_DIGITAL)
    ;

instrEscribir
    : ESCRIBIR componente (NUMERO | PIN_DIGITAL) valorDigital
    ;

instrRepetir
    : REPETIR NUMERO VECES instruccion* FIN_REPETIR
    ;

instrSi
    : SI condicion ENTONCES instruccion* (SINO instruccion*)? FIN_SI
    ;

condicion
    : (PIN_ANALOGICO | PIN_DIGITAL | IDENTIFICADOR) operadorRelacional NUMERO
    ;

operadorRelacional
    : MAYOR_IGUAL | MENOR_IGUAL | IGUAL | DIFERENTE | MAYOR | MENOR
    ;

modo
    : ENTRADA | SALIDA | ENTRADA_PULLUP
    ;

componente
    : LED | SENSOR | SERVO | BUZZER | MOTOR | BOTON | PANTALLA
    ;

valorDigital
    : ALTO | BAJO
    ;

unidad
    : MS | SEGUNDOS | GRADOS
    ;


// ══════════════════════════════════════════════════════════════════
//  REGLAS LÉXICAS — ACCIONES
// ══════════════════════════════════════════════════════════════════

CONFIGURAR : 'configurar';
ENCENDER   : 'encender';
APAGAR     : 'apagar';
LEER       : 'leer';
ESCRIBIR   : 'escribir';
ESPERAR    : 'esperar';
MOVER      : 'mover';
REPETIR    : 'repetir';

// ── COMPONENTES ──────────────────────────────────────────────────

LED      : 'led';
SENSOR   : 'sensor';
SERVO    : 'servo';
BUZZER   : 'buzzer';
MOTOR    : 'motor';
BOTON    : 'boton';
PANTALLA : 'pantalla';

// ── PALABRAS CLAVE DE SINTAXIS ────────────────────────────────────

PIN    : 'pin';
COMO   : 'como';
EN     : 'en';
A      : 'a';
DURANTE: 'durante';
VECES  : 'veces';

// ── MODOS DE PIN ─────────────────────────────────────────────────

ENTRADA        : 'entrada';
SALIDA         : 'salida';
ENTRADA_PULLUP : 'entrada_pullup';

// ── VALORES DIGITALES ────────────────────────────────────────────

ALTO : 'alto';
BAJO : 'bajo';

// ── CONTROL DE FLUJO ─────────────────────────────────────────────

SI          : 'si';
ENTONCES    : 'entonces';
SINO        : 'sino';
FIN_SI      : 'fin_si';
FIN_REPETIR : 'fin_repetir';

// ── OPERADORES RELACIONALES ───────────────────────────────────────

MAYOR_IGUAL : '>=';
MENOR_IGUAL : '<=';
IGUAL       : '==';
DIFERENTE   : '!=';
MAYOR       : '>';
MENOR       : '<';

// ── UNIDADES ─────────────────────────────────────────────────────

MS       : 'ms';
SEGUNDOS : 'segundos';
GRADOS   : 'grados';

// ── LITERALES ────────────────────────────────────────────────────

PIN_ANALOGICO : 'A' [0-5];
PIN_DIGITAL   : 'D' [0-9] [0-3]?;   // D0..D13

NUMERO : [0-9]+ ('.' [0-9]+)?;

CADENA : '"' ~["\r\n]* '"';

IDENTIFICADOR : [a-zA-Z_] [a-zA-Z0-9_]*;

// ── DELIMITADORES ────────────────────────────────────────────────

PUNTO_COMA : ';';
LPAREN     : '(';
RPAREN     : ')';
LBRACE     : '{';
RBRACE     : '}';

// ── IGNORADOS ────────────────────────────────────────────────────

COMENTARIO : '#' ~[\r\n]*   -> skip;   // comentario de una línea con #
COMENTARIO_LINEA  : '//' ~[\r\n]* -> skip;
COMENTARIO_BLOQUE : '/*' .*? '*/'  -> skip;
WS         : [ \t\r\n]+     -> skip;
