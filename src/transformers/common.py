"""Transformaciones del padrón.  [TEMPLATE — completar]

Cada transformación es una clase pequeña: recibe los registros (una lista de
diccionarios, uno por fila) y devuelve los registros ya transformados.
`TrimStrings` ya está hecha y sirve de ejemplo: copia su forma.

Los datos de origen traen inconsistencias reales (mayúsculas, valores escritos
de varias formas, fechas en dos formatos, campos vacíos, duplicados). Mira los
archivos de data/empadronados/ antes de escribir código.
"""
from __future__ import annotations

from typing import Iterable

from src.transformers.base import BaseTransformer


class TrimStrings(BaseTransformer):
    """Ejemplo de referencia ya implementado: recorta espacios."""

    def transform(self, records: Iterable[dict]) -> Iterable[dict]:
        for r in records:
            yield {k: (v.strip() if isinstance(v, str) else v) for k, v in r.items()}


class StandardizeCategories(BaseTransformer):
    """Estandariza valores categóricos: sexo, estado_registro, rango_edad.

    `mapping` tiene la forma {columna: {valor_original: valor_estandar}}.
    La forma estándar de cada columna está en el enunciado.

    TODO: implementar. Piensa qué pasa con mayúsculas/minúsculas y con los
    valores vacíos o que no están en el mapeo.
    """

    def __init__(self, mapping: dict[str, dict[str, str]]) -> None:
        self.mapping = mapping

    def transform(self, records: Iterable[dict]) -> Iterable[dict]:
        raise NotImplementedError("TODO: implementar")


class ParseDates(BaseTransformer):
    """Convierte fechas en formato mixto (YYYY-MM-DD y DD/MM/YYYY) a YYYY-MM-DD.

    TODO: implementar. Decide qué haces con una fecha que no se puede leer.
    """

    def __init__(self, fields: list[str]) -> None:
        self.fields = fields

    def transform(self, records: Iterable[dict]) -> Iterable[dict]:
        raise NotImplementedError("TODO: implementar")


class Deduplicate(BaseTransformer):
    """Elimina filas repetidas según la llave (id_empadronado).

    TODO: implementar. Si dos filas tienen la misma llave pero difieren en
    otras columnas, decide cuál se queda y documéntalo en DECISIONES.md.
    """

    def __init__(self, key: list[str]) -> None:
        self.key = key

    def transform(self, records: Iterable[dict]) -> Iterable[dict]:
        raise NotImplementedError("TODO: implementar")
