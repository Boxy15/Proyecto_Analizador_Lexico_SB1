"""
main.py — Punto de entrada del analizador léxico ArduinoEspañol.

Uso:
    python src/main.py <archivo.ard>
    python src/main.py tests/valid/programa1.ard
"""

import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

# Asegurar que Python encuentre los módulos en src/
sys.path.insert(0, os.path.dirname(__file__))

from lexer import Lexer
from errors import reportar_tokens, reportar_errores, resumen_tokens


def leer_archivo(ruta: str) -> str:
    """Lee el contenido de un archivo .ard y lo devuelve como cadena."""
    with open(ruta, 'r', encoding='utf-8') as f:
        return f.read()


def ejecutar(ruta_archivo: str) -> None:
    """Orquesta la ejecución completa: lectura → análisis → reporte."""
    if not os.path.isfile(ruta_archivo):
        print(f"\n  [ERROR] No se encontró el archivo: {ruta_archivo}")
        print("  Uso: python src/main.py <archivo.ard>\n")
        sys.exit(1)

    print()
    print(f"  Archivo : {os.path.abspath(ruta_archivo)}")
    print()

    fuente = leer_archivo(ruta_archivo)
    lexer = Lexer(fuente)
    tokens = lexer.escanear_tokens()

    reportar_tokens(tokens)
    reportar_errores(lexer.errores)
    resumen_tokens(tokens)
    print()


def main() -> None:
    if len(sys.argv) < 2:
        print("\n  [ERROR] Debes especificar un archivo .ard")
        print("  Uso: python src/main.py <archivo.ard>")
        print("  Ejemplo: python src/main.py tests/valid/programa1.ard\n")
        sys.exit(1)

    ejecutar(sys.argv[1])


if __name__ == '__main__':
    main()
