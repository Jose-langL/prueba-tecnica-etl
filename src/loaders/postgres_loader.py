"""Loader de PostgreSQL para el padrón.  [TEMPLATE — completar]"""
from __future__ import annotations

from typing import Iterable

from src.loaders.base import BaseLoader
from src.utils.logger import get_logger

logger = get_logger(__name__)


class IncrementalLoader(BaseLoader):
    """Actualización diaria del padrón.

    Cada archivo es una fotografía completa del padrón a una fecha. Debe
    manejar:
      - altas: empadronados que no existían en la tabla -> se insertan
      - cambios: empadronados que ya existían con datos distintos (p. ej. un
        traslado de centro/mesa) -> se actualizan
      - bajas: empadronados que pasan a suspendido / fallecido -> se actualiza
        su estado (no se borra a nadie)

    TODO:
      1. Cargar los registros sin duplicar y sin que la ejecución repetida de
         la misma fecha agregue filas. Pista: busca "PostgreSQL upsert" /
         "INSERT ... ON CONFLICT DO UPDATE". `id_empadronado` ya es llave
         primaria de la tabla.
      2. Registrar hasta qué fecha se procesó (marca de agua). Puedes escribir
         una fila en la tabla electoral.carga_log.
      3. Devolver la cantidad de registros cargados.

    En src/utils/db.py ya tienes `get_connection()` e `insert_many()` como
    punto de partida.
    """

    def __init__(self, table: str, natural_key: list[str], fecha: str) -> None:
        super().__init__(table, natural_key)
        self.fecha = fecha

    def load(self, records: Iterable[dict]) -> int:
        raise NotImplementedError("TODO: implementar")
