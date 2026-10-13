"""Validaciones de calidad de datos.  [TEMPLATE — completar]

Un registro que no pasa una validación NO debe desaparecer en silencio: se
descarta, se cuenta y se deja un log con el motivo.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Iterable


@dataclass
class ValidationResult:
    valid: list[dict] = field(default_factory=list)
    rejected: list[tuple[dict, str]] = field(default_factory=list)

    @property
    def summary(self) -> dict:
        return {"validos": len(self.valid), "rechazados": len(self.rejected)}


class Validator:
    """Aplica una lista de reglas y separa válidos de rechazados."""

    def __init__(self, rules: list[tuple[str, Callable[[dict], bool]]]) -> None:
        self.rules = rules

    def run(self, records: Iterable[dict]) -> ValidationResult:
        result = ValidationResult()
        for r in records:
            for name, rule in self.rules:
                if not rule(r):
                    result.rejected.append((r, name))
                    break
            else:
                result.valid.append(r)
        return result


def has_id(record: dict) -> bool:
    value = record.get("id_empadronado")
    return isinstance(value, str) and bool(value.strip())


def valid_sexo(record: dict) -> bool:
    return record.get("sexo") in (None, "M", "F")


def valid_estado(record: dict) -> bool:
    return record.get("estado_registro") in {"activo", "suspendido", "fallecido"}


def valid_rango_edad(record: dict) -> bool:
    return record.get("rango_edad") in {"18-25", "26-35", "36-45", "46-60", "61+"}


def valid_fecha_inscripcion(record: dict) -> bool:
    value = record.get("fecha_inscripcion")
    if not isinstance(value, str):
        return False
    try:
        return datetime.strptime(value, "%Y-%m-%d").strftime("%Y-%m-%d") == value
    except ValueError:
        return False
