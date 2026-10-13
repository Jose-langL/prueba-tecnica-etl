"""Flujo incremental: padrón electoral (fuente viva).  [TEMPLATE — completar]"""
from __future__ import annotations

from src.config.settings import PROJECT_ROOT, source_config
from src.extractors.csv_extractor import CSVExtractor
from src.loaders.postgres_loader import IncrementalLoader
from src.pipelines.base_pipeline import Pipeline
from src.quality.validations import Validator, has_id, valid_estado, valid_fecha_inscripcion, valid_rango_edad, valid_sexo
from src.transformers.base import TransformerPipeline
from src.transformers.common import Deduplicate, ParseDates, StandardizeCategories, TrimStrings


def build_empadronados_pipeline(fecha: str) -> Pipeline:
    cfg = source_config("empadronados")
    path = PROJECT_ROOT / cfg["path_pattern"].format(fecha=fecha.replace("-", ""))

    extractor = CSVExtractor(path)
    transformer = TransformerPipeline(
        TrimStrings(),
        StandardizeCategories(
            {
                "sexo": {
                    "M": "M",
                    "m": "M",
                    "MASCULINO": "M",
                    "F": "F",
                    "f": "F",
                    "FEMENINO": "F",
                },
                "estado_registro": {
                    "activo": "activo",
                    "suspendido": "suspendido",
                    "fallecido": "fallecido",
                },
                "rango_edad": {
                    "18-25": "18-25",
                    "18 a 25": "18-25",
                    "26-35": "26-35",
                    "26 a 35": "26-35",
                    "36-45": "36-45",
                    "46-60": "46-60",
                    "61+": "61+",
                    "mayor de 60": "61+",
                },
            }
        ),
        ParseDates(["fecha_inscripcion"]),
        Deduplicate(cfg["natural_key"]),
    )
    validator = Validator(
        [
            ("id_empadronado vacío", has_id),
            ("sexo fuera del catálogo", valid_sexo),
            ("estado_registro fuera del catálogo", valid_estado),
            ("rango_edad fuera del catálogo", valid_rango_edad),
            ("fecha_inscripcion inválida", valid_fecha_inscripcion),
        ]
    )
    loader = IncrementalLoader(cfg["target_table"], cfg["natural_key"], fecha)

    pipeline = Pipeline(extractor, transformer, loader, validator)
    pipeline.name = "empadronados"
    return pipeline
