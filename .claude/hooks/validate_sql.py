#!/usr/bin/env python3
"""Hook PostToolUse: valida los archivos .sql creados o modificados por Write/Edit.

Entrada: JSON del evento por stdin (se usa tool_input.file_path).
Salida:
  - 0: el archivo no es .sql o pasa la validación (mensaje en stdout).
  - 2: la validación falla; el motivo va a stderr para que Claude Code lo reciba.
  - 1: el evento recibido no es válido (error no bloqueante del propio Hook).

Solo lee el archivo: no lo modifica ni ejecuta consultas.
"""

import json
import re
import sys
from pathlib import Path

DROP_TABLE_PATTERN = re.compile(r"\bDROP\s+TABLE\b", re.IGNORECASE)


def read_event():
    """Lee el evento del Hook desde stdin."""
    try:
        return json.load(sys.stdin)
    except json.JSONDecodeError as error:
        print(f"[validate_sql] Evento JSON inválido en stdin: {error}", file=sys.stderr)
        sys.exit(1)


def get_file_path(event):
    """Extrae la ruta del archivo afectado por la herramienta."""
    tool_input = event.get("tool_input") or {}
    file_path = tool_input.get("file_path")
    return Path(file_path) if file_path else None


def strip_comments_and_strings(sql):
    """Sustituye comentarios y literales por espacios, conservando los saltos de línea.

    Así las palabras dentro de comentarios o cadenas no generan falsos positivos
    y los números de línea del resultado siguen coincidiendo con el original.
    """
    result = []
    i, length = 0, len(sql)

    def blank(text):
        return "".join("\n" if char == "\n" else " " for char in text)

    while i < length:
        char, pair = sql[i], sql[i:i + 2]
        if pair == "--":
            end = sql.find("\n", i)
            end = length if end == -1 else end
        elif pair == "/*":
            end = sql.find("*/", i + 2)
            end = length if end == -1 else end + 2
        elif char in ("'", '"', "`"):
            end = i + 1
            while end < length:
                if sql[end] == char:
                    # Comilla duplicada ('') es un escape dentro del literal.
                    if end + 1 < length and sql[end + 1] == char:
                        end += 2
                        continue
                    end += 1
                    break
                end += 1
        else:
            result.append(char)
            i += 1
            continue
        result.append(blank(sql[i:end]))
        i = end
    return "".join(result)


def find_drop_table_lines(sql):
    """Devuelve los números de línea con instrucciones DROP TABLE reales."""
    cleaned = strip_comments_and_strings(sql)
    return [cleaned.count("\n", 0, match.start()) + 1 for match in DROP_TABLE_PATTERN.finditer(cleaned)]


def validate_sql_file(path):
    """Valida el archivo y devuelve una lista de errores (vacía si es válido)."""
    if not path.is_file():
        return [f"El archivo no existe: {path}"]
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        return [f"No se pudo leer el archivo como UTF-8: {error}"]
    if not content.strip():
        return ["El archivo está vacío."]

    lines = find_drop_table_lines(content)
    if lines:
        line_list = ", ".join(str(line) for line in lines)
        return [f"Contiene instrucciones DROP TABLE (línea(s): {line_list}). No están permitidas."]
    return []


def main():
    path = get_file_path(read_event())
    if path is None or path.suffix.lower() != ".sql":
        sys.exit(0)

    errors = validate_sql_file(path)
    if errors:
        print(f"[validate_sql] ✗ Validación fallida para {path}:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        print("  Corrige el archivo antes de continuar.", file=sys.stderr)
        sys.exit(2)

    print(f"[validate_sql] ✓ {path.name} validado correctamente.")
    sys.exit(0)


if __name__ == "__main__":
    main()
