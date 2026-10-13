"""Transformaciones del padrón.  [TEMPLATE — completar]

Cada transformación es una clase pequeña: recibe los registros (una lista de
diccionarios, uno por fila) y devuelve los registros ya transformados.
`TrimStrings` ya está hecha y sirve de ejemplo: copia su forma.

Los datos de origen traen inconsistencias reales (mayúsculas, valores escritos
de varias formas, fechas en dos formatos, campos vacíos, duplicados). Mira los
archivos de data/empadronados/ antes de escribir código.
"""
from __future__ import annotations

from datetime import datetime
from typing import Iterable

from src.transformers.base import BaseTransformer


class TrimStrings(BaseTransformer):
    """Ejemplo de referencia ya implementado: recorta espacios."""

    def transform(self, records: Iterable[dict]) -> Iterable[dict]:
        for r in records:
            yield {k: (v.strip() if isinstance(v, str) else v) for k, v in r.items()}


class StandardizeCategories(BaseTransformer):

    def __init__(self, mapping: dict[str, dict[str, str]]) -> None:
        self.mapping = mapping

    def transform(self, records: Iterable[dict]) -> Iterable[dict]:
        normalized_mapping = {
            field: {source.strip().casefold(): target for source, target in values.items()}
            for field, values in self.mapping.items()
        }

        for record in records:
            transformed = record.copy()
            for field, values in normalized_mapping.items():
                value = transformed.get(field)
                if value is None or (isinstance(value, str) and not value.strip()):
                    transformed[field] = None
                elif isinstance(value, str):
                    cleaned = value.strip()
                    transformed[field] = values.get(cleaned.casefold(), cleaned)
            yield transformed


class ParseDates(BaseTransformer):
    def __init__(self, fields: list[str]) -> None:
        self.fields = fields

    def transform(self, records: Iterable[dict]) -> Iterable[dict]:
        for record in records:
            transformed = record.copy()
            for field in self.fields:
                value = transformed.get(field)
                if value is None or not str(value).strip():
                    transformed[field] = None
                    continue

                value = str(value).strip()
                parsed = None
                for date_format in ("%Y-%m-%d", "%d/%m/%Y"):
                    try:
                        parsed = datetime.strptime(value, date_format)
                        break
                    except ValueError:
                        continue

            transformed[field] = parsed.strftime("%Y-%m-%d") if parsed else value
            yield transformed


class Deduplicate(BaseTransformer):
    def __init__(self, key: list[str]) -> None:
        self.key = key

    def transform(self, records: Iterable[dict]) -> Iterable[dict]:
        output: list[dict] = []
        positions: dict[tuple, int] = {}

        for record in records:
            key_values = tuple(record.get(field) for field in self.key)
            if not self.key or any(value is None or value == "" for value in key_values):
                output.append(record)
                continue

            if key_values in positions:
                output[positions[key_values]] = record
            else:
                positions[key_values] = len(output)
                output.append(record)

        return iter(output)
