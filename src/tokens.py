from enum import Enum, auto
from dataclasses import dataclass
from typing import Any


# ══════════════════════════════════════════════════════════════════════════════
#  TIPOS DE TOKEN — ArduinoEspañol
# ══════════════════════════════════════════════════════════════════════════════

class TokenTypes(Enum):
    # ── ACCIONES ─────────────────────────────────────────────────────────────
    Configurar     = auto()   # configurar
    Encender       = auto()   # encender
    Apagar         = auto()   # apagar
    Leer           = auto()   # leer
    Escribir       = auto()   # escribir
    Esperar        = auto()   # esperar
    Mover          = auto()   # mover
    Repetir        = auto()   # repetir

    # ── COMPONENTES ──────────────────────────────────────────────────────────
    Led            = auto()   # led
    Sensor         = auto()   # sensor
    Servo          = auto()   # servo
    Buzzer         = auto()   # buzzer
    Motor          = auto()   # motor
    Boton          = auto()   # boton
    Pantalla       = auto()   # pantalla

    # ── PALABRAS CLAVE DE SINTAXIS ────────────────────────────────────────────
    Pin            = auto()   # pin
    Como           = auto()   # como
    En             = auto()   # en
    A              = auto()   # a
    Durante        = auto()   # durante
    Veces          = auto()   # veces

    # ── MODOS DE PIN ─────────────────────────────────────────────────────────
    Entrada        = auto()   # entrada
    Salida         = auto()   # salida
    EntradaPullup  = auto()   # entrada_pullup

    # ── VALORES DIGITALES ────────────────────────────────────────────────────
    Alto           = auto()   # alto  (HIGH)
    Bajo           = auto()   # bajo  (LOW)

    # ── CONTROL DE FLUJO ─────────────────────────────────────────────────────
    Si             = auto()   # si
    Entonces       = auto()   # entonces
    SiNo           = auto()   # sino
    FinSi          = auto()   # fin_si
    FinRepetir     = auto()   # fin_repetir

    # ── OPERADORES RELACIONALES ───────────────────────────────────────────────
    MayorIgualQ    = auto()   # >=
    MenorIgualQ    = auto()   # <=
    Igual          = auto()   # ==
    Diferente      = auto()   # !=
    MayorQ         = auto()   # >
    MenorQ         = auto()   # <

    # ── UNIDADES ─────────────────────────────────────────────────────────────
    Ms             = auto()   # ms
    Segundos       = auto()   # segundos
    Grados         = auto()   # grados

    # ── LITERALES ────────────────────────────────────────────────────────────
    PinAnalogico   = auto()   # A0 … A5
    PinDigital     = auto()   # D0 … D13
    Numero         = auto()   # entero o flotante: 100, 3.3
    Cadena         = auto()   # "Hola Arduino"
    Identificador  = auto()   # nombre de variable del usuario

    # ── DELIMITADORES ────────────────────────────────────────────────────────
    PuntoYComa     = auto()   # ;
    ParentesisI    = auto()   # (
    ParentesisD    = auto()   # )
    LlaveApertura  = auto()   # {
    LlaveCierre    = auto()   # }

    # ── ESPECIALES ───────────────────────────────────────────────────────────
    NuevaLinea     = auto()   # \n  (separador de instrucciones)
    Error          = auto()   # carácter no reconocido
    FinalCodigo    = auto()   # EOF


# ══════════════════════════════════════════════════════════════════════════════
#  CLASE TOKEN
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class Token:
    tipo: TokenTypes
    valor: Any
    linea: int
    columna: int
    posicion: int

    def __str__(self) -> str:
        return (
            f"Token({self.tipo.name:<18} {repr(self.valor):<20} "
            f"linea={self.linea}, col={self.columna})"
        )

    def __repr__(self) -> str:
        return (
            f"Token(tipo={self.tipo.name}, valor={self.valor!r}, "
            f"linea={self.linea}, columna={self.columna}, posicion={self.posicion})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Token):
            return False
        return self.tipo == other.tipo and self.valor == other.valor

    # ── Genéricos ─────────────────────────────────────────────────────────────

    def es_tipo(self, tipo: TokenTypes) -> bool:
        """Verifica si el token es del tipo dado."""
        return self.tipo == tipo

    def tiene_valor(self, valor_esperado: Any) -> bool:
        return self.valor == valor_esperado

    def coincide(self, tipo: TokenTypes, valor: Any = None) -> bool:
        if valor is None:
            return self.es_tipo(tipo)
        return self.es_tipo(tipo) and self.tiene_valor(valor)

    # ── Acciones ──────────────────────────────────────────────────────────────

    def es_configurar(self) -> bool:
        return self.es_tipo(TokenTypes.Configurar)

    def es_encender(self) -> bool:
        return self.es_tipo(TokenTypes.Encender)

    def es_apagar(self) -> bool:
        return self.es_tipo(TokenTypes.Apagar)

    def es_leer(self) -> bool:
        return self.es_tipo(TokenTypes.Leer)

    def es_escribir(self) -> bool:
        return self.es_tipo(TokenTypes.Escribir)

    def es_esperar(self) -> bool:
        return self.es_tipo(TokenTypes.Esperar)

    def es_mover(self) -> bool:
        return self.es_tipo(TokenTypes.Mover)

    def es_repetir(self) -> bool:
        return self.es_tipo(TokenTypes.Repetir)

    # ── Componentes ───────────────────────────────────────────────────────────

    def es_led(self) -> bool:
        return self.es_tipo(TokenTypes.Led)

    def es_sensor(self) -> bool:
        return self.es_tipo(TokenTypes.Sensor)

    def es_servo(self) -> bool:
        return self.es_tipo(TokenTypes.Servo)

    def es_buzzer(self) -> bool:
        return self.es_tipo(TokenTypes.Buzzer)

    def es_motor(self) -> bool:
        return self.es_tipo(TokenTypes.Motor)

    def es_boton(self) -> bool:
        return self.es_tipo(TokenTypes.Boton)

    def es_pantalla(self) -> bool:
        return self.es_tipo(TokenTypes.Pantalla)

    # ── Palabras clave de sintaxis ────────────────────────────────────────────

    def es_pin(self) -> bool:
        return self.es_tipo(TokenTypes.Pin)

    def es_como(self) -> bool:
        return self.es_tipo(TokenTypes.Como)

    def es_en(self) -> bool:
        return self.es_tipo(TokenTypes.En)

    def es_a(self) -> bool:
        return self.es_tipo(TokenTypes.A)

    def es_durante(self) -> bool:
        return self.es_tipo(TokenTypes.Durante)

    def es_veces(self) -> bool:
        return self.es_tipo(TokenTypes.Veces)

    # ── Modos de pin ─────────────────────────────────────────────────────────

    def es_entrada(self) -> bool:
        return self.es_tipo(TokenTypes.Entrada)

    def es_salida(self) -> bool:
        return self.es_tipo(TokenTypes.Salida)

    def es_entrada_pullup(self) -> bool:
        return self.es_tipo(TokenTypes.EntradaPullup)

    # ── Valores digitales ────────────────────────────────────────────────────

    def es_alto(self) -> bool:
        return self.es_tipo(TokenTypes.Alto)

    def es_bajo(self) -> bool:
        return self.es_tipo(TokenTypes.Bajo)

    # ── Control de flujo ─────────────────────────────────────────────────────

    def es_si(self) -> bool:
        return self.es_tipo(TokenTypes.Si)

    def es_entonces(self) -> bool:
        return self.es_tipo(TokenTypes.Entonces)

    def es_sino(self) -> bool:
        return self.es_tipo(TokenTypes.SiNo)

    def es_fin_si(self) -> bool:
        return self.es_tipo(TokenTypes.FinSi)

    def es_fin_repetir(self) -> bool:
        return self.es_tipo(TokenTypes.FinRepetir)

    # ── Operadores relacionales ───────────────────────────────────────────────

    def es_mayor_igual_q(self) -> bool:
        return self.es_tipo(TokenTypes.MayorIgualQ)

    def es_menor_igual_q(self) -> bool:
        return self.es_tipo(TokenTypes.MenorIgualQ)

    def es_igual(self) -> bool:
        return self.es_tipo(TokenTypes.Igual)

    def es_diferente(self) -> bool:
        return self.es_tipo(TokenTypes.Diferente)

    def es_mayor_q(self) -> bool:
        return self.es_tipo(TokenTypes.MayorQ)

    def es_menor_q(self) -> bool:
        return self.es_tipo(TokenTypes.MenorQ)

    # ── Unidades ─────────────────────────────────────────────────────────────

    def es_ms(self) -> bool:
        return self.es_tipo(TokenTypes.Ms)

    def es_segundos(self) -> bool:
        return self.es_tipo(TokenTypes.Segundos)

    def es_grados(self) -> bool:
        return self.es_tipo(TokenTypes.Grados)

    # ── Literales ────────────────────────────────────────────────────────────

    def es_pin_analogico(self) -> bool:
        return self.es_tipo(TokenTypes.PinAnalogico)

    def es_pin_digital(self) -> bool:
        return self.es_tipo(TokenTypes.PinDigital)

    def es_numero(self) -> bool:
        return self.es_tipo(TokenTypes.Numero)

    def es_cadena(self) -> bool:
        return self.es_tipo(TokenTypes.Cadena)

    def es_identificador(self) -> bool:
        return self.es_tipo(TokenTypes.Identificador)

    # ── Delimitadores ────────────────────────────────────────────────────────

    def es_punto_y_coma(self) -> bool:
        return self.es_tipo(TokenTypes.PuntoYComa)

    def es_parentesis_i(self) -> bool:
        return self.es_tipo(TokenTypes.ParentesisI)

    def es_parentesis_d(self) -> bool:
        return self.es_tipo(TokenTypes.ParentesisD)

    def es_llave_apertura(self) -> bool:
        return self.es_tipo(TokenTypes.LlaveApertura)

    def es_llave_cierre(self) -> bool:
        return self.es_tipo(TokenTypes.LlaveCierre)

    # ── Especiales ───────────────────────────────────────────────────────────

    def es_nueva_linea(self) -> bool:
        return self.es_tipo(TokenTypes.NuevaLinea)

    def es_error(self) -> bool:
        return self.es_tipo(TokenTypes.Error)

    def es_final_codigo(self) -> bool:
        return self.es_tipo(TokenTypes.FinalCodigo)
