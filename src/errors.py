"""
errors.py — Módulo de manejo y reporte de errores léxicos.

Centraliza la presentación de errores detectados por el Lexer,
incluyendo número de línea, columna y descripción del problema.
"""

from typing import List
from tokens import Token, TokenTypes


# ── Constantes de formato ──────────────────────────────────────────────────────
ANCHO: int = 60
SEPARADOR: str = "=" * ANCHO


def imprimir_encabezado(titulo: str) -> None:
    """Imprime un encabezado con separadores."""
    print(SEPARADOR)
    print(f"  {titulo}")
    print(SEPARADOR)


def reportar_tokens(tokens: List[Token]) -> None:
    """Imprime la lista numerada de tokens generados por el lexer."""
    imprimir_encabezado("ARDUINOESPAÑOL — TOKENS GENERADOS")
    for i, token in enumerate(tokens, start=1):
        print(f"  [{i:>3}] {token}")


def reportar_errores(errores: List[str]) -> None:
    """
    Imprime los errores léxicos detectados.
    Cada error incluye línea, columna y descripción del problema.
    Si no hay errores muestra un mensaje de éxito.
    """
    if errores:
        print()
        imprimir_encabezado("ERRORES LÉXICOS DETECTADOS")
        for error in errores:
            print(f"  [!] {error}")
        print()
        print(f"  Total de errores: {len(errores)}")
    else:
        print()
        print("  [OK] Sin errores léxicos.")


def resumen_tokens(tokens: List[Token]) -> None:
    """
    Imprime un resumen estadístico de los tokens generados,
    agrupados por categoría (excluyendo NuevaLinea y FinalCodigo).
    """
    conteo: dict = {}
    for token in tokens:
        if token.tipo in (TokenTypes.NuevaLinea, TokenTypes.FinalCodigo):
            continue
        nombre = token.tipo.name
        conteo[nombre] = conteo.get(nombre, 0) + 1

    print()
    imprimir_encabezado("RESUMEN POR CATEGORÍA")
    for tipo, cantidad in sorted(conteo.items(), key=lambda x: -x[1]):
        print(f"  {tipo:<20} {cantidad:>3} ocurrencia(s)")
    total = sum(conteo.values())
    print(f"  {'─' * 28}")
    print(f"  {'TOTAL':<20} {total:>3} token(s)")
