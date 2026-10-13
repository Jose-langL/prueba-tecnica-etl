"""Flujo incremental: padrón electoral (fuente viva).  [TEMPLATE — completar]"""
from __future__ import annotations

from src.config.settings import PROJECT_ROOT, source_config
from src.extractors.csv_extractor import CSVExtractor
from src.loaders.postgres_loader import IncrementalLoader
from src.pipelines.base_pipeline import Pipeline
from src.transformers.base import TransformerPipeline
from src.transformers.common import TrimStrings


def build_empadronados_pipeline(fecha: str) -> Pipeline:
    """Construye el flujo para una fecha de proceso.

    Args:
        fecha: fecha de corte en formato YYYY-MM-DD.

    El extractor y el loader ya están conectados. Falta:
      - agregar tus transformaciones en `TransformerPipeline(...)`, en el
        orden en que deben aplicarse
      - (si llegas) armar un `Validator` con las reglas de
        src/quality/validations.py y pasarlo en lugar de `None`
    """
    cfg = source_config("empadronados")
    path = PROJECT_ROOT / cfg["path_pattern"].format(fecha=fecha.replace("-", ""))

    extractor = CSVExtractor(path)
    transformer = TransformerPipeline(
        TrimStrings(),
        # TODO: agrega aquí el resto de transformaciones
    )
    validator = None  # TODO (opcional): Validator([...])
    loader = IncrementalLoader(cfg["target_table"], cfg["natural_key"], fecha)

    pipeline = Pipeline(extractor, transformer, loader, validator)
    pipeline.name = "empadronados"
    return pipeline
