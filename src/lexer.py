from typing import List, Dict, Any
from tokens import TokenTypes, Token


class Lexer:
    """
    Analizador léxico de ArduinoEspañol.
    Recorre la cadena fuente carácter a carácter y produce una lista de Tokens.
    Los errores léxicos se acumulan en self.errores sin detener el análisis.
    """

    # ── Vocabulario completo de ArduinoEspañol ────────────────────────────────
    PALABRAS_CLAVE: Dict[str, TokenTypes] = {
        # Acciones
        'configurar':    TokenTypes.Configurar,
        'encender':      TokenTypes.Encender,
        'apagar':        TokenTypes.Apagar,
        'leer':          TokenTypes.Leer,
        'escribir':      TokenTypes.Escribir,
        'esperar':       TokenTypes.Esperar,
        'mover':         TokenTypes.Mover,
        'repetir':       TokenTypes.Repetir,
        # Componentes
        'led':           TokenTypes.Led,
        'sensor':        TokenTypes.Sensor,
        'servo':         TokenTypes.Servo,
        'buzzer':        TokenTypes.Buzzer,
        'motor':         TokenTypes.Motor,
        'boton':         TokenTypes.Boton,
        'pantalla':      TokenTypes.Pantalla,
        # Sintaxis
        'pin':           TokenTypes.Pin,
        'como':          TokenTypes.Como,
        'en':            TokenTypes.En,
        'a':             TokenTypes.A,
        'durante':       TokenTypes.Durante,
        'veces':         TokenTypes.Veces,
        # Modos de pin
        'entrada':         TokenTypes.Entrada,
        'salida':          TokenTypes.Salida,
        'entrada_pullup':  TokenTypes.EntradaPullup,
        # Valores digitales
        'alto':          TokenTypes.Alto,
        'bajo':          TokenTypes.Bajo,
        # Control de flujo
        'si':            TokenTypes.Si,
        'entonces':      TokenTypes.Entonces,
        'sino':          TokenTypes.SiNo,
        'fin_si':        TokenTypes.FinSi,
        'fin_repetir':   TokenTypes.FinRepetir,
        # Unidades de tiempo / ángulo
        'ms':            TokenTypes.Ms,
        'segundos':      TokenTypes.Segundos,
        'grados':        TokenTypes.Grados,
    }

    def __init__(self, fuente: str) -> None:
        self.fuente: str = fuente
        self.tokens: List[Token] = []
        self.errores: List[str] = []

        self.inicio: int = 0
        self.actual: int = 0
        self.posicion: int = 0
        self.linea: int = 1
        self.columna: int = 1

    # ── Interfaz pública ──────────────────────────────────────────────────────

    def escanear_tokens(self) -> List[Token]:
        """Recorre toda la fuente y devuelve la lista completa de tokens."""
        while not self.es_final():
            self.inicio = self.actual
            self.escanear_token()

        self.tokens.append(
            Token(TokenTypes.FinalCodigo, '', self.linea, self.columna, self.actual)
        )
        return self.tokens

    # ── Primitivas de avance ──────────────────────────────────────────────────

    def es_final(self) -> bool:
        return self.actual >= len(self.fuente)

    def avanzar(self) -> str:
        char = self.fuente[self.actual]
        self.actual += 1
        self.posicion += 1
        self.columna += 1
        return char

    def mirar_siguiente(self) -> str:
        """Devuelve el carácter actual sin consumirlo."""
        if self.es_final():
            return '\0'
        return self.fuente[self.actual]

    def mirar_dos(self) -> str:
        """Devuelve el carácter que viene después del actual."""
        if self.actual + 1 >= len(self.fuente):
            return '\0'
        return self.fuente[self.actual + 1]

    def coincidir(self, esperado: str) -> bool:
        """Consume el carácter actual solo si coincide con el esperado."""
        if self.es_final():
            return False
        if self.fuente[self.actual] != esperado:
            return False
        self.avanzar()
        return True

    def añadir_token(self, tipo: TokenTypes, valor: Any = None) -> None:
        texto = self.fuente[self.inicio:self.actual]
        valor_real = valor if valor is not None else texto
        col_inicio = self.columna - (self.actual - self.inicio)
        self.tokens.append(Token(tipo, valor_real, self.linea, col_inicio, self.inicio))

    # ── Lógica principal de escaneo ───────────────────────────────────────────

    def escanear_token(self) -> None:
        c = self.avanzar()

        # ── Delimitadores ────────────────────────────────────────────────────
        if   c == ';': self.añadir_token(TokenTypes.PuntoYComa)
        elif c == '(': self.añadir_token(TokenTypes.ParentesisI)
        elif c == ')': self.añadir_token(TokenTypes.ParentesisD)
        elif c == '{': self.añadir_token(TokenTypes.LlaveApertura)
        elif c == '}': self.añadir_token(TokenTypes.LlaveCierre)

        # ── Operadores relacionales ──────────────────────────────────────────
        elif c == '>':
            self.añadir_token(TokenTypes.MayorIgualQ if self.coincidir('=') else TokenTypes.MayorQ)
        elif c == '<':
            self.añadir_token(TokenTypes.MenorIgualQ if self.coincidir('=') else TokenTypes.MenorQ)
        elif c == '=':
            if self.coincidir('='):
                self.añadir_token(TokenTypes.Igual)
            else:
                msg = f"Simbolo '=' suelto en linea {self.linea}, col {self.columna - 1}: use '==' para comparar."
                self.errores.append(msg)
                self.añadir_token(TokenTypes.Error, c)
        elif c == '!':
            if self.coincidir('='):
                self.añadir_token(TokenTypes.Diferente)
            else:
                msg = f"Caracter inesperado '!' en linea {self.linea}, col {self.columna - 1}."
                self.errores.append(msg)
                self.añadir_token(TokenTypes.Error, c)

        # ── Comentario con # (estilo ANTLR / Python) ─────────────────────────
        elif c == '#':
            self._procesar_comentario_numeral()

        # ── Comentarios con // o /* */ ───────────────────────────────────────
        elif c == '/':
            if self.coincidir('/'):
                self._procesar_comentario_linea()
            elif self.coincidir('*'):
                self._procesar_comentario_bloque()
            else:
                msg = f"Caracter '/' no reconocido en linea {self.linea}, col {self.columna - 1}."
                self.errores.append(msg)
                self.añadir_token(TokenTypes.Error, c)

        # ── Espacios / retorno de carro / tabulador → se ignoran ─────────────
        elif c in (' ', '\r', '\t'):
            pass

        # ── Salto de línea → NuevaLinea (separador de instrucciones) ─────────
        elif c == '\n':
            self.añadir_token(TokenTypes.NuevaLinea)
            self.linea += 1
            self.columna = 1

        # ── Cadena de texto ──────────────────────────────────────────────────
        elif c == '"':
            self._procesar_cadena()

        # ── Número: entero o flotante ────────────────────────────────────────
        elif c.isdigit():
            self._procesar_numero()

        # ── Identificador / palabra clave / pines analógicos o digitales ─────
        elif c.isalpha() or c == '_':
            self._procesar_identificador()

        # ── Cualquier otra cosa → error léxico ───────────────────────────────
        else:
            msg = f"Caracter desconocido '{c}' en linea {self.linea}, col {self.columna - 1}."
            self.errores.append(msg)
            self.añadir_token(TokenTypes.Error, c)

    # ── Procesadores auxiliares ───────────────────────────────────────────────

    def _procesar_cadena(self) -> None:
        """Reconoce cadenas entre comillas dobles en una sola línea."""
        while self.mirar_siguiente() != '"' and not self.es_final():
            if self.mirar_siguiente() == '\n':
                self.errores.append(
                    f"Cadena sin cerrar en linea {self.linea}: "
                    "las cadenas no pueden ocupar varias lineas."
                )
                self.añadir_token(TokenTypes.Error)
                return
            self.avanzar()

        if self.es_final():
            self.errores.append(
                f"Cadena sin terminar al final del archivo (linea {self.linea})."
            )
            self.añadir_token(TokenTypes.Error)
            return

        self.avanzar()  # consume la comilla de cierre
        valor = self.fuente[self.inicio + 1: self.actual - 1]
        self.añadir_token(TokenTypes.Cadena, valor)

    def _procesar_numero(self) -> None:
        """Reconoce enteros y flotantes (e.g. 100, 3.3)."""
        while self.mirar_siguiente().isdigit():
            self.avanzar()

        if self.mirar_siguiente() == '.' and self.mirar_dos().isdigit():
            self.avanzar()  # consume el punto
            while self.mirar_siguiente().isdigit():
                self.avanzar()

        texto = self.fuente[self.inicio:self.actual]
        valor = float(texto) if '.' in texto else int(texto)
        self.añadir_token(TokenTypes.Numero, valor)

    def _procesar_identificador(self) -> None:
        """
        Reconoce:
          • Pin analógico:  A0 … A5
          • Pin digital:    D0 … D13
          • Palabra clave:  configurar, encender, fin_si, entrada_pullup …
          • Identificador:  nombre de variable del usuario
        """
        while self.mirar_siguiente().isalnum() or self.mirar_siguiente() == '_':
            self.avanzar()

        texto = self.fuente[self.inicio:self.actual]

        # Pin analógico: A seguida de un dígito 0-5
        if len(texto) == 2 and texto[0] == 'A' and texto[1] in '012345':
            self.añadir_token(TokenTypes.PinAnalogico, texto)
            return

        # Pin digital: D seguida de uno o dos dígitos (D0-D13)
        if len(texto) >= 2 and texto[0] == 'D' and texto[1:].isdigit():
            num = int(texto[1:])
            if 0 <= num <= 13:
                self.añadir_token(TokenTypes.PinDigital, texto)
                return

        # Búsqueda en el vocabulario (insensible a mayúsculas)
        tipo = self.PALABRAS_CLAVE.get(texto.lower(), TokenTypes.Identificador)
        self.añadir_token(tipo, texto)

    def _procesar_comentario_numeral(self) -> None:
        """Descarta el resto de la línea desde # (estilo Python / ANTLR)."""
        while self.mirar_siguiente() != '\n' and not self.es_final():
            self.avanzar()

    def _procesar_comentario_linea(self) -> None:
        """Descarta el resto de la línea desde //."""
        while self.mirar_siguiente() != '\n' and not self.es_final():
            self.avanzar()

    def _procesar_comentario_bloque(self) -> None:
        """Descarta todo hasta encontrar el cierre */."""
        while not self.es_final():
            if self.mirar_siguiente() == '\n':
                self.linea += 1
                self.columna = 1
            if self.mirar_siguiente() == '*' and self.mirar_dos() == '/':
                self.avanzar()  # *
                self.avanzar()  # /
                return
            self.avanzar()

        self.errores.append(
            f"Comentario de bloque sin cerrar, inicio en linea {self.linea}."
        )
